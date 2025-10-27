def test_get_pantry_ingredient(client, test_seed_data, authenticate_demo_user):
	response = client.get("/pantryingredient/pantry", headers=authenticate_demo_user)
	assert response.status_code == 200
	data = response.json()
	assert len(data) > 0
	assert data[0]["id"] == 1


def test_update_pantry_ingredient(client, test_seed_data, authenticate_demo_user):
	updated_pantry_ingredient = {"unit": "lbs"}

	response = client.put("/pantryingredient/1", json=updated_pantry_ingredient, headers=authenticate_demo_user)
	assert response.status_code == 200
	data = response.json()
	assert data["unit"] == updated_pantry_ingredient["unit"]


def test_delete_pantry_ingredient(client, test_seed_data, authenticate_demo_user):
	response = client.delete("/pantryingredient/1", headers=authenticate_demo_user)
	assert response.status_code == 204

	response = client.get("/pantryingredient/1", headers=authenticate_demo_user)
	assert response.status_code == 404
