import enum

from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Enum

from src.api.dependencies.database import Base


class Role(enum.Enum):
	User = "user"
	Administrator = "admin"
	Moderator = "moderator"


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, unique=True, index=True)
	email = Column(String, unique=True, index=True)
	hashed_password = Column(String)
	is_active = Column(Boolean, default=True, nullable=False)
	created_at = Column(DateTime, default=func.now())
	role = Column(Enum(Role), default=Role.User, nullable=False)
