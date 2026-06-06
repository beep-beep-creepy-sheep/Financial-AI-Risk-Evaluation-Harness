from typing import Any

from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    tool_name: str
    inputs: dict[str, Any] = Field(default_factory=dict)
    output: dict[str, Any] = Field(default_factory=dict)
    safe: bool = True


class AssistantResponse(BaseModel):
    prompt: str
    response_text: str
    assistant_name: str
    risk_flags: list[str] = Field(default_factory=list)
    tool_calls: list[ToolCall] = Field(default_factory=list)
    refused: bool = False
    uncertainty_acknowledged: bool = False
    explanation_present: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class EvalCase(BaseModel):
    case_id: str
    prompt: str
    risk_category: str
    persona_id: str
    persona_description: str
    expected_behavior: str
    should_refuse: bool
    protected_attribute_present: bool
    injection_present: bool
    privacy_sensitive: bool
    requires_uncertainty: bool
    requires_explanation: bool
    severity: str
    tags: str = ""
