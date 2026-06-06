import pandas as pd
import typer
from rich.console import Console

from .assistant import BaselineFinancialAssistant, GuardedFinancialAssistant
from .byo_evaluation import evaluate_model_outputs
from .config import DATA_DIR, FIGURES_DIR, REPORTS_DIR, ensure_dirs
from .credit_model import train_credit_model
from .eval_case_generator import write_eval_cases
from .evaluators import evaluate_cases
from .fairness import run_fairness_perturbations
from .metrics import pass_rate_by_category, severity_weighted_score, summary_metrics
from .plotting import plot_credit_group_metrics, plot_pass_rates
from .reporting import write_reports
from .risk_taxonomy import write_taxonomy
from .synthetic_data import write_synthetic_credit_data

app = typer.Typer(help="Offline financial AI risk evaluation harness.")
console = Console()


@app.command("generate-data")
def generate_data(rows: int = 2500, seed: int = 42) -> None:
    """Generate all local synthetic datasets and the risk taxonomy."""
    ensure_dirs()
    credit = write_synthetic_credit_data(n_rows=rows, seed=seed)
    cases = write_eval_cases()
    write_taxonomy()
    console.print(f"Wrote {len(credit)} synthetic credit rows and {len(cases)} evaluation cases.")


@app.command("generate-cases")
def generate_cases() -> None:
    """Generate only the synthetic evaluation case CSV and risk taxonomy."""
    ensure_dirs()
    cases = write_eval_cases()
    write_taxonomy()
    console.print(f"Wrote {len(cases)} evaluation cases to {DATA_DIR / 'eval_cases.csv'}.")


@app.command("evaluate")
@app.command("run-evals")
def evaluate(assistant: str = typer.Option("both", help="Built-in assistant to evaluate: baseline, guarded, or both.")) -> None:
    """Run deterministic risk evaluation for the built-in demonstration assistants."""
    ensure_dirs()
    cases_path = DATA_DIR / "eval_cases.csv"
    if not cases_path.exists():
        write_eval_cases()
    cases = pd.read_csv(cases_path)
    results = evaluate_cases(cases, assistant_name=assistant)
    out = REPORTS_DIR / "evaluation_results.csv"
    results.to_csv(out, index=False)
    summary_metrics(results).to_csv(REPORTS_DIR / "evaluation_metrics.csv", index=False)
    pass_rate_by_category(results).to_csv(REPORTS_DIR / "category_metrics.csv", index=False)
    severity_weighted_score(results).to_csv(REPORTS_DIR / "assistant_comparison.csv", index=False)
    plot_pass_rates(results, FIGURES_DIR)
    console.print(f"Wrote {len(results)} evaluation rows to {out}.")


@app.command("credit-model")
@app.command("run-credit-model")
def credit_model() -> None:
    """Train and evaluate the local synthetic tabular credit-risk model."""
    ensure_dirs()
    data_path = DATA_DIR / "synthetic_credit_data.csv"
    if not data_path.exists():
        write_synthetic_credit_data()
    df = pd.read_csv(data_path)
    result = train_credit_model(df)
    pd.DataFrame([result["metrics"]]).to_csv(REPORTS_DIR / "credit_model_metrics.csv", index=False)
    result["group_metrics"].to_csv(REPORTS_DIR / "credit_model_group_metrics.csv", index=False)
    result["group_metrics"].to_csv(REPORTS_DIR / "credit_group_metrics.csv", index=False)
    plot_credit_group_metrics(result["group_metrics"], FIGURES_DIR)
    console.print(result["metrics"])


@app.command("fairness")
@app.command("run-fairness")
def fairness(assistant: str = typer.Option("guarded", help="Built-in assistant to perturb: baseline or guarded.")) -> None:
    """Run paired protected-attribute perturbation tests for a built-in assistant."""
    ensure_dirs()
    results = run_fairness_perturbations(assistant)
    out = REPORTS_DIR / f"fairness_perturbations_{assistant}.csv"
    results.to_csv(out, index=False)
    results.to_csv(REPORTS_DIR / "fairness_results.csv", index=False)
    console.print(f"Wrote fairness perturbation results to {out}.")


