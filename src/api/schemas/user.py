from typing import Optional

from pydantic import BaseModel

from src.api.models.user import Role


class User(BaseModel):
	"""Public representation of a user returned by the API."""
	username: str
	email: Optional[str] = None
	is_active: Optional[bool] = None
	role: Role = Role.User

	class Config:
		orm_mode = True


class UserInDB(User):
	"""Internal model including stored hashed password (not returned by default)."""
	hashed_password: str


class UserCreate(BaseModel):
	"""Payload used to create a new user account."""
	username: str
	email: str
	password: str

	class Config:
		orm_mode = True
