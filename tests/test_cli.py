from typer.testing import CliRunner

from fin_ai_risk_eval.cli import app


def test_cli_help():
    result = CliRunner().invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Offline financial AI risk evaluation harness" in result.output


def test_cli_exposes_qa_commands():
    result = CliRunner().invoke(app, ["--help"])
    for command in [
        "generate-cases",
        "run-evals",
        "run-credit-model",
        "run-fairness",
        "make-report",
        "create-demo-outputs",
        "evaluate-outputs",
        "showcase",
    ]:
        assert command in result.output
