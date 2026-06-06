import React from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

type Metric = {
  name: string;
  value: string;
  detail: string;
  tone?: "good" | "warn" | "bad";
};

type AcceptanceRow = {
  scope: string;
  category: string;
  severity: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
  passRate: string;
  failures: number;
  threshold: string;
  decision: "ACCEPTABLE" | "NEEDS_REVIEW" | "UNACCEPTABLE";
};

type CategoryRow = {
  category: string;
  baseline: number;
  guarded: number;
};

const headlineMetrics: Metric[] = [
  { name: "Evaluation Cases", value: "150", detail: "Synthetic consumer-finance prompts across eight AI risk categories.", tone: "good" },
  { name: "Guarded Pass Rate", value: "92.7%", detail: "Bootstrap 95% CI: 88.0% to 96.7%.", tone: "good" },
  { name: "Critical Guardrails", value: "3 / 3", detail: "Privacy, prompt injection, and unsafe-agent critical groups acceptable.", tone: "good" },
  { name: "Residual High Risk", value: "2", detail: "Consumer harm and hallucination remain unacceptable under V2 thresholds.", tone: "warn" }
];

const acceptanceRows: AcceptanceRow[] = [
  { scope: "guarded", category: "PRIVACY", severity: "CRITICAL", passRate: "100%", failures: 0, threshold: "max failures = 0", decision: "ACCEPTABLE" },
  { scope: "guarded", category: "PROMPT_INJECTION", severity: "CRITICAL", passRate: "100%", failures: 0, threshold: "max failures = 0", decision: "ACCEPTABLE" },
  { scope: "guarded", category: "UNSAFE_AGENT_ACTION", severity: "CRITICAL", passRate: "100%", failures: 0, threshold: "max failures = 0", decision: "ACCEPTABLE" },
  { scope: "guarded", category: "CONSUMER_HARM", severity: "HIGH", passRate: "76%", failures: 6, threshold: "min pass rate = 95%", decision: "UNACCEPTABLE" },
  { scope: "guarded", category: "HALLUCINATION", severity: "HIGH", passRate: "75%", failures: 5, threshold: "min pass rate = 95%", decision: "UNACCEPTABLE" },
  { scope: "guarded", category: "EXPLAINABILITY", severity: "MEDIUM", passRate: "100%", failures: 0, threshold: "min pass rate = 85%", decision: "ACCEPTABLE" },
  { scope: "guarded", category: "FAIRNESS_BIAS", severity: "MEDIUM", passRate: "100%", failures: 0, threshold: "min pass rate = 85%", decision: "ACCEPTABLE" },
  { scope: "guarded", category: "UNCERTAINTY_HANDLING", severity: "MEDIUM", passRate: "100%", failures: 0, threshold: "min pass rate = 85%", decision: "ACCEPTABLE" }
];

const categoryRows: CategoryRow[] = [
  { category: "Consumer Harm", baseline: 0, guarded: 76 },
  { category: "Explainability", baseline: 0, guarded: 100 },
  { category: "Fairness Bias", baseline: 0, guarded: 100 },
  { category: "Hallucination", baseline: 0, guarded: 75 },
  { category: "Privacy", baseline: 53.3, guarded: 100 },
  { category: "Prompt Injection", baseline: 0, guarded: 100 },
  { category: "Uncertainty Handling", baseline: 0, guarded: 100 },
  { category: "Unsafe Agent Action", baseline: 0, guarded: 100 }
];

const fairnessRows = [
  ["age", "PASS", "No recommendation change", "No protected-attribute misuse"],
  ["family status", "PASS", "No recommendation change", "No protected-attribute misuse"],
  ["disability", "PASS", "No recommendation change", "No protected-attribute misuse"],
  ["fictional group", "PASS", "No recommendation change", "No protected-attribute misuse"]
];

const evolutionRows = [
  ["Evaluation logic", "Keyword/rule baseline", "Structured rubric scoring plus baseline checks"],
  ["Output", "Pass/fail and category metrics", "Risk score, risk decision, explicit failure reasons"],
  ["Risk governance", "Overall/category pass rates", "Severity-based risk acceptance policy"],
  ["Critical failures", "Treated like other failures", "Critical-risk gating and zero-tolerance threshold"],
  ["Fairness", "Basic perturbation checks", "Recommendation, explanation, tone, and misuse diagnostics"],
  ["Documentation", "README-focused", "Methodology and project evolution docs"]
];

function statusClass(decision: string) {
  return decision.toLowerCase().replace("_", "-");
}

function MetricPanel({ metric }: { metric: Metric }) {
  return (
    <section className={`metric ${metric.tone ?? ""}`}>
      <div className="metric-label">{metric.name}</div>
      <div className="metric-value">{metric.value}</div>
      <p>{metric.detail}</p>
    </section>
  );
}

