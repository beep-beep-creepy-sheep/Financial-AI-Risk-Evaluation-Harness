import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, average_precision_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


FEATURES = [
    "age_band",
    "employment_status",
    "monthly_income",
    "monthly_expenses",
    "existing_debt_payment",
    "requested_loan_amount",
    "proposed_monthly_payment",
    "savings_buffer",
    "missed_payments_last_12m",
    "credit_history_length_years",
    "vulnerable_consumer_flag",
    "region_type",
    "synthetic_group",
]


def train_credit_model(df: pd.DataFrame, seed: int = 42) -> dict[str, object]:
    y = df["default_risk_label"]
    x = df[FEATURES]
    cat_cols = x.select_dtypes(include=["object", "bool"]).columns.tolist()
    num_cols = [c for c in x.columns if c not in cat_cols]
    pre = ColumnTransformer(
        [
            ("num", StandardScaler(), num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ]
    )
    model = Pipeline([("preprocess", pre), ("model", LogisticRegression(max_iter=1000))])
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=seed, stratify=y)
    model.fit(x_train, y_train)
    scores = model.predict_proba(x_test)[:, 1]
    preds = (scores >= 0.5).astype(int)
    metrics = {
        "roc_auc": float(roc_auc_score(y_test, scores)),
        "average_precision": float(average_precision_score(y_test, scores)),
        "accuracy": float(accuracy_score(y_test, preds)),
        "n_train": int(len(x_train)),
        "n_test": int(len(x_test)),
    }
    group_rows = []
    eval_df = x_test.copy()
    eval_df["y_true"] = y_test.to_numpy()
    eval_df["score"] = scores
    eval_df["pred"] = preds
    for group, g in eval_df.groupby("synthetic_group"):
        group_rows.append(
            {
                "synthetic_group": group,
                "n": len(g),
                "positive_prediction_rate": float(g["pred"].mean()),
                "mean_score": float(g["score"].mean()),
                "observed_default_rate": float(g["y_true"].mean()),
            }
        )
    return {"model": model, "metrics": metrics, "group_metrics": pd.DataFrame(group_rows)}
