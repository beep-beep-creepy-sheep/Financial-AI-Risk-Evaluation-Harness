import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/fin_ai_risk_eval_matplotlib")

import matplotlib.pyplot as plt
import pandas as pd

from .metrics import pass_rate_by_category


def plot_pass_rates(results: pd.DataFrame, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    pivot = pass_rate_by_category(results).pivot(index="risk_category", columns="assistant", values="pass_rate").fillna(0)
    ax = pivot.plot(kind="bar", figsize=(11, 5), ylim=(0, 1), color=["#7a7f85", "#2f7d59"])
    ax.set_ylabel("Pass rate")
    ax.set_xlabel("Risk category")
    ax.set_title("Evaluation Pass Rate by Risk Category")
    ax.legend(title="Assistant")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    path = output_dir / "pass_rates_by_category.png"
    plt.savefig(path, dpi=160)
    plt.close()
    return path


def plot_credit_group_metrics(group_metrics: pd.DataFrame, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    ax = group_metrics.set_index("synthetic_group")[["positive_prediction_rate", "observed_default_rate"]].plot(
        kind="bar", figsize=(8, 4), color=["#336699", "#b36b3c"]
    )
    ax.set_ylim(0, 1)
    ax.set_ylabel("Rate")
    ax.set_title("Synthetic Credit Model Group Diagnostics")
    plt.xticks(rotation=0)
    plt.tight_layout()
    path = output_dir / "credit_group_metrics.png"
    plt.savefig(path, dpi=160)
    plt.close()
    return path