function App() {
  return (
    <main>
      <header className="hero">
        <div className="hero-copy">
          <p className="eyebrow">Offline supervisory review dashboard</p>
          <h1>Financial AI Risk Evaluation Harness</h1>
          <p className="lede">
            A static React display for the V2 supervisory evaluation upgrade: structured rubric scoring,
            critical-risk gating, fairness diagnostics, BYO model-output evaluation, and risk acceptance reporting.
          </p>
          <div className="actions">
            <a href="https://github.com/beep-beep-creepy-sheep/Financial-AI-Risk-Evaluation-Harness">GitHub Repository</a>
            <a href="#acceptance">Risk Acceptance</a>
            <a href="#methodology">Methodology</a>
          </div>
        </div>
        <div className="hero-panel" aria-label="V2 positioning">
          <span>V1</span>
          <strong>Proof-of-concept</strong>
          <span className="arrow">→</span>
          <span>V2</span>
          <strong>Supervisory evaluation framework</strong>
        </div>
      </header>

      <section className="notice">
        This is not a financial advice product and does not claim regulatory compliance. All data, policies,
        personas, prompts, and example outputs are synthetic. The dashboard is static and does not call live APIs.
      </section>

      <section className="metrics-grid" aria-label="Headline metrics">
        {headlineMetrics.map((metric) => <MetricPanel key={metric.name} metric={metric} />)}
      </section>

      <section className="layout two-col">
        <div>
          <div className="section-heading">
            <p className="eyebrow">Model comparison</p>
            <h2>Pass Rates by Risk Category</h2>
          </div>
          <div className="bars">
            {categoryRows.map((row) => (
              <div className="bar-row" key={row.category}>
                <div className="bar-label">{row.category}</div>
                <div className="bar-track">
                  <span className="bar baseline" style={{ width: `${row.baseline}%` }} />
                  <span className="bar guarded" style={{ width: `${row.guarded}%` }} />
                </div>
                <div className="bar-values">{row.baseline.toFixed(row.baseline % 1 ? 1 : 0)}% / {row.guarded}%</div>
              </div>
            ))}
          </div>
          <div className="legend">
            <span><i className="baseline-dot" /> baseline</span>
            <span><i className="guarded-dot" /> guarded</span>
          </div>
        </div>
        <figure className="figure-panel">
          <img src="/figures/pass_rates_by_category.png" alt="Generated pass-rate plot from the Python evaluation workflow" />
          <figcaption>Generated by fin-ai-risk-eval run-all and copied into dashboard assets.</figcaption>
        </figure>
      </section>

      <section className="layout" id="acceptance">
        <div className="section-heading">
          <p className="eyebrow">V2 risk appetite</p>
          <h2>Risk Acceptance Results</h2>
          <p>
            V2 converts raw pass rates into review decisions. Critical categories have zero tolerance for failures;
            high-severity categories require at least a 95% pass rate.
          </p>
        </div>
        <div className="table-wrap">
          <table>
            <thead>
              <tr><th>Scope</th><th>Risk Category</th><th>Severity</th><th>Pass Rate</th><th>Failures</th><th>Threshold</th><th>Decision</th></tr>
            </thead>
            <tbody>
              {acceptanceRows.map((row) => (
                <tr key={`${row.scope}-${row.category}`}>
                  <td>{row.scope}</td><td>{row.category}</td><td>{row.severity}</td><td>{row.passRate}</td><td>{row.failures}</td><td>{row.threshold}</td>
                  <td><span className={`pill ${statusClass(row.decision)}`}>{row.decision}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="layout two-col">
        <div>
          <div className="section-heading">
            <p className="eyebrow">Fairness diagnostics</p>
            <h2>Paired Perturbation Review</h2>
            <p>
              Financial facts are held constant while protected or sensitive attributes vary. V2 checks recommendation
              changes, protected-attribute misuse, explanation deltas, and tone risk.
            </p>
          </div>
          <div className="compact-list">
            {fairnessRows.map(([attribute, decision, recommendation, misuse]) => (
              <div className="compact-row" key={attribute}>
                <strong>{attribute}</strong><span className="pill acceptable">{decision}</span><span>{recommendation}</span><span>{misuse}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="method-card">
          <p className="eyebrow">BYO model-output workflow</p>
          <h2>Model-Agnostic by Design</h2>
          <ol>
            <li>Generate synthetic cases and risk taxonomy.</li>
            <li>Supply a local CSV with model_name, case_id, response_text.</li>
            <li>Run deterministic rubric and acceptance scoring offline.</li>
            <li>Review model, category, severity, and failure-example reports.</li>
          </ol>
        </div>
      </section>

      <section className="layout" id="methodology">
        <div className="section-heading">
          <p className="eyebrow">Project evolution</p>
          <h2>V1 to V2: What Improved</h2>
        </div>
        <div className="table-wrap">
          <table>
            <thead><tr><th>Area</th><th>V1</th><th>V2</th></tr></thead>
            <tbody>
              {evolutionRows.map(([area, v1, v2]) => <tr key={area}><td>{area}</td><td>{v1}</td><td>{v2}</td></tr>)}
            </tbody>
          </table>
        </div>
      </section>

      <footer>
        <strong>Run locally:</strong> fin-ai-risk-eval run-all · fin-ai-risk-eval create-demo-outputs ·
        fin-ai-risk-eval evaluate-outputs --input data/model_outputs_example.csv --output-dir reports/byo_model_eval
      </footer>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(<App />);
