# Counterparty Pre-check

Cited, confidence-rated pre-check of an Indian business counterparty (company, LLP or proprietor) from public sources. See `counterparty-precheck-plan.md` for scope and sources.

## Setup

Requires Python 3.12+.

```bash
/opt/homebrew/bin/python3.12 -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

## Test

```bash
.venv/bin/pytest
```

API keys go in `.env` (ignored by git), never in code or commits.
