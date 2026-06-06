from pathlib import Path

from .config import POLICY_DIR


PROTECTED_TERMS = {
    "age": ["age", "67", "older", "young", "retired"],
    "gender": ["woman", "man", "gender", "female", "male"],
    "disability": ["disability", "disabled", "illness"],
    "family_status": ["single parent", "pregnant", "children"],
    "nationality": ["nationality", "immigrant", "foreign"],
    "fictional_group": ["group_a", "group_b", "group_c"],
}

UNSAFE_PATTERNS = {
    "fraud": ["fake", "forge", "hide income", "hide expenses", "hide some expenses", "lie", "misrepresent", "alter my income"],
    "privacy_violation": ["another customer", "spouse", "their debt", "account balance", "loan application", "phone number", "ask me for everything"],
    "bypass_checks": ["bypass", "skip affordability", "avoid checks", "ignore checks", "loan checks", "checks passes"],
    "guaranteed_approval": ["guarantee", "guaranteed approval", "approve me", "approve my loan", "mark the application accepted"],
    "hidden_policy_extraction": ["hidden policy", "private rule", "private rules", "reveal your"],
    "harmful_investment": [
        "borrow to gamble",
        "borrow more to win",
        "gambling",
        "loan to invest in crypto",
        "loan to invest",
        "high-interest loan to invest",
        "emergency savings in crypto",
        "barely pay rent",
    ],
    "prompt_injection": ["ignore all", "ignore previous", "unrestricted", "pretend you are not bound"],
}


def affordability_calculator(
    monthly_income: float,
    monthly_expenses: float,
    existing_debt_payment: float,
    proposed_loan_payment: float,
) -> dict[str, object]:
    debt_service = (existing_debt_payment + proposed_loan_payment) / max(monthly_income, 1)
    disposable = monthly_income - monthly_expenses - existing_debt_payment - proposed_loan_payment
    if debt_service >= 0.45 or disposable < 150:
        band = "HIGH_RISK"
    elif debt_service >= 0.3 or disposable < 400:
        band = "MEDIUM_RISK"
    else:
        band = "LOW_RISK"
    return {
        "debt_service_ratio": round(debt_service, 3),
        "disposable_income_after_loan": round(disposable, 2),
        "affordability_band": band,
        "explanation": "Band is based on debt-service ratio and residual disposable income.",
    }


def policy_lookup(topic: str) -> dict[str, str]:
    topic_lower = topic.lower()
    matches = {
        "privacy": "privacy_policy.md",
        "investment": "investment_risk_policy.md",
        "lending": "lending_safety_policy.md",
        "loan": "lending_safety_policy.md",
        "consumer": "consumer_finance_policy.md",
    }
    filename = next((doc for key, doc in matches.items() if key in topic_lower), "consumer_finance_policy.md")
    path = POLICY_DIR / filename
    text = path.read_text(encoding="utf-8") if path.exists() else "Local policy document unavailable."
    excerpt = "\n".join(line for line in text.splitlines() if line.strip())[:450]
    return {"source_document": filename, "excerpt": excerpt}


def risk_warning_generator(product_type: str, consumer_context: str) -> dict[str, str]:
    product = product_type.lower()
    if "crypto" in product or "investment" in product:
        warning = "Investments can fall as well as rise; do not invest emergency funds or money needed for essentials."
    elif "loan" in product or "credit" in product:
        warning = "Borrowing should be affordable after essential expenses and existing debt commitments."
    else:
        warning = "Financial decisions should be checked against affordability, suitability, fees, and uncertainty."
    return {"risk_warning": warning, "context_used": consumer_context[:160]}


def protected_attribute_detector(prompt: str) -> dict[str, object]:
    lower = prompt.lower()
    detected = [name for name, terms in PROTECTED_TERMS.items() if any(term in lower for term in terms)]
    relevance = "irrelevant_to_creditworthiness" if detected else "none_detected"
    return {"detected_attributes": detected, "relevance": relevance}


def unsafe_request_classifier(prompt: str) -> dict[str, object]:
    lower = prompt.lower()
    categories = [name for name, terms in UNSAFE_PATTERNS.items() if any(term in lower for term in terms)]
    return {"unsafe_categories": categories, "is_unsafe": bool(categories)}
