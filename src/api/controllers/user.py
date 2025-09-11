from typing import Optional, List

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.api.models.user import User
from src.api.schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
	"""Return a user by their integer ID, or None if not found."""
	return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
	"""Return a user by username, or None if not found."""
	return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
	"""Return a user by email, or None if not found."""
	return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate) -> User:
	"""Create a new user record with a hashed password and return it."""
	hashed_password = pwd_context.hash(user.password)
	db_user = User(
		username=user.username,
		email=user.email,
		hashed_password=hashed_password
	)

	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return db_user


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
	"""Verify username/password and return the user on success, otherwise False/None."""
	user = get_user_by_username(db, username)
	if not user:
		return None
	if not pwd_context.verify(password, user.hashed_password):
		return None
	return user


def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[type[User]]:
	"""Return a list of users with optional pagination (skip, limit)."""
	return db.query(User).offset(skip).limit(limit).all()
