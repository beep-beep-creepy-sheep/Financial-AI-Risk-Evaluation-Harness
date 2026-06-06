# Project Evolution: V1 to V2

## V1 — Proof-of-Concept Evaluation Harness

The goal of V1 was to build an offline, model-agnostic AI risk evaluation harness for consumer-finance assistant outputs.

V1 features:

- synthetic consumer finance cases;
- deterministic keyword-based checks;
- basic fairness perturbation;
- BYO model-output CSV workflow;
- pass-rate and category metrics;
- HTML/CSV reports.

V1 strengths:

- transparent;
- reproducible;
- no real customer data;
- easy to inspect;
- fully offline and free to run.

V1 limitations:

- keyword checks can miss paraphrases;
- pass rate alone is not enough for risk governance;
- fairness checks were shallow;
- critical failures were not strongly separated;
- methodology needed clearer documentation.

## V2 — Supervisory Evaluation Upgrade

The goal of V2 is to make the harness more suitable for AI risk review in a financial supervision context.

V2 improvements:

- structured rubric scoring;
- explicit failure reasons;
- `risk_score` and `risk_decision`;
- risk acceptance policy;
- `CRITICAL`, `HIGH`, `MEDIUM`, and `LOW` severity thresholds;
- critical-risk gating;
- richer fairness diagnostics;
- stronger tests;
- methodology documentation.

Why this matters:

- moves from "does the model pass some prompts?" to "what residual risk remains?";
- separates minor weaknesses from unacceptable critical failures;
- makes outputs easier for non-technical supervisors to interpret;
- keeps the evaluation transparent and reproducible.

## Interview Talking Point

In V1, I built a proof-of-concept offline evaluation harness to test financial AI assistant outputs against synthetic risk scenarios. It was deliberately simple and transparent: deterministic checks, category-level metrics, and reproducible reports. After reviewing it critically, I realised that a regulator would need more than pass rates. So in V2, I added structured rubric scoring, explicit failure reasons, severity-based risk acceptance thresholds, and critical-risk gating. I also strengthened fairness diagnostics and documented the methodology. The main improvement is that V2 does not just ask whether a model passed a prompt set; it asks whether the remaining risk would be acceptable in a supervisory context.
