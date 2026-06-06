from pathlib import Path

import pandas as pd

from .config import DATA_DIR
from .eval_case_generator import write_eval_cases
from .evaluators import score_model_output
from .html_report import write_html_report
from .metrics import bootstrap_ci
from .output_loader import load_model_outputs, merge_outputs_with_cases
from .plotting import plot_pass_rates
from .risk_acceptance import evaluate_against_policy


def _md_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    headers = [str(c) for c in df.columns]
    table = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in df.iterrows():
        table.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(table)


def _rate_table(results: pd.DataFrame, group_cols: list[str]) -> pd.DataFrame:
    grouped = results.groupby(group_cols, as_index=False).agg(pass_rate=("passed", "mean"), n=("passed", "size"))
    return grouped.sort_values(group_cols)


def _model_metrics(results: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for model, group in results.groupby("model_name"):
        lo, hi = bootstrap_ci(group["passed"].astype(float).to_numpy())
        rows.append({"model_name": model, "pass_rate": group["passed"].mean(), "ci_low": lo, "ci_high": hi, "n": len(group)})
    return pd.DataFrame(rows).sort_values("model_name")


def evaluate_model_outputs(input_path: Path | str, output_dir: Path | str, cases_path: Path | str | None = None) -> dict[str, Path]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    cases_file = Path(cases_path) if cases_path else DATA_DIR / "eval_cases.csv"
    if not cases_file.exists():
        write_eval_cases()
    cases = pd.read_csv(cases_file)
    outputs = load_model_outputs(input_path, cases)
    merged = merge_outputs_with_cases(outputs, cases)
    results = pd.DataFrame([score_model_output(row) for _, row in merged.iterrows()])
    model_metrics = _model_metrics(results)
    category_metrics = _rate_table(results, ["model_name", "risk_category"])
    severity_metrics = _rate_table(results, ["model_name", "severity"])
    risk_acceptance = evaluate_against_policy(results)
    failures = results.loc[~results["passed"], ["model_name", "case_id", "risk_category", "severity", "failure_reasons", "prompt", "response_text"]].copy()
    failures["response_excerpt"] = failures["response_text"].str.slice(0, 260)
    failure_examples = failures.drop(columns=["response_text"]).head(50)

    paths = {
        "results": output_dir / "evaluation_results.csv",
        "model_metrics": output_dir / "model_metrics.csv",
        "category_metrics": output_dir / "category_metrics.csv",
        "severity_metrics": output_dir / "severity_metrics.csv",
        "risk_acceptance": output_dir / "risk_acceptance_results.csv",
        "failure_examples": output_dir / "failure_examples.csv",
        "summary_md": output_dir / "summary_report.md",
        "summary_html": output_dir / "summary_report.html",
    }
    results.to_csv(paths["results"], index=False)
    model_metrics.to_csv(paths["model_metrics"], index=False)
    category_metrics.to_csv(paths["category_metrics"], index=False)
    severity_metrics.to_csv(paths["severity_metrics"], index=False)
    risk_acceptance.to_csv(paths["risk_acceptance"], index=False)
    failure_examples.to_csv(paths["failure_examples"], index=False)

    plot_df = results.rename(columns={"model_name": "assistant"})
    plot_pass_rates(plot_df, output_dir / "figures")
    summary = f"""# BYO Model Output Evaluation Summary

This report evaluates a user-supplied model-output CSV against the synthetic consumer-finance risk cases in this repository.

The workflow is model-agnostic: any model, rules engine, or assistant can be evaluated if its outputs are provided as a local CSV with `model_name`, `case_id`, and `response_text`. The built-in assistants are demonstration systems only; the core contribution is the offline evaluation harness, deterministic scoring, fairness and safety test design, and supervisory-style reporting.

## Important Scope Notes

- All prompts, personas, policies, credit records, and example model outputs are synthetic.
- The project does not provide financial advice and does not claim regulatory compliance.
- No real customer data, paid AI APIs, live APIs, cloud services, or API keys are used.
- Deterministic keyword scoring is transparent and reproducible, but it can miss paraphrases or flag benign mentions.

## Model Metrics

{_md_table(model_metrics)}

## Category Metrics

{_md_table(category_metrics)}

## Severity Metrics

{_md_table(severity_metrics)}

## Risk Acceptance Results

{_md_table(risk_acceptance)}

## Failure Examples

{_md_table(failure_examples.head(10))}

![BYO pass rates](figures/pass_rates_by_category.png)
"""
    paths["summary_md"].write_text(summary, encoding="utf-8")
    write_html_report(paths["summary_html"], model_metrics, category_metrics, severity_metrics, failure_examples)
    return paths
