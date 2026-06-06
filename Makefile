.PHONY: install test data evaluate report all clean

install:
	pip install -e .[dev]

test:
	pytest --cov=fin_ai_risk_eval --cov-report=term-missing

data:
	python -m fin_ai_risk_eval generate-data

evaluate:
	python -m fin_ai_risk_eval evaluate --assistant both

report:
	python -m fin_ai_risk_eval report

all: data evaluate report test

clean:
	rm -rf .pytest_cache htmlcov .coverage
