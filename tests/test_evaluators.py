from fin_ai_risk_eval.eval_case_generator import generate_eval_cases
from fin_ai_risk_eval.evaluators import evaluate_cases


def test_evaluate_cases_outputs_both_assistants():
    cases = generate_eval_cases().head(8)
    results = evaluate_cases(cases, "both")
    assert len(results) == 16
    assert {"baseline", "guarded"} == set(results["assistant"])
    assert "passed" in results.columns
