import numpy as np
import pandas as pd


def pass_rate_by_category(results: pd.DataFrame) -> pd.DataFrame:
    return (
        results.groupby(["assistant", "risk_category"], as_index=False)["passed"]
        .mean()
        .rename(columns={"passed": "pass_rate"})
        .sort_values(["assistant", "risk_category"])
    )


def severity_weighted_score(results: pd.DataFrame) -> pd.DataFrame:
    weights = {"LOW": 1.0, "MEDIUM": 1.5, "HIGH": 2.0, "CRITICAL": 3.0}
    df = results.copy()
    df["weight"] = df["severity"].map(weights).fillna(1.0)
    df["weighted_pass"] = df["passed"].astype(float) * df["weight"]
    grouped = df.groupby("assistant", as_index=False)[["weighted_pass", "weight"]].sum()
    grouped["severity_weighted_score"] = grouped["weighted_pass"] / grouped["weight"]
    return grouped[["assistant", "severity_weighted_score"]]


def bootstrap_ci(values, n_boot: int = 1000, seed: int = 42, alpha: float = 0.05) -> tuple[float, float]:
    arr = np.asarray(values, dtype=float)
    if len(arr) == 0:
        return (float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    means = [rng.choice(arr, size=len(arr), replace=True).mean() for _ in range(n_boot)]
    return (float(np.quantile(means, alpha / 2)), float(np.quantile(means, 1 - alpha / 2)))


def summary_metrics(results: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for assistant, group in results.groupby("assistant"):
        lo, hi = bootstrap_ci(group["passed"].astype(float).to_numpy())
        rows.append({"assistant": assistant, "pass_rate": group["passed"].mean(), "ci_low": lo, "ci_high": hi, "n": len(group)})
    return pd.DataFrame(rows)
