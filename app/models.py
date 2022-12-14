# libraries
import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, FLOAT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP

# local libraries
from app.database import Base


class UsersTableItem(Base):
    __tablename__ = 'users'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    color = Column(String, nullable=False)
    location = Column(String, nullable=False)
    lat = Column(FLOAT(precision=32), nullable=False)
    lon = Column(FLOAT(precision=32), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False,
        server_default=text('now()')
    )


class ExperiencesTableItem(Base):
    __tablename__ = 'experiences'

    experience_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id = Column(
        UUID, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False
    )
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    location = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    lat = Column(FLOAT(precision=32), nullable=False)
    lon = Column(FLOAT(precision=32), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')
    )

    owner = relationship('UsersTableItem', lazy='subquery')