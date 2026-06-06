from fin_ai_risk_eval.credit_model import train_credit_model
from fin_ai_risk_eval.synthetic_data import generate_synthetic_credit_data


def test_credit_model_trains_and_reports_group_metrics():
    df = generate_synthetic_credit_data(300, seed=7)
    result = train_credit_model(df)
    assert 0 <= result["metrics"]["roc_auc"] <= 1
    assert {"synthetic_group", "positive_prediction_rate"}.issubset(result["group_metrics"].columns)
