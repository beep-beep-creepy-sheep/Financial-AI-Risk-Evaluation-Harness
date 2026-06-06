from fin_ai_risk_eval.fairness import run_fairness_perturbations


def test_guarded_fairness_perturbations_pass():
    results = run_fairness_perturbations("guarded")
    assert len(results) >= 4
    assert results["pass"].all()
