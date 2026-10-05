"""Step 6: one MaxEnt model per species and lead time. Trained on 2015-2024, tested on 2025-2026.
Baseline: month-of-year calendar ("is it jellyfish season?"). A model that cannot beat it is useless.
Outputs: outputs/skill.json (read by the website), outputs/skill_vs_lead_<species>.png, outputs/models/*.pkl"""
import json, pickle
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from elapid import MaxentModel
from sklearn.metrics import roc_auc_score
from config import (INTERIM, OUT, LEAD_DAYS, TRAIN_YEARS, TEST_START, FEATURES, MAP_LEAD,
                    MIN_AT_SEA_TRAIN, MIN_AT_SEA_TEST)
from s02_audit import go_species

def boot_ci(y, s, n=500, seed=0):
    rng, out = np.random.default_rng(seed), []
    for _ in range(n):
        i = rng.integers(0, len(y), len(y))
        if 0 < y[i].sum() < len(i):
            out.append(roc_auc_score(y[i], s[i]))
    lo, hi = np.percentile(out, [2.5, 97.5])
    return float(lo), float(hi)

def score(m, sub, clim):
    s = m.predict(sub[FEATURES])
    c = sub.date.dt.month.map(clim).fillna(0).values
    lo, hi = boot_ci(sub.y.values, s)
    return dict(auc=float(roc_auc_score(sub.y, s)), ci=[lo, hi],
                auc_calendar=float(roc_auc_score(sub.y, c)), n_pres=int(sub.y.sum()), n_bg=int((sub.y == 0).sum()))

def run(sp):
    tag = sp.replace(" ", "_")
    (OUT / "models").mkdir(exist_ok=True)
    rows, importance = [], None
    for L in LEAD_DAYS:
        d = pd.read_csv(INTERIM / f"train_{tag}_L{L}.csv", parse_dates=["date"])
        tr, te = d[d.date.dt.year.isin(TRAIN_YEARS)], d[d.date >= TEST_START]
        open_only = int(tr[tr.at_sea].y.sum()) >= MIN_AT_SEA_TRAIN
        if open_only:
            tr = tr[tr.at_sea]
        m = MaxentModel(beta_multiplier=1.5, random_state=0).fit(tr[FEATURES], tr.y)
        clim = tr.groupby(tr.date.dt.month).y.mean()    # share of sightings that were this species, by month
        row = dict(lead=L, trained_on="open-water sightings only" if open_only else "all sightings",
                   n_train_pres=int(tr.y.sum()), test=score(m, te, clim))
        sea = te[te.at_sea]
        n_sea = int(sea.y.sum())
        row["test_open_water"] = score(m, sea, clim) if n_sea >= MIN_AT_SEA_TEST and (sea.y == 0).any() else dict(n_pres=n_sea)
        rows.append(row)
        pickle.dump(m, open(OUT / "models" / f"maxent_{tag}_L{L}.pkl", "wb"))
        if L == MAP_LEAD:
            imp = m.permutation_importance_scores(te[FEATURES], te.y, n_repeats=10)
            importance = {f: float(v) for f, v in zip(FEATURES, np.asarray(imp).mean(axis=1))}
        t = row["test"]
        print(f"{sp} lead {L}d: AUC {t['auc']:.3f} [{t['ci'][0]:.3f}, {t['ci'][1]:.3f}] "
              f"vs calendar {t['auc_calendar']:.3f} (test sightings {t['n_pres']}, open water {n_sea})")
    r = pd.DataFrame([dict(lead=x["lead"], auc=x["test"]["auc"], lo=x["test"]["ci"][0], hi=x["test"]["ci"][1],
                           cal=x["test"]["auc_calendar"]) for x in rows])
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.fill_between(r.lead, r.lo, r.hi, alpha=.2, color="#7a3cb0")
    ax.plot(r.lead, r.auc, "o-", color="#7a3cb0", lw=2, label="Jelly Alert model")
    ax.plot(r.lead, r.cal, "--", color="#8a8a86", lw=2, label="Calendar only")
    ax.axhline(.5, color="#bbb", lw=.8)
    ax.set(xlabel="Days ahead", ylabel="AUC on 2025-2026 (held out)", title=sp, ylim=(.4, 1))
    ax.legend(frameon=False); fig.tight_layout(); fig.savefig(OUT / f"skill_vs_lead_{tag}.png", dpi=150)
    return dict(rows=rows, importance=importance)

def main():
    skill = {sp: run(sp) for sp in go_species()}
    (OUT / "skill.json").write_text(json.dumps(skill, indent=1))

if __name__ == "__main__":
    main()
