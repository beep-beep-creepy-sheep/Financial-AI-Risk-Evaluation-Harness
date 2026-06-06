# Validation Notes

This repository uses deterministic keyword and rule checks as a prototype triage layer for synthetic consumer-finance AI risk cases. The scoring is designed to be reproducible and inspectable, not semantically complete.

## What The Evaluator Can Do

- Apply the same checks to every run without API keys, model drift, or hidden external dependencies.
- Surface repeatable failure examples for hallucination, consumer harm, prompt injection, privacy, unsafe tool action, explainability, uncertainty, and fairness diagnostics.
- Preserve failure reasons so reviewers can inspect why a case passed, failed, or needs review.
- Gate critical cases so serious prompt-injection, privacy, or unsafe-agent failures cannot be hidden by good average metrics.

## Deterministic Rule Limitations

Keyword and rule evaluators are intentionally simple. They can miss unsafe paraphrases, sarcasm, multi-step reasoning failures, and context-specific risks. They can also flag benign text that mentions a risky phrase while refusing it. The results should therefore be treated as repeatable triage signals rather than final assurance.

## False Positive Examples

- A response says, "I cannot guarantee approval." A naive keyword rule might detect "guarantee approval" even though the sentence is a refusal.
- A response discusses why "hiding expenses" is harmful. A simple rule might flag the phrase even though the answer discourages the behaviour.
- A privacy-safe response may mention "another customer" while explaining that it cannot reveal another customer's data.

## False Negative Examples

- A model could imply guaranteed approval without using any exact banned phrase.
- A privacy leak could disclose indirectly identifying details without saying "account balance" or "another customer."
- An unsafe agent action could be described in natural language without using the simulated tool name.
- A fairness failure could be expressed through tone, ranking, or framing rather than an explicit protected-attribute phrase.

## Coverage Limitations

The bring-your-own model-output workflow accepts valid subsets of the case file. This is useful for quick experiments and category-specific checks, but partial submissions should not be interpreted as complete benchmark results unless coverage is reported and justified. A formal validation run should require all planned cases, document missing cases, or use a pre-registered sampling rule.

## Why Deterministic Scoring Is Still Useful

Deterministic scoring is useful for reproducibility, auditability, and fast regression checks. It gives reviewers a stable baseline: the same synthetic cases and responses produce the same metrics and failure reasons. That makes it easier to compare model versions, check whether a guardrail change improved critical cases, and inspect individual examples offline.

## What A Real Validation Programme Would Add

In a real programme, deterministic checks would be combined with expert review, human annotation, semantic evaluation, richer adversarial testing, monitoring, and governance evidence. Reviewers would define gold labels, measure false positive and false negative rates, calibrate thresholds against business and consumer-risk appetite, and document residual risk.

Thresholds could be calibrated by running the harness against human-reviewed examples, measuring precision and recall by risk category and severity, setting stricter gates for critical cases, and reviewing disagreements between automated scores and expert labels. Any threshold would need periodic review as products, models, prompts, and risk appetite change.
