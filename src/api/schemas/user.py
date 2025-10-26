from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator

from src.api.models.user import Role


class User(BaseModel):
	"""Public representation of a user returned by the API."""
	username: str
	email: Optional[str] = None
	is_active: Optional[bool] = None
	role: Role = Role.User

	model_config = {
		"from_attributes": True
	}


class UserCreate(BaseModel):
	"""Payload used to create a new user account."""
	username: str
	email: EmailStr
	password: str

	@field_validator('username')
	@classmethod
	def validate_username(cls, v):
		if not v or len(v.strip()) == 0:
			raise ValueError('Username cannot be empty')
		if len(v) < 3:
			raise ValueError('Username must be at least 3 characters long')
		if len(v) > 50:
			raise ValueError('Username must not exceed 50 characters')
		return v.strip()

	@field_validator('password')
	@classmethod
	def validate_password(cls, v):
		if not v or len(v) == 0:
			raise ValueError('Password cannot be empty')
		if len(v) < 6:
			raise ValueError('Password must be at least 6 characters long')
		if len(v) > 100:
			raise ValueError('Password must not exceed 100 characters')
		return v

	model_config = {
		"from_attributes": True
	}


class UserUpdate(BaseModel):
	"""Public representation of a user returned by the API."""
	username: Optional[str] = None
	email: Optional[str] = None
	is_active: Optional[bool] = None
	role: Role = Role.User


class UserRead(BaseModel):
	"""Public representation of a user returned by the API."""
	id: int
	username: str
	email: str
	is_active: bool
	role: Role

	model_config = {
		"from_attributes": True
	}
