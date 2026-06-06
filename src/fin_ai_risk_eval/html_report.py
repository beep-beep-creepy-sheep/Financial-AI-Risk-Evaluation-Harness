from html import escape
from pathlib import Path

import pandas as pd


def _html_table(df: pd.DataFrame, max_rows: int = 25) -> str:
    if df.empty:
        return "<p><em>No rows.</em></p>"
    head = "".join(f"<th>{escape(str(col))}</th>" for col in df.columns)
    body = []
    for _, row in df.head(max_rows).iterrows():
        body.append("<tr>" + "".join(f"<td>{escape(str(value))}</td>" for value in row) + "</tr>")
    return f"<table><thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table>"


def write_html_report(
    output_path: Path,
    model_metrics: pd.DataFrame,
    category_metrics: pd.DataFrame,
    severity_metrics: pd.DataFrame,
    failure_examples: pd.DataFrame,
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>BYO Model Output Evaluation Summary</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #1f2933; line-height: 1.45; }}
    h1, h2 {{ color: #102a43; }}
    table {{ border-collapse: collapse; width: 100%; margin: 12px 0 28px; font-size: 14px; }}
    th, td {{ border: 1px solid #d9e2ec; padding: 8px; vertical-align: top; }}
    th {{ background: #f0f4f8; text-align: left; }}
    .note {{ background: #f8fafc; border-left: 4px solid #486581; padding: 12px 16px; }}
  </style>
</head>
<body>
  <h1>BYO Model Output Evaluation Summary</h1>
  <div class="note">
    This offline report evaluates supplied model-output CSV rows against synthetic financial AI risk cases.
    It is model-agnostic, uses deterministic scoring, and does not provide financial advice or claim regulatory compliance.
  </div>
  <h2>Model Metrics</h2>
  {_html_table(model_metrics)}
  <h2>Category Metrics</h2>
  {_html_table(category_metrics, max_rows=100)}
  <h2>Severity Metrics</h2>
  {_html_table(severity_metrics, max_rows=100)}
  <h2>Failure Examples</h2>
  {_html_table(failure_examples, max_rows=20)}
</body>
</html>
"""
    output_path.write_text(html, encoding="utf-8")
    return output_path
