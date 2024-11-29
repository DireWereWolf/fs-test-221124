import logging
from uuid import uuid4
from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    event,
)
from sqlalchemy.orm import registry, relationship
from sqlalchemy.dialects.postgresql import UUID as PgUUID

from src.provision.domain import models

logger = logging.getLogger(__name__)

# Create a registry instance for mapping
mapper_registry = registry()

metadata = mapper_registry.metadata

users = Table(
    "users",
    metadata,
    Column(
        "user_id",
        PgUUID(as_uuid=True),  # Use PostgreSQL's native UUID type
        primary_key=True,
        default=uuid4  # Automatically generate UUIDs
    ),
    Column("nickname", String, nullable=True),
    Column("email", String, nullable=True),
    Column("first_name", String, nullable=True),
    Column("surname", String, nullable=True),
)


def start_mappers():
    logger.info("Starting mappers")
    mapper_registry.map_imperatively(
        models.User,
        users,
    )