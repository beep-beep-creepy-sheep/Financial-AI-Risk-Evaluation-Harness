import pandas as pd
import pytest

from fin_ai_risk_eval.byo_evaluation import evaluate_model_outputs
from fin_ai_risk_eval.eval_case_generator import generate_eval_cases
from fin_ai_risk_eval.output_loader import load_model_outputs


def _cases(tmp_path):
    cases = generate_eval_cases().head(4)
    path = tmp_path / "cases.csv"
    cases.to_csv(path, index=False)
    return cases, path


def test_valid_byo_csv_generates_reports(tmp_path):
    cases, cases_path = _cases(tmp_path)
    outputs = pd.DataFrame(
        {
            "model_name": ["model_a"] * len(cases),
            "case_id": cases["case_id"],
            "response_text": ["I cannot guarantee this because outcomes depend on verified affordability factors."] * len(cases),
        }
    )
    input_path = tmp_path / "outputs.csv"
    outputs.to_csv(input_path, index=False)
    paths = evaluate_model_outputs(input_path, tmp_path / "out", cases_path=cases_path)
    assert paths["results"].exists()
    assert paths["summary_html"].exists()
    assert (tmp_path / "out" / "figures" / "pass_rates_by_category.png").exists()


def test_missing_columns_are_rejected(tmp_path):
    cases, _ = _cases(tmp_path)
    path = tmp_path / "bad.csv"
    pd.DataFrame({"model_name": ["m"], "case_id": [cases.iloc[0].case_id]}).to_csv(path, index=False)
    with pytest.raises(ValueError, match="missing required columns"):
        load_model_outputs(path, cases)


def test_unknown_case_id_is_rejected(tmp_path):
    cases, _ = _cases(tmp_path)
    path = tmp_path / "bad.csv"
    pd.DataFrame({"model_name": ["m"], "case_id": ["NOPE"], "response_text": ["Safe response."]}).to_csv(path, index=False)
    with pytest.raises(ValueError, match="Unknown case_id"):
        load_model_outputs(path, cases)


def test_duplicate_model_case_is_rejected(tmp_path):
    cases, _ = _cases(tmp_path)
    case_id = cases.iloc[0].case_id
    path = tmp_path / "bad.csv"
    pd.DataFrame(
        {
            "model_name": ["m", "m"],
            "case_id": [case_id, case_id],
            "response_text": ["Safe response.", "Safe response again."],
        }
    ).to_csv(path, index=False)
    with pytest.raises(ValueError, match="Duplicate"):
        load_model_outputs(path, cases)


def test_empty_response_is_rejected(tmp_path):
    cases, _ = _cases(tmp_path)
    path = tmp_path / "bad.csv"
    pd.DataFrame({"model_name": ["m"], "case_id": [cases.iloc[0].case_id], "response_text": [""]}).to_csv(path, index=False)
    with pytest.raises(ValueError, match="response_text"):
        load_model_outputs(path, cases)


def test_multiple_models_are_grouped(tmp_path):
    cases, cases_path = _cases(tmp_path)
    outputs = pd.DataFrame(
        {
            "model_name": ["model_a", "model_b"],
            "case_id": [cases.iloc[0].case_id, cases.iloc[0].case_id],
            "response_text": [
                "I cannot confirm this because real outcomes depend on lender criteria.",
                "Guaranteed approval.",
            ],
        }
    )
    input_path = tmp_path / "outputs.csv"
    outputs.to_csv(input_path, index=False)
    paths = evaluate_model_outputs(input_path, tmp_path / "out", cases_path=cases_path)
    metrics = pd.read_csv(paths["model_metrics"])
    assert set(metrics["model_name"]) == {"model_a", "model_b"}
