from typing import List, Optional

from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from src.api.models.pantry_ingredient import PantryIngredient as Model
from src.api.models.user import User as UserModel


def create(db: Session, request):
	new_item = Model(
		user_id=request.user_id,
		ingredient_id=request.ingredient_id,
		quantity=request.quantity,
		unit=request.unit
	)

	try:
		db.add(new_item)
		db.commit()
		db.refresh(new_item)
	except SQLAlchemyError as e:
		error = str(e.__dict__['orig'])
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

	return new_item


def read_all(db: Session, skip: int = 0, limit: int = 100, user_id: Optional[int] = None) -> List[type[Model]]:
	try:
		query = db.query(Model)
		if user_id is not None:
			query = query.filter(Model.user_id == user_id)
		result = query.offset(skip).limit(limit).all()
	except SQLAlchemyError as e:
		error = str(e.__dict__['orig'])
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
	return result


def read_by_user(db: Session, username: str) -> List[type[Model]]:
	"""Get all pantry ingredients for a specific user by username."""
	try:
		user = db.query(UserModel).filter(UserModel.username == username).first()
		if not user:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

		result = db.query(Model).options(joinedload(Model.ingredient)).filter(Model.user_id == user.id).all()
	except SQLAlchemyError as e:
		error = str(e.__dict__['orig'])
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
	return result


def read_one(db: Session, id):
	try:
		item = db.query(Model).filter(Model.id == id).first()
		if not item:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
	except SQLAlchemyError as e:
		error = str(e.__dict__['orig'])
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

	return item


def update(db: Session, id, request):
	try:
		item = db.query(Model).filter(Model.id == id)
		if not item.first():
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
		update_data = request.dict(exclude_unset=True)
		item.update(update_data, synchronize_session=False)
		db.commit()
	except SQLAlchemyError as e:
		error = str(e.__dict__['orig'])
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
	return item.first()


def delete(db: Session, id):
	try:
		item = db.query(Model).filter(Model.id == id)
		if not item.first():
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
		item.delete(synchronize_session=False)
		db.commit()
	except SQLAlchemyError as e:
		error = str(e.__dict__['orig'])
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
	return Response(status_code=status.HTTP_204_NO_CONTENT)
