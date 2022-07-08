from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.sql.functions import now

from db.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(), primary_key=True, default=True, unique=True, nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    disabled = Column(Boolean, default=False, nullable=False)
    created_at = Column(
        DateTime, info={"verbose_name": "дата создания"}, server_default=now()
    )
    updated_at = Column(
        DateTime, info={"verbose_name": "дата изменения"}, server_default=now(), onupdate=now()
    )
