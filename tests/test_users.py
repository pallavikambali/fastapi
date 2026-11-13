def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )

    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
    assert "password" not in response.json()



def test_get_user(client):
    # First, register a user
    create_response = client.post(
        "/users/",
        json={
            "email": "getuser@example.com",
            "password": "testpassword123"
        }
    )

    user_id = create_response.json()["id"]

    # Now retrieve that user
    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["email"] == "getuser@example.com"


def test_get_user_not_found(client):
    response = client.get("/users/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_user_fixture(test_user):
    assert test_user["email"] == "fixture@example.com"
    assert "id" in test_user
    assert "password" not in test_user
