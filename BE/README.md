# FS test backend

## DB migrations (alembic)
Autogenerate - ```alembic revision --autogenerate -m "Commit message"```

Upgrade - ```alembic upgrade head```


### Testing

Local - ```pytest --cov-config=.coveragerc --cov=src```
Local with report (html) - ```pytest --cov-config=.coveragerc --cov=src --cov-report html```


### Ruff linter ([docs](https://docs.astral.sh/ruff/))

To check - ```ruff check```

To fix - ```ruff --fix```
