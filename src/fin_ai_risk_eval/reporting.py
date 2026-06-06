from pathlib import Path

import pandas as pd

from .config import FIGURES_DIR, REPORTS_DIR, ensure_dirs
from .metrics import pass_rate_by_category, severity_weighted_score, summary_metrics
from .risk_acceptance import evaluate_against_policy


def _md_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    headers = [str(c) for c in df.columns]
    rows = [[str(v) for v in row] for row in df.to_numpy()]
    table = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    table.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(table)


def write_reports(results: pd.DataFrame, credit_metrics: dict[str, object] | None = None) -> dict[str, Path]:
    ensure_dirs()
    summary = summary_metrics(results)
    by_cat = pass_rate_by_category(results)
    weighted = severity_weighted_score(results)
    acceptance = evaluate_against_policy(results)
    credit_text = "Credit model metrics were not generated in this run."
    if credit_metrics:
        credit_text = "\n".join(f"- {k}: {v:.3f}" if isinstance(v, float) else f"- {k}: {v}" for k, v in credit_metrics["metrics"].items())
    report = f"""# Financial AI Risk Evaluation Report

This report documents an offline, model-agnostic evaluation harness for consumer-finance AI risk. It is not a financial advice product, does not claim regulatory compliance, and does not use real customer data, real bank data, paid model APIs, live APIs, or LLM-as-judge evaluation.

## Executive Summary

The harness compares a weak deterministic baseline assistant against a guarded deterministic assistant across hallucination, consumer harm, fairness, prompt injection, privacy, unsafe tool use, explainability, and uncertainty handling. These assistants are demonstration systems. The reusable contribution is the evaluation harness: synthetic cases, transparent scoring, metrics, plots, and reporting.

## Model-Agnostic Evaluation Design

The same case set can evaluate any model or assistant through the BYO output workflow. A reviewer can provide a local CSV containing `model_name`, `case_id`, and `response_text`; the harness joins those outputs to the synthetic risk cases and produces model-level, category-level, severity-level, and failure-example reports. This makes the project more than a chatbot demo: it is a reproducible risk evaluation workflow.

## Overall Metrics

{_md_table(summary)}

## Severity Weighted Score

{_md_table(weighted)}

## Risk Category Pass Rates

{_md_table(by_cat)}

## Risk Acceptance Results

{_md_table(acceptance)}

## Credit Model Diagnostics

{credit_text}

## Governance Notes

- All scenarios and credit records are synthetic.
- Example model outputs, policies, and personas are synthetic.
- Fairness groups are fictional and do not represent real ethnicity, nationality, or population statistics.
- Evaluators are deterministic rules intended for transparent supervisory-style testing.
- The harness measures safety behaviours, not chatbot helpfulness alone.
- Offline operation supports privacy, auditability, reproducibility, and no-cost execution.
- Deterministic scoring is transparent but should be complemented by expert review for real-world assurance.

![Pass rates](figures/pass_rates_by_category.png)
"""
    model_card = """# Model Card: Offline Financial AI Risk Evaluation Harness

## Intended Use
Evaluate AI risk controls for consumer-finance assistance in a fully offline, model-agnostic demo. Built-in assistants are deterministic demonstration systems; external model outputs can be evaluated through the BYO CSV workflow.

## Out of Scope
This system must not be used for real lending decisions, regulated advice, account access, customer profiling, product recommendation, or claims of regulatory compliance.

## Data
Synthetic prompts, personas, policy documents, example model outputs, and tabular credit records generated locally. No real customer or bank data is used.

## Evaluation
Deterministic policy checks, bootstrap confidence intervals, fairness perturbations, agentic safety checks, failure examples, and a simple scikit-learn credit-risk model diagnostic.

## Key Risks
Hallucination, consumer harm, bias, privacy leakage, prompt injection, unsafe tool use, weak explainability, and overconfidence.

## Limitations
Keyword-based scoring is reproducible and auditable, but it can miss paraphrases and cannot replace expert judgement, legal review, or production monitoring.
"""
    risk_register = """# Risk Register

This register is a synthetic governance artifact for the offline evaluation harness. It is not a compliance opinion.

| Risk | Example Harm | Control | Evidence Artifact |
|---|---|---|---|
| Hallucination | False approval, rate, or policy claim | Unsupported-claim refusal and uncertainty scoring | `category_metrics.csv` |
| Consumer harm | Encouraging unaffordable debt or gambling recovery borrowing | Harmful request refusal | `failure_examples.csv` |
| Fairness bias | Protected-attribute treatment changes | Paired perturbation tests with fictional groups | `fairness_results.csv` |
| Prompt injection | Safety bypass or hidden-policy extraction | Injection pattern tests | `eval_cases.csv` |
| Privacy | Third-party disclosure or over-collection | Privacy refusal and data-minimisation checks | `evaluation_results.csv` |
| Unsafe agent action | Simulated unauthorized approval or record change | Safe tool allow-list and tool-call logging | `evaluation_results.csv` |
| Explainability | Opaque high-stakes guidance | Reason-factor scoring | `category_metrics.csv` |
| Uncertainty | Overreliance on guaranteed outcomes | Caveat and uncertainty scoring | `evaluation_metrics.csv` |
"""
    paths = {
        "report": REPORTS_DIR / "ai_risk_evaluation_report.md",
        "model_card": REPORTS_DIR / "model_card.md",
        "risk_register": REPORTS_DIR / "risk_register.md",
    }
    paths["report"].write_text(report, encoding="utf-8")
    paths["model_card"].write_text(model_card, encoding="utf-8")
    paths["risk_register"].write_text(risk_register, encoding="utf-8")
    FIGURES_DIR.mkdir(exist_ok=True)
    return paths
