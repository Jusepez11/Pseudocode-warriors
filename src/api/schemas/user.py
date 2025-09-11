from pydantic import BaseModel
from typing import Optional

from src.api.models.user import Role


class User(BaseModel):
	username: str
	email: Optional[str] = None
	is_active: Optional[bool] = None
	role: Optional[str] = Role.User


class UserInDB(User):
	hashed_password: str


class UserCreate(BaseModel):
	username: str
	email: str
	password: str
