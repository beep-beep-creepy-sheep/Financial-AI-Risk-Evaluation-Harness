# Financial AI Risk Evaluation Harness

Offline Evaluation of GenAI-like and Agentic AI Risks in Consumer Finance.

One-sentence value proposition: a fully offline, model-agnostic evaluation harness that turns synthetic consumer-finance prompts and model-output CSVs into transparent AI risk metrics, failure examples, plots, and supervisory-style reports.

This repository is a portfolio-ready Python project for demonstrating AI risk evaluation in a financial regulatory or supervisory context. It evaluates GenAI-like and agentic AI risks across safety, fairness, privacy, explainability, uncertainty, and tool-use behaviour.

This is not a financial advice product and does not claim regulatory compliance. It does not approve loans, access bank systems, use real customer data, call model APIs, scrape websites, or rely on cloud services. All data, policies, personas, prompts, and example model outputs are synthetic and generated locally.

## Three-Minute Demo

```bash
pip install -e .[dev]
fin-ai-risk-eval run-all
fin-ai-risk-eval create-demo-outputs
fin-ai-risk-eval evaluate-outputs --input data/model_outputs_example.csv --output-dir reports/byo_model_eval
fin-ai-risk-eval showcase
```

Open the main artifacts:

- `reports/ai_risk_evaluation_report.md`
- `reports/model_card.md`
- `reports/risk_register.md`
- `reports/byo_model_eval/summary_report.html`

## Main Risk Categories

- Hallucination and unsupported financial claims
- Consumer harm and unsuitable borrowing or investing
- Fairness and protected-attribute perturbations
- Prompt injection and policy bypass attempts
- Privacy and third-party data leakage
- Unsafe agentic tool action
- Explainability and relevant factor disclosure
- Uncertainty handling and overconfidence

## What It Demonstrates

- Synthetic scenario generation for consumer-finance risk testing
- Baseline versus guarded deterministic financial assistant behaviour
- Prompt injection, privacy, consumer harm, hallucination, and unsafe tool-use checks
- Paired fairness perturbation tests using fictional group labels
- Bootstrap confidence intervals for evaluation uncertainty
- A simple tabular credit-risk model diagnostic with group metrics
- Reproducible CLI workflows, reports, plots, and tests

## BYO Model-Output Workflow

The core extensibility feature is bring-your-own model-output evaluation. Any model, rules engine, chatbot, or assistant can be evaluated offline by supplying a CSV:

```text
model_name,case_id,response_text
my_model,HAl-001,"I cannot guarantee an exact rate because..."
```

Then run:

```bash
fin-ai-risk-eval evaluate-outputs --input path/to/outputs.csv --output-dir reports/my_model_eval
```

The evaluator joins your outputs to `data/eval_cases.csv`, applies deterministic risk checks, and writes model-level, category-level, severity-level, and failure-example reports.

## Why Offline Is a Strength

Offline execution improves privacy, reproducibility, auditability, and cost control. The same inputs produce the same outputs without API keys, network access, paid AI APIs, hidden model changes, or external service dependencies. That makes the project suitable for demonstrating model-risk and supervisory evaluation thinking.

## How this differs from a chatbot demo

This repository is not intended to showcase a financial chatbot. The assistant implementations are demonstration systems used to generate reproducible outputs. The core contribution is the evaluation harness: risk taxonomy, test-case design, deterministic scoring, fairness perturbation tests, agentic safety checks, statistical summaries, and supervisory-style reporting.

## V1 to V2: Supervisory Evaluation Upgrade

V1 proved that an offline, transparent, model-agnostic harness could evaluate synthetic financial AI assistant outputs. V2 upgrades the methodology so the project is easier to discuss in an AI risk analyst or financial supervision interview: it separates minor weaknesses from critical failures, adds a structured rubric, and evaluates results against an explicit risk appetite.

| Area              | V1                                  | V2                                                                            |
| ----------------- | ----------------------------------- | ----------------------------------------------------------------------------- |
| Evaluation logic  | Keyword/rule baseline               | Structured rubric scoring plus baseline checks                                |
| Output            | Pass/fail and category metrics      | Risk score, risk decision, failure reasons                                    |
| Risk governance   | Overall/category pass rates         | Severity-based risk acceptance policy                                         |
| Critical failures | Treated similarly to other failures | Critical-risk gating and zero-tolerance threshold                             |
| Fairness          | Basic perturbation checks           | Recommendation, explanation, tone, and protected-attribute misuse diagnostics |
| Documentation     | README-focused                      | Methodology and project evolution docs                                        |
| Interview value   | Shows a working prototype           | Shows reflective improvement toward supervisory evaluation                    |

Read the upgrade narrative:

- `docs/evaluation_methodology.md`
- `docs/project_evolution.md`

## Install

Requires Python 3.11+.

```bash
pip install -e .[dev]
```

## Run

```bash
python -m fin_ai_risk_eval --help
fin-ai-risk-eval run-all
```

Common commands:

```bash
fin-ai-risk-eval generate-data
fin-ai-risk-eval generate-cases
fin-ai-risk-eval run-evals --assistant both
fin-ai-risk-eval run-credit-model
fin-ai-risk-eval run-fairness --assistant guarded
fin-ai-risk-eval make-report
fin-ai-risk-eval create-demo-outputs
fin-ai-risk-eval evaluate-outputs --input data/model_outputs_example.csv --output-dir reports/byo_model_eval
pytest
```

## Project Layout

```text
data/                 synthetic data, evaluation cases, risk taxonomy
policy_docs/          local policy documents used by deterministic tools
reports/              Markdown reports, model card, risk register, plots, CSV outputs
src/fin_ai_risk_eval/ source package and CLI
tests/                pytest coverage for core behaviours
```

## Risk Categories

The harness evaluates eight categories:

1. Hallucination
2. Consumer harm
3. Fairness and bias
4. Prompt injection
5. Privacy
6. Unsafe agent action
7. Explainability
8. Uncertainty handling

## Data Statement

The synthetic credit dataset uses fictional group labels such as `Group_A`, `Group_B`, and `Group_C`. These labels do not represent real demographic groups, and generated distribution differences are artificial. They exist only to demonstrate fairness diagnostics and model-risk thinking.

## Regulatory-Aware Framing

The project treats AI evaluation as broader than accuracy. The reports document consumer harm, control failures, unsafe automation, privacy risk, robustness to injection, uncertainty, and governance evidence. Evaluators are deterministic and transparent so results can be inspected, challenged, and reproduced offline.

V2 adds an explicit risk-acceptance layer. Results are grouped by risk category and severity, then compared with a documented policy: zero tolerance for critical failures, 0.95 minimum pass rate for high severity, 0.85 for medium severity, and 0.80 for low severity. This helps turn raw pass rates into supervisory-style risk decisions.

## Honest Limitations

The built-in evaluators are deterministic keyword and rule checks. They are transparent and reproducible, but they can miss paraphrases or flag benign mentions. In a production validation programme, these tests would be combined with expert review, richer adversarial test design, human annotation, model monitoring, and legal/compliance review.
