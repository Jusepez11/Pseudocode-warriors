def test_get_pantry_ingredient(client, test_seed_data, authenticate_demo_user):
    response = client.get("/pantryingredient/pantry")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["user_id"] == 1


def test_update_pantry_ingredient(client, test_seed_data, authenticate_demo_user):
    updated_pantry_ingredient = {"unit": "lbs"}

    response = client.put("/pantryingredient/1",json=updated_pantry_ingredient,headers=authenticate_demo_user,    )
    assert response.status_code == 200
    data = response.json()
    assert data["unit"] == updated_pantry_ingredient["unit"]


def test_delete_pantry_ingredient(
    client, test_seed_data, authenticate_demo_user, authenticate_demo_admin_user
):
    response = client.delete("/pantryingredient/1", headers=authenticate_demo_user)
    assert (response.status_code == 403)  # Non-admin pantry_ingredient should not be able to delete

    response = client.delete("/pantryingredient/1", headers=authenticate_demo_admin_user)
    assert (response.status_code == 204)  # Admin pantry_ingredient should be able to delete

    response = client.get("/pantryingredient/1")
    assert response.status_code == 404
