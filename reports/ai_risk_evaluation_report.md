# Financial AI Risk Evaluation Report

This report documents an offline, model-agnostic evaluation harness for consumer-finance AI risk. It is not a financial advice product, does not claim regulatory compliance, and does not use real customer data, real bank data, paid model APIs, live APIs, or LLM-as-judge evaluation.

## Executive Summary

The harness compares a weak deterministic baseline assistant against a guarded deterministic assistant across hallucination, consumer harm, fairness, prompt injection, privacy, unsafe tool use, explainability, and uncertainty handling. These assistants are demonstration systems. The reusable contribution is the evaluation harness: synthetic cases, transparent scoring, metrics, plots, and reporting.

## Model-Agnostic Evaluation Design

The same case set can evaluate any model or assistant through the BYO output workflow. A reviewer can provide a local CSV containing `model_name`, `case_id`, and `response_text`; the harness joins those outputs to the synthetic risk cases and produces model-level, category-level, severity-level, and failure-example reports. This makes the project more than a chatbot demo: it is a reproducible risk evaluation workflow.

## Overall Metrics

| assistant | pass_rate | ci_low | ci_high | n |
| --- | --- | --- | --- | --- |
| baseline | 0.05333333333333334 | 0.02 | 0.08666666666666667 | 150 |
| guarded | 0.96 | 0.9266666666666666 | 0.9866666666666667 | 150 |

## Severity Weighted Score

| assistant | severity_weighted_score |
| --- | --- |
| baseline | 0.07272727272727272 |
| guarded | 0.9636363636363636 |

## Risk Category Pass Rates

| assistant | risk_category | pass_rate |
| --- | --- | --- |
| baseline | CONSUMER_HARM | 0.0 |
| baseline | EXPLAINABILITY | 0.0 |
| baseline | FAIRNESS_BIAS | 0.0 |
| baseline | HALLUCINATION | 0.0 |
| baseline | PRIVACY | 0.5333333333333333 |
| baseline | PROMPT_INJECTION | 0.0 |
| baseline | UNCERTAINTY_HANDLING | 0.0 |
| baseline | UNSAFE_AGENT_ACTION | 0.0 |
| guarded | CONSUMER_HARM | 0.76 |
| guarded | EXPLAINABILITY | 1.0 |
| guarded | FAIRNESS_BIAS | 1.0 |
| guarded | HALLUCINATION | 1.0 |
| guarded | PRIVACY | 1.0 |
| guarded | PROMPT_INJECTION | 1.0 |
| guarded | UNCERTAINTY_HANDLING | 1.0 |
| guarded | UNSAFE_AGENT_ACTION | 1.0 |

## Credit Model Diagnostics

- roc_auc: 0.705
- average_precision: 0.471
- accuracy: 0.771
- n_train: 1750.000
- n_test: 750.000

## Governance Notes

- All scenarios and credit records are synthetic.
- Example model outputs, policies, and personas are synthetic.
- Fairness groups are fictional and do not represent real ethnicity, nationality, or population statistics.
- Evaluators are deterministic rules intended for transparent supervisory-style testing.
- The harness measures safety behaviours, not chatbot helpfulness alone.
- Offline operation supports privacy, auditability, reproducibility, and no-cost execution.
- Deterministic scoring is transparent but should be complemented by expert review for real-world assurance.

![Pass rates](figures/pass_rates_by_category.png)
