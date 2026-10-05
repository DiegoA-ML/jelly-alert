# Feature selection (training years only)

Leave-one-year-out cross-validation within 2015-2024, 5 days ahead. Each row is the average AUC over held-out training years. The 2025-2026 test seasons were not used.

| Feature set | Cyanea capillata | Aurelia aurita | Average |
|---|---|---|---|
| ocean+wind | 0.644 | 0.709 | 0.676 |
| ocean+wind+season | 0.705 | 0.737 | 0.721 |
| ocean+wind(3d)+season | 0.709 | 0.736 | 0.723 |
| ocean+wind+season+distance to land | 0.734 | 0.754 | 0.744 |
| Calendar only | 0.679 | 0.680 | 0.680 |

Chosen: **ocean+wind+season+distance to land**. Tested once on 2025-2026 in step 6.
