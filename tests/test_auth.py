def test_login(client):
    # Step 1: Register a user
    client.post(
        "/users/",
        json={
            "email": "login@example.com",
            "password": "testpassword123"
        }
    )

    # Step 2: Log in using the registered credentials
    response = client.post(
        "/login",
        data={
            "username": "login@example.com",
            "password": "testpassword123"
        }
    )

    # Step 3: Verify the response
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert "access_token" in response.json()


def test_incorrect_password(client):
    # Register a user
    client.post(
        "/users/",
        json={
            "email": "wrongpass@example.com",
            "password": "correctpassword123"
        }
    )

    # Attempt login with an incorrect password
    response = client.post(
        "/login",
        data={
            "username": "wrongpass@example.com",
            "password": "wrongpassword123"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_valid_token_access(client):
    # Register a user
    client.post("/users/", json={
        "email": "token@example.com",
        "password": "testpassword123"
    })

    # Login and get access token
    login_response = client.post("/login", data={
        "username": "token@example.com",
        "password": "testpassword123"
    })

    token = login_response.json()["access_token"]

    # Access protected endpoint using token
    response = client.get(
        "/posts/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_no_token_access(client):
    response = client.get("/posts/")

    assert response.status_code == 401