@app.command("report")
@app.command("make-report")
def report() -> None:
    """Generate portfolio-ready Markdown reports from current evaluation outputs."""
    ensure_dirs()
    results_path = REPORTS_DIR / "evaluation_results.csv"
    if not results_path.exists():
        cases = pd.read_csv(DATA_DIR / "eval_cases.csv") if (DATA_DIR / "eval_cases.csv").exists() else write_eval_cases()
        evaluate_cases(cases, "both").to_csv(results_path, index=False)
    credit = None
    if (REPORTS_DIR / "credit_model_metrics.csv").exists():
        credit = {"metrics": pd.read_csv(REPORTS_DIR / "credit_model_metrics.csv").iloc[0].to_dict()}
    results = pd.read_csv(results_path)
    paths = write_reports(results, credit)
    console.print(f"Wrote reports: {', '.join(str(p) for p in paths.values())}")


@app.command("create-demo-outputs")
def create_demo_outputs() -> None:
    """Create an example BYO model-output CSV from the built-in demonstration assistants."""
    ensure_dirs()
    cases_path = DATA_DIR / "eval_cases.csv"
    if not cases_path.exists():
        write_eval_cases()
    cases = pd.read_csv(cases_path)
    assistants = [BaselineFinancialAssistant(), GuardedFinancialAssistant()]
    rows = []
    for assistant in assistants:
        for _, case in cases.iterrows():
            response = assistant.respond(case.prompt, persona={"persona_id": case.persona_id})
            rows.append(
                {
                    "model_name": assistant.name,
                    "case_id": case.case_id,
                    "response_text": response.response_text,
                    "refused": response.refused,
                    "tool_calls": "|".join(call.tool_name for call in response.tool_calls),
                }
            )
    out = DATA_DIR / "model_outputs_example.csv"
    pd.DataFrame(rows).to_csv(out, index=False)
    console.print(f"Wrote example BYO model-output CSV to {out}.")


@app.command("evaluate-outputs")
def evaluate_outputs(
    input: str = typer.Option(..., "--input", help="Path to a local CSV with model_name, case_id, and response_text columns."),
    output_dir: str = typer.Option("reports/byo_model_eval", "--output-dir", help="Directory for BYO evaluation outputs."),
) -> None:
    """Evaluate a bring-your-own model-output CSV against the synthetic risk cases."""
    ensure_dirs()
    paths = evaluate_model_outputs(input, output_dir)
    console.print(f"Wrote BYO evaluation outputs to {paths['summary_md'].parent}.")


@app.command("showcase")
def showcase() -> None:
    """Print a concise portfolio walkthrough and key artifact locations."""
    console.print(
        "\n".join(
            [
                "Financial AI Risk Evaluation Harness",
                "",
                "Three-minute demo:",
                "  fin-ai-risk-eval run-all",
                "  fin-ai-risk-eval create-demo-outputs",
                "  fin-ai-risk-eval evaluate-outputs --input data/model_outputs_example.csv --output-dir reports/byo_model_eval",
                "",
                "Portfolio artifacts:",
                f"  {REPORTS_DIR / 'ai_risk_evaluation_report.md'}",
                f"  {REPORTS_DIR / 'model_card.md'}",
                f"  {REPORTS_DIR / 'risk_register.md'}",
                f"  {REPORTS_DIR / 'byo_model_eval' / 'summary_report.html'}",
                "",
                "Core point: the built-in assistants are demos; the reusable asset is the offline, model-agnostic risk evaluation harness.",
            ]
        )
    )


@app.command("run-all")
def run_all() -> None:
    """Run the complete built-in offline evaluation workflow."""
    generate_data()
    evaluate("both")
    credit_model()
    fairness("baseline")
    fairness("guarded")
    report()
