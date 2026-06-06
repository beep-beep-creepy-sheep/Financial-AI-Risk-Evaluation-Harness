# Model Card: Offline Financial AI Risk Evaluation Harness

## Intended Use
Evaluate AI risk controls for consumer-finance assistance in a fully offline, model-agnostic demo. Built-in assistants are deterministic demonstration systems; external model outputs can be evaluated through the BYO CSV workflow.

## Out of Scope
This system must not be used for real lending decisions, regulated advice, account access, customer profiling, product recommendation, or claims of regulatory compliance.

## Data
Synthetic prompts, personas, policy documents, example model outputs, and tabular credit records generated locally. No real customer or bank data is used.

## Evaluation
Deterministic policy checks, bootstrap confidence intervals, fairness perturbations, agentic safety checks, failure examples, and a simple scikit-learn credit-risk model diagnostic.

## Key Risks
Hallucination, consumer harm, bias, privacy leakage, prompt injection, unsafe tool use, weak explainability, and overconfidence.

## Limitations
Keyword-based scoring is reproducible and auditable, but it can miss paraphrases and cannot replace expert judgement, legal review, or production monitoring.
