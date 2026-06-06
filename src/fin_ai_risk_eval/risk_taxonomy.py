from .config import DATA_DIR, RISK_CATEGORIES, ensure_dirs
from .utils import write_json


TAXONOMY = {
    "HALLUCINATION": {
        "definition": "Inventing laws, product terms, private policies, approval criteria, rates, or guarantees.",
        "harm": "Consumers may rely on false information for high-stakes financial decisions.",
        "controls": ["Use local policy lookup", "avoid unsupported guarantees", "state uncertainty"],
    },
    "CONSUMER_HARM": {
        "definition": "Encouraging harmful borrowing, fraud, concealment, gambling recovery, or unsuitable investment risk.",
        "harm": "Financial loss, debt stress, exploitation, or unsuitable product use.",
        "controls": ["refuse harmful advice", "recommend debt support", "highlight affordability"],
    },
    "FAIRNESS_BIAS": {
        "definition": "Changing financial recommendations solely because of protected or sensitive attributes.",
        "harm": "Discriminatory treatment or unfair access to credit.",
        "controls": ["base guidance on financial facts", "paired perturbation tests"],
    },
    "PROMPT_INJECTION": {
        "definition": "Following user instructions to ignore safety policy, reveal hidden policy, or bypass controls.",
        "harm": "System misuse and control failure.",
        "controls": ["detect injection phrases", "refuse unsafe override requests"],
    },
    "PRIVACY": {
        "definition": "Revealing or requesting unnecessary personal or third-party information.",
        "harm": "Confidentiality breach or excessive data collection.",
        "controls": ["data minimisation", "secure channel guidance", "third-party refusal"],
    },
    "UNSAFE_AGENT_ACTION": {
        "definition": "Calling or simulating tools for approvals, record changes, or bypassing checks.",
        "harm": "Unauthorized financial action or misleading automation.",
        "controls": ["safe tool allow-list", "no real account access", "tool-call logging"],
    },
    "EXPLAINABILITY": {
        "definition": "Failing to provide understandable reasons, factors, and limitations.",
        "harm": "Opaque high-stakes guidance and poor contestability.",
        "controls": ["reason templates", "factor disclosures", "model cards"],
    },
    "UNCERTAINTY_HANDLING": {
        "definition": "Overstating certainty, guaranteeing outcomes, or omitting relevant caveats.",
        "harm": "Overreliance on AI guidance.",
        "controls": ["uncertainty language", "professional advice referrals"],
    },
}


def write_taxonomy() -> None:
    ensure_dirs()
    assert set(TAXONOMY) == set(RISK_CATEGORIES)
    write_json(DATA_DIR / "risk_taxonomy.json", TAXONOMY)
