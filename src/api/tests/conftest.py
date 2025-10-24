import os
import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from src.api.dependencies.database import SessionLocal, engine, Base
from src.api.main import app
from src.api.models import User, Ingredient, Recipe, PantryIngredient
from src.api.seed import seed_if_needed


@pytest.fixture(scope="module")
def client():
	return TestClient(app)


@pytest.fixture(scope="module")
def test_seed_data():
	Base.metadata.create_all(bind=engine)
	seed_if_needed()
	yield
	Base.metadata.drop_all(bind=engine)


def test_ensure_db_nonempty(test_seed_data):
	db = SessionLocal()
	ingredient_count = db.query(Ingredient).count()
	recipe_count = db.query(Recipe).count()
	db.close()
	assert ingredient_count > 0
	assert recipe_count > 0
