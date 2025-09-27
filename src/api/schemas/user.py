from typing import Optional

from pydantic import BaseModel

from src.api.models.user import Role


class UserBase(BaseModel):
	"""Public representation of a user returned by the API."""
	username: str
	email: str
	is_active: str
	role: Role = Role.User

class UserCreate(UserBase):
	"""Payload used to create a new user account."""
	pass

class UserUpdate(BaseModel):
    """Public representation of a user returned by the API."""
    username: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[str] = None
    role: Role = Role.User

class UserRead(UserBase):
    id: int

    model_config = {
        "from_attributes": True
    }

class UserInDB(UserBase):
	"""Internal model including stored hashed password (not returned by default)."""
	hashed_password: str
