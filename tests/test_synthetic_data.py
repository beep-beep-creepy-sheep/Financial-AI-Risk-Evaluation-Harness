from fin_ai_risk_eval.synthetic_data import generate_synthetic_credit_data


def test_synthetic_credit_data_shape_and_columns():
    df = generate_synthetic_credit_data(2000, seed=1)
    assert len(df) == 2000
    assert {"applicant_id", "synthetic_group", "default_risk_label"}.issubset(df.columns)
    assert set(df["synthetic_group"]).issubset({"Group_A", "Group_B", "Group_C"})
    assert set(df["default_risk_label"].unique()).issubset({0, 1})
