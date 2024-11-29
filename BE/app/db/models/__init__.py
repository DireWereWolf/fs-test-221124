# List of all declared models for alembic (needed for autogenerate support)
# Provided to alembic/env.py
from app.db.models._base import Base # Core

# API models
from app.db.models.user import User