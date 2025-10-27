def test_create_ingredient(client, test_seed_data, authenticate_demo_user):
	new_ingredient = {
		"name": "Tomato"
	}

	response = client.post("/ingredient", json=new_ingredient, headers=authenticate_demo_user)
	assert response.status_code == 200
	data = response.json()
	assert data["name"] == new_ingredient["name"]


def test_get_ingredients(client, test_seed_data):
	response = client.get("/ingredient")
	assert response.status_code == 200
	data = response.json()
	assert isinstance(data, list)
	assert len(data) >= 5
	assert any(ingredient["name"] == "Bacon" for ingredient in data)


def test_search_ingredients(client, test_seed_data):
	response = client.get("/ingredient/search/", params={"query": "Baco", "threshold": 60})
	assert response.status_code == 200
	data = response.json()
	assert isinstance(data, list)
	assert any(ingredient["name"] == "Bacon" for ingredient in data)


def test_update_ingredient(client, test_seed_data, authenticate_demo_user):
	updated_ingredient = {
		"name": "Updated Bacon"
	}

	response = client.put(f"/ingredient/1", json=updated_ingredient, headers=authenticate_demo_user)
	assert response.status_code == 200
	data = response.json()
	assert data["name"] == updated_ingredient["name"]


def test_delete_ingredient(client, test_seed_data, authenticate_demo_user):
	response = client.delete(f"/ingredient/1", headers=authenticate_demo_user)
	assert response.status_code == 204

	response = client.get(f"/ingredient/1")
	assert response.status_code == 404
