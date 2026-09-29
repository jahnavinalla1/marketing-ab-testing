# Marketing landing-page A/B experiment

**Independent portfolio case study · simulated data · no client affiliation**

Experiment design · confidence intervals · statistical testing

[Dashboard file](index.html) · [Decision memo](results/report.md) · [SQL](analysis.sql) · [Python](analyze.py)

## Business problem

A growth team needs a defensible decision on a landing-page variation, beyond comparing two raw conversion percentages.

## Reproduce

This is a self-contained repository. Python 3.10+ is the only dependency; no shared portfolio repository, API key, or third-party package is required.

```sh
git clone https://github.com/jahnavinalla1/marketing-ab-testing.git
cd marketing-ab-testing
python3 run.py
```

`run.py` regenerates the seeded dataset, rebuilds the dashboard and reports, and executes the tests. To analyze the included CSV without replacing it:

```sh
python3 analyze.py
python3 -m unittest discover -s tests -v
```

Open `index.html` in your browser to explore the dashboard. Its data is embedded, so no server is needed. `generate.py` intentionally overwrites `data.csv` with the same simulated sample; `analyze.py` only reads it and rebuilds outputs.

## Data and provenance

One randomly assigned user per row; 6,000 users, independent 50/50 Bernoulli assignment. Seed 3303. Conversion probabilities deliberately differ in the simulation. Data is authored by the deterministic generator in this folder. It contains no real people, company transactions, or external source material. Patterns in the simulation are intentionally constructed for analytical practice; they are not evidence about actual markets or employers.

| Field | Meaning |
|---|---|
| `user_id` | Unique unit of randomization |
| `variant` | A = control, B = treatment |
| `device` | Desktop or Mobile; exploratory dimension |
| `converted` | Binary primary outcome |
| `revenue_cents` | Simulated gross revenue; zero for non-converters |
| `acquisition_cents` | Illustrative cost per assigned user |

## Metric contract and method

Primary estimand is the intention-to-treat absolute conversion difference B−A in percentage points. The two-sided pooled two-proportion z-test uses alpha 0.05. The 95% interval uses an unpooled standard error. A chi-square goodness-of-fit test with one degree of freedom detects sample-ratio mismatch at 0.01. At least 10 conversions and 10 non-conversions per group are required for the normal approximation. No multiple-comparison claims are made for device cuts.

`analysis.sql` is the actual executed SQL, not a decorative example. Python loads the CSV into constrained in-memory SQLite tables, executes named SQL blocks, validates key invariants, calculates any statistical/scenario outputs, and renders the result files. No network, API key, or paid BI license is needed.

## Stakeholders and decision ownership

Growth owns the rollout decision; analytics owns experiment integrity; product owns refund, usability and latency guardrails.

## Data quality and acceptance

User IDs must be unique; variant totals must reconcile; zero converters cannot generate revenue. An SRM failure blocks a rollout conclusion. Primary definition and stopping rules must be set before a real experiment begins.

## Deliverables

- `data.csv`: complete reproducible source dataset.
- `generate.py`: seeded data-generation logic and business assumptions.
- `analysis.sql` / `analyze.py`: executable analytical logic.
- `index.html`: portable interactive dashboard with filtering and sorting.
- `results/metrics.json` and result CSVs: machine-readable, exportable outputs.
- `results/report.md`: computed findings, recommended actions and limitations.

## Interpretation

Read the decision memo for the actual computed results. Recommendations are proposals for a future pilot; no employer outcome, production deployment, cash saving, or measured improvement is claimed. Replacing the synthetic source requires revisiting schema constraints, hardcoded fixture sizes, missing-data policies and the metric contract.
