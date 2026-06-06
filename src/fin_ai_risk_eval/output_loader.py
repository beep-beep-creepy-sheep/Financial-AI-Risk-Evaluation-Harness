from pathlib import Path

import pandas as pd

REQUIRED_OUTPUT_COLUMNS = {"model_name", "case_id", "response_text"}


def load_model_outputs(input_path: Path | str, cases: pd.DataFrame) -> pd.DataFrame:
    path = Path(input_path)
    if not path.exists():
        raise ValueError(f"Model-output CSV does not exist: {path}")
    outputs = pd.read_csv(path)
    missing = sorted(REQUIRED_OUTPUT_COLUMNS - set(outputs.columns))
    if missing:
        raise ValueError(f"Model-output CSV is missing required columns: {', '.join(missing)}")
    if outputs.empty:
        raise ValueError("Model-output CSV contains no rows.")
    outputs["model_name"] = outputs["model_name"].astype(str).str.strip()
    outputs["case_id"] = outputs["case_id"].astype(str).str.strip()
    outputs["response_text"] = outputs["response_text"].fillna("").astype(str).str.strip()
    if (outputs["model_name"] == "").any():
        raise ValueError("Column model_name contains blank values.")
    if (outputs["case_id"] == "").any():
        raise ValueError("Column case_id contains blank values.")
    empty_responses = outputs.loc[outputs["response_text"] == "", ["model_name", "case_id"]]
    if not empty_responses.empty:
        sample = empty_responses.head(3).to_dict(orient="records")
        raise ValueError(f"response_text contains blank values for examples: {sample}")
    duplicates = outputs.duplicated(["model_name", "case_id"], keep=False)
    if duplicates.any():
        sample = outputs.loc[duplicates, ["model_name", "case_id"]].head(5).to_dict(orient="records")
        raise ValueError(f"Duplicate model_name + case_id rows found: {sample}")
    known_case_ids = set(cases["case_id"].astype(str))
    unknown = sorted(set(outputs["case_id"]) - known_case_ids)
    if unknown:
        raise ValueError(f"Unknown case_id values in model-output CSV: {unknown[:10]}")
    return outputs


def merge_outputs_with_cases(outputs: pd.DataFrame, cases: pd.DataFrame) -> pd.DataFrame:
    case_cols = [
        "case_id",
        "prompt",
        "risk_category",
        "persona_id",
        "persona_description",
        "expected_behavior",
        "should_refuse",
        "protected_attribute_present",
        "injection_present",
        "privacy_sensitive",
        "requires_uncertainty",
        "requires_explanation",
        "severity",
        "tags",
    ]
    return outputs.merge(cases[case_cols], on="case_id", how="left", validate="many_to_one")
