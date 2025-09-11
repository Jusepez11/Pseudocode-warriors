import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.api.dependencies.database import get_db
from src.api.models.user import User as UserModel
from src.api.schemas.user import User as UserSchema
from src.api.controllers import user as user_controller

SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def convert_db_user_to_user(db_user: UserModel) -> UserModel:
	"""Convert database user to Pydantic user model."""
	return UserModel(
		username=db_user.username,
		email=db_user.email,
		is_active=db_user.is_active
	)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
	"""Create a JWT access token."""
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.now(timezone.utc) + expires_delta
	else:
		expire = datetime.now(timezone.utc) + timedelta(minutes=15)

	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
	"""Get the current user from the JWT token."""
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Could not validate credentials",
		headers={"WWW-Authenticate": "Bearer"},
	)

	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		username: str = payload.get("sub")
		if username is None:
			raise credentials_exception
	except JWTError:
		raise credentials_exception

	db_user = user_controller.get_user_by_username(db, username=username)
	if db_user is None:
		raise credentials_exception
	return convert_db_user_to_user(db_user)


async def get_current_active_user(current_user: UserSchema = Depends(get_current_user)):
	"""Get the current active user (not disabled)."""
	if not current_user.is_active:
		raise HTTPException(status_code=400, detail="Inactive user")
	return current_user
