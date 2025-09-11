from sqlalchemy.orm import Session
from passlib.context import CryptContext

from src.api.models.user import User
from src.api.schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_id(db: Session, user_id: int):
	"""Get user by ID."""
	return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
	"""Get user by username."""
	return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
	"""Get user by email."""
	return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
	"""Create a new user."""
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


def authenticate_user(db: Session, username: str, password: str):
	"""Authenticate user with username and password."""
	user = get_user_by_username(db, username)
	if not user:
		return False
	if not pwd_context.verify(password, user.hashed_password):
		return False
	return user


def get_all_users(db: Session, skip: int = 0, limit: int = 100):
	"""Get all users with pagination."""
	return db.query(User).offset(skip).limit(limit).all()
