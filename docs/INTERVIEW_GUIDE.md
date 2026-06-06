# Interview Guide

This is a self-directed AI-assisted prototype, not production regulatory tooling. It uses synthetic prompts, personas, policies, model outputs, reports, and credit data to demonstrate how offline evaluation evidence can be structured and discussed.

## Three-Minute Walkthrough

1. Start with the README and explain that the core idea is a model-agnostic offline evaluation harness for synthetic consumer-finance AI risk cases.
2. Show `data/eval_cases.csv` to explain the risk taxonomy, severity labels, refusal expectations, uncertainty requirements, and explanation requirements.
3. Open `src/fin_ai_risk_eval/evaluators.py` and `src/fin_ai_risk_eval/rubric.py` to show deterministic checks plus structured rubric scoring.
4. Show `reports/byo_model_eval/summary_report.html` or `reports/ai_risk_evaluation_report.md` to demonstrate how raw outputs become metrics, failure examples, and risk decisions.
5. Close with the limitations: deterministic rules are reproducible and auditable, but not a substitute for expert review, semantic evaluation, monitoring, and governance evidence.

## Commands To Run

```bash
pip install -e .[dev]
fin-ai-risk-eval run-all
fin-ai-risk-eval create-demo-outputs
fin-ai-risk-eval evaluate-outputs --input data/model_outputs_example.csv --output-dir reports/byo_model_eval
pytest
```

## Files To Inspect

- `data/eval_cases.csv`: synthetic risk cases and expected behaviour fields.
- `src/fin_ai_risk_eval/evaluators.py`: deterministic text and tool-use checks.
- `src/fin_ai_risk_eval/rubric.py`: category-specific rubric terms and critical gating inputs.
- `src/fin_ai_risk_eval/byo_evaluation.py`: bring-your-own model-output evaluation workflow.
- `reports/byo_model_eval/summary_report.html`: generated report from a model-output CSV.
- `docs/VALIDATION_NOTES.md`: scoring limitations and validation extension path.

## Architecture In One Explanation

The project separates case design, model outputs, deterministic scoring, risk acceptance, and reporting. Synthetic cases define the prompt, risk category, severity, and expected behaviour. A built-in demo assistant or BYO CSV supplies responses. The evaluator applies transparent keyword/rule checks and a structured rubric, then writes metrics, failure examples, plots, and summary reports. The risk-acceptance layer turns raw pass/fail results into severity-aware decisions.

## Likely Questions And Defensible Answers

**Why deterministic scoring instead of an LLM judge?**

Deterministic scoring is reproducible, inspectable, cheap, and easy to run offline. That makes it useful as a baseline triage layer. I would add human-reviewed labels, semantic similarity checks, and calibrated LLM-as-judge experiments before using it for stronger assurance claims.

**Does this prove a model is safe or compliant?**

No. It is a prototype evidence workflow using synthetic data. It can surface repeatable failures and compare outputs against a documented rubric, but it does not establish production safety, regulatory compliance, or final assurance.

**Why use synthetic data?**

Synthetic data avoids exposing real customers and makes the project reproducible in public. The trade-off is that synthetic cases cannot represent the full distribution, complexity, or legal context of real customer interactions.

**How does critical gating work?**

Critical cases such as prompt injection, privacy leakage, and unsafe agent actions are treated more strictly. If forbidden content, forbidden tool action, or missing refusal appears in a critical case, the result is forced into a failure path instead of being averaged away.

**How would you extend this in a real programme?**

I would build human-reviewed gold labels, measure precision and recall by risk category, calibrate thresholds, add semantic and adversarial tests, monitor live drift, and document governance evidence such as ownership, review cadence, escalation paths, and residual risk acceptance.

**Could a model cherry-pick easy cases in the BYO workflow?**

The current BYO loader supports partial submissions so users can run small slices quickly. For a formal benchmark I would require full case coverage, report missing case IDs, and include coverage in the summary metrics so pass rates cannot be interpreted without the denominator.

**Why does the synthetic credit model include fictional group labels?**

The credit model is a diagnostic demonstration, not a lending model. The fictional group labels make group-level metrics visible for fairness discussion. In a real model I would justify or remove sensitive proxies, run ablation tests, compare error rates across groups, and involve legal/compliance review.

**What would you say if someone calls the scorer too keyword-based?**

That criticism is fair. The deterministic scorer is intentionally a transparent baseline for repeatable triage, not a semantic safety judge. The next validation step is to compare it against human-labelled examples and calibrated semantic or LLM-judge methods, then measure false positives and false negatives by risk category.
