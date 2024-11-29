from app.db.models._base import Base

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column
import uuid

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),  # Use PostgreSQL's native UUID type
        primary_key=True,
        default=uuid.uuid4     # Automatically generate UUIDs
    )
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=True)