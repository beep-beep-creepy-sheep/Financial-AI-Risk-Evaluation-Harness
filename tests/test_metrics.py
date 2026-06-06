import pandas as pd

from fin_ai_risk_eval.metrics import bootstrap_ci, pass_rate_by_category, summary_metrics


def test_metrics_return_expected_columns():
    df = pd.DataFrame(
        {
            "assistant": ["a", "a", "a"],
            "risk_category": ["X", "X", "Y"],
            "passed": [True, False, True],
        }
    )
    assert "pass_rate" in pass_rate_by_category(df).columns
    assert "ci_low" in summary_metrics(df).columns
    lo, hi = bootstrap_ci([1, 0, 1], n_boot=100)
    assert 0 <= lo <= hi <= 1
