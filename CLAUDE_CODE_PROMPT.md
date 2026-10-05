Paste everything below the line into Claude Code, started from the `jelly-alert` folder (`cd` into it, then `claude`).

---

You are in the `jelly-alert` project folder on my Mac. Goal: run the data pipeline on real data, check the result, and publish the website on GitHub Pages. Read `README.md` and `src/config.py` first.

Rules:
- Python only through uv in this project (`uv sync`, `uv run`). No pip, no conda, no global Python packages. Homebrew is fine for command-line tools (uv, gh) if they are missing.
- Never invent, simulate or fill in data. If a download fails or data is missing, stop and tell me exactly what failed and why.
- Never print the contents of `.env` or any credential.
- Ask me before: creating the GitHub repo, pushing, and deleting any file.

Steps:

1. Tools. Run `uv --version`, `git --version`, `gh --version`. Install uv or gh with brew if missing. If `gh auth status` says I am not logged in, tell me to run `gh auth login` myself and wait for me.

2. Credentials. If `.env` does not exist, copy `.env.example` to `.env`, open it for me, and stop until I say I filled it in. If it exists, check without printing values that every key in `.env.example` has a non-empty value in `.env`. List empty key names and stop if any.

3. `uv sync`.

4. Check the Copernicus dataset IDs before the long downloads: run `uv run --env-file .env copernicusmarine describe --help` to find the right flags, then describe the products `BALTICSEA_MULTIYEAR_PHY_003_011` and `BALTICSEA_ANALYSISFORECAST_PHY_003_006`. Confirm the daily datasets listed in `CMEMS_PHY_PRODUCTS` in `src/config.py` exist, and report their time coverage to me. If an ID has changed, update only that ID in `config.py` and tell me.

5. Run the pipeline in the background with a log: `uv run --env-file .env python src/run_all.py 2>&1 | tee outputs/run.log`. It takes 1 to 3 hours. Check the log every few minutes and give me a one-line status when a step finishes. If a step fails, read the error, fix it only if it is a code or configuration bug (not missing data), and rerun (finished steps are skipped). If the audit says NO-GO for every species, stop and show me `outputs/audit.md`.

6. When it finishes, show me `outputs/audit.md` and `outputs/results.md`. Then check that `docs/index.html` and `docs/about.html` exist, are under 25 MB each, and do not contain the word SYNTHETIC. Run `open docs/index.html` so I can look at it.

7. Git. Run `git init` if needed. Confirm `.gitignore` excludes `.env`, `data/` and `outputs/models/`. `git add -A`, show me `git status`, and confirm `.env` and `data/` are not staged. Commit with the message "Jelly Alert prototype: pipeline and website".

8. Ask me for the repository name (suggest `jelly-alert`). GitHub Pages on a free account needs a public repository; it will contain only code, results and the website, no credentials and no raw data. After my OK: `gh repo create <name> --public --source=. --remote=origin --push`.

9. Turn on GitHub Pages from the `/docs` folder of `main`: `gh api -X POST repos/{owner}/{repo}/pages -f "source[branch]=main" -f "source[path]=/docs"` (use `-X PUT` if Pages already exists). Poll `gh api repos/{owner}/{repo}/pages` until the status is `built`, then open the site URL.

10. Finish with: the website URL, the repository URL, and the headline numbers from `outputs/results.md` (AUC at 5 days ahead against the calendar baseline, and the season check), per species.

For later updates: rerun step 5, then commit and push. Pages rebuilds by itself.
