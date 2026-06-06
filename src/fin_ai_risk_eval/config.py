from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
POLICY_DIR = PROJECT_ROOT / "policy_docs"

RISK_CATEGORIES = [
    "HALLUCINATION",
    "CONSUMER_HARM",
    "FAIRNESS_BIAS",
    "PROMPT_INJECTION",
    "PRIVACY",
    "UNSAFE_AGENT_ACTION",
    "EXPLAINABILITY",
    "UNCERTAINTY_HANDLING",
]

SEVERITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]


def ensure_dirs() -> None:
    for path in [DATA_DIR, REPORTS_DIR, FIGURES_DIR, POLICY_DIR]:
        path.mkdir(parents=True, exist_ok=True)
