import numpy as np
import pandas as pd

from .config import DATA_DIR, ensure_dirs


def generate_synthetic_credit_data(n_rows: int = 2500, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    groups = rng.choice(["Group_A", "Group_B", "Group_C"], size=n_rows, p=[0.45, 0.35, 0.20])
    group_shift = np.select([groups == "Group_A", groups == "Group_B", groups == "Group_C"], [200, -100, -250])
    income = np.clip(rng.normal(3200 + group_shift, 950, n_rows), 900, 9000)
    expenses = np.clip(income * rng.normal(0.55, 0.12, n_rows), 500, income * 0.95)
    existing_debt = np.clip(rng.gamma(2.0, 120, n_rows), 0, 1800)
    loan_amount = np.clip(rng.normal(6500, 2500, n_rows), 500, 20000)
    proposed_payment = np.clip(loan_amount / rng.choice([24, 36, 48, 60], n_rows) * 1.12, 30, 900)
    savings = np.clip(rng.normal(income * 1.1, 1600, n_rows), 0, 25000)
    missed = rng.poisson(np.select([groups == "Group_A", groups == "Group_B", groups == "Group_C"], [0.35, 0.55, 0.7]))
    history = np.clip(rng.normal(6.5, 3.5, n_rows), 0, 25)
    vulnerable = rng.binomial(1, 0.12 + (groups == "Group_C") * 0.05)
    dsr = (existing_debt + proposed_payment) / income
    stress = (
        2.2 * dsr
        + 0.35 * (expenses / income)
        + 0.16 * missed
        - 0.00006 * savings
        - 0.04 * history
        + 0.25 * vulnerable
        + rng.normal(0, 0.25, n_rows)
    )
    prob_default = 1 / (1 + np.exp(-2.2 * (stress - 0.75)))
    label = rng.binomial(1, np.clip(prob_default, 0.02, 0.95))
    return pd.DataFrame(
        {
            "applicant_id": [f"SYN-{i:05d}" for i in range(n_rows)],
            "age_band": rng.choice(["18-25", "26-40", "41-55", "56-70", "70+"], n_rows, p=[0.12, 0.35, 0.28, 0.18, 0.07]),
            "employment_status": rng.choice(["employed", "self_employed", "part_time", "unemployed", "retired"], n_rows, p=[0.58, 0.14, 0.12, 0.08, 0.08]),
            "monthly_income": np.round(income, 2),
            "monthly_expenses": np.round(expenses, 2),
            "existing_debt_payment": np.round(existing_debt, 2),
            "requested_loan_amount": np.round(loan_amount, 2),
            "proposed_monthly_payment": np.round(proposed_payment, 2),
            "savings_buffer": np.round(savings, 2),
            "missed_payments_last_12m": np.clip(missed, 0, 8),
            "credit_history_length_years": np.round(history, 1),
            "vulnerable_consumer_flag": vulnerable.astype(bool),
            "region_type": rng.choice(["urban", "suburban", "rural"], n_rows, p=[0.48, 0.34, 0.18]),
            "synthetic_group": groups,
            "default_risk_label": label,
        }
    )


def write_synthetic_credit_data(n_rows: int = 2500, seed: int = 42) -> pd.DataFrame:
    ensure_dirs()
    df = generate_synthetic_credit_data(n_rows=n_rows, seed=seed)
    df.to_csv(DATA_DIR / "synthetic_credit_data.csv", index=False)
    return df
