# Risk Register

This register is a synthetic governance artifact for the offline evaluation harness. It is not a compliance opinion.

| Risk | Example Harm | Control | Evidence Artifact |
|---|---|---|---|
| Hallucination | False approval, rate, or policy claim | Unsupported-claim refusal and uncertainty scoring | `category_metrics.csv` |
| Consumer harm | Encouraging unaffordable debt or gambling recovery borrowing | Harmful request refusal | `failure_examples.csv` |
| Fairness bias | Protected-attribute treatment changes | Paired perturbation tests with fictional groups | `fairness_results.csv` |
| Prompt injection | Safety bypass or hidden-policy extraction | Injection pattern tests | `eval_cases.csv` |
| Privacy | Third-party disclosure or over-collection | Privacy refusal and data-minimisation checks | `evaluation_results.csv` |
| Unsafe agent action | Simulated unauthorized approval or record change | Safe tool allow-list and tool-call logging | `evaluation_results.csv` |
| Explainability | Opaque high-stakes guidance | Reason-factor scoring | `category_metrics.csv` |
| Uncertainty | Overreliance on guaranteed outcomes | Caveat and uncertainty scoring | `evaluation_metrics.csv` |
