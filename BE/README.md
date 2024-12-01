# FS test backend

## DB migrations (alembic)
Autogenerate - ```alembic revision --autogenerate -m "Commit message"```

Upgrade - ```alembic upgrade head```


### Testing

Test flows separation: 
```
pytest -m unit
pytest -m integration
pytest -m e2e
```
All flows with report (html) - ```pytest --cov-report html```
All flows with report in console ```pytest --cov-config=.coveragerc --cov=src```


### Ruff linter ([docs](https://docs.astral.sh/ruff/))

To check - ```ruff check```

To fix - ```ruff --fix```
