"""Step 6a: choose the feature set, using the training years ONLY (2015-2024).
Leave-one-year-out: for each training year, fit on the other nine and score on the held-out one.
The set with the best average AUC (both species, MAP_LEAD days ahead) is written into config.py.
The 2025-2026 test seasons are not read here, so the final test in step 6 stays a fair, one-shot test.
Output: outputs/feature_selection.md"""
import json, re
import numpy as np, pandas as pd
from elapid import MaxentModel
from sklearn.metrics import roc_auc_score
from config import ROOT, INTERIM, OUT, TRAIN_YEARS, FEATURE_SETS, MAP_LEAD, MIN_AT_SEA_TRAIN
from s02_audit import go_species

def cv(d, feats):
    """Mean AUC over held-out training years, for the model and for the calendar-only baseline."""
    model, cal = [], []
    for y in TRAIN_YEARS:
        tr, te = d[d.date.dt.year != y], d[d.date.dt.year == y]
        if te.y.sum() < 10 or (te.y == 0).sum() < 10:
            continue
        if int(tr[tr.at_sea].y.sum()) >= MIN_AT_SEA_TRAIN:
            tr = tr[tr.at_sea]
        m = MaxentModel(beta_multiplier=1.5, random_state=0).fit(tr[feats], tr.y)
        clim = tr.groupby(tr.date.dt.month).y.mean()
        model.append(roc_auc_score(te.y, m.predict(te[feats])))
        cal.append(roc_auc_score(te.y, te.date.dt.month.map(clim).fillna(0)))
    return float(np.mean(model)), float(np.mean(cal)), len(model)

def main():
    res = []
    for sp in go_species():
        d = pd.read_csv(INTERIM / f"train_{sp.replace(' ', '_')}_L{MAP_LEAD}.csv", parse_dates=["date"])
        d = d[d.date.dt.year.isin(TRAIN_YEARS)]
        for name, feats in FEATURE_SETS.items():
            auc, cal, n = cv(d, feats)
            res.append(dict(species=sp, set=name, auc=auc, calendar=cal, years=n))
            print(f"{sp} | {name}: CV AUC {auc:.3f} (calendar {cal:.3f}, {n} years)")
    r = pd.DataFrame(res)
    mean = r.groupby("set").auc.mean()
    order = list(FEATURE_SETS)
    best = max(order, key=lambda s: (round(mean[s], 3), -len(FEATURE_SETS[s])))   # tie: fewer features
    lines = ["# Feature selection (training years only)\n\n",
             f"Leave-one-year-out cross-validation within {TRAIN_YEARS[0]}-{TRAIN_YEARS[-1]}, {MAP_LEAD} days ahead. "
             "Each row is the average AUC over held-out training years. The 2025-2026 test seasons were not used.\n\n",
             "| Feature set | " + " | ".join(go_species()) + " | Average |\n|---|" + "---|" * (len(go_species()) + 1) + "\n"]
    for s in order:
        lines.append(f"| {s} | " + " | ".join(f"{r[(r.set == s) & (r.species == sp)].auc.iloc[0]:.3f}" for sp in go_species())
                     + f" | {mean[s]:.3f} |\n")
    lines.append("| Calendar only | " + " | ".join(f"{r[r.species == sp].calendar.iloc[0]:.3f}" for sp in go_species())
                 + f" | {r.groupby('species').calendar.first().mean():.3f} |\n")
    lines.append(f"\nChosen: **{best}**. Tested once on 2025-2026 in step 6.\n")
    (OUT / "feature_selection.md").write_text("".join(lines))
    (INTERIM / "feature_selection.json").write_text(json.dumps(dict(
        chosen=best, sets=order, auc={s: round(float(mean[s]), 3) for s in order},
        calendar=round(float(r.groupby("species").calendar.first().mean()), 3))))
    cfg = ROOT / "src" / "config.py"
    cfg.write_text(re.sub(r'^FEATURE_SET = "[^"]*"', f'FEATURE_SET = "{best}"', cfg.read_text(), flags=re.M))
    print("".join(lines))

if __name__ == "__main__":
    main()
