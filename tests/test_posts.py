def test_create_post(client):
    # Step 1: Register a user
    client.post(
        "/users/",
        json={
            "email": "postuser@example.com",
            "password": "testpassword123"
        }
    )

    # Step 2: Log in
    login_response = client.post(
        "/login",
        data={
            "username": "postuser@example.com",
            "password": "testpassword123"
        }
    )

    token = login_response.json()["access_token"]

    # Step 3: Prepare authentication headers
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Step 4: Create a post
    response = client.post(
        "/posts/",
        json={
            "title": "My First Test Post",
            "content": "Learning FastAPI testing with Pytest",
            "published": True
        },
        headers=headers
    )

    # Step 5: Verify the response
    assert response.status_code == 201
    assert response.json()["title"] == "My First Test Post"
    assert response.json()["content"] == "Learning FastAPI testing with Pytest"
    assert response.json()["owner"]["email"] == "postuser@example.com"



def test_get_all_posts(client):
    # Step 1: Register a user
    client.post(
        "/users/",
        json={
            "email": "getposts@example.com",
            "password": "testpassword123"
        }
    )

    # Step 2: Login
    login_response = client.post(
        "/login",
        data={
            "username": "getposts@example.com",
            "password": "testpassword123"
        }
    )

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Step 3: Create a post
    client.post(
        "/posts/",
        json={
            "title": "Testing GET Posts",
            "content": "Checking whether posts can be retrieved",
            "published": True
        },
        headers=headers
    )

    # Step 4: Retrieve all posts
    response = client.get("/posts/", headers=headers)

    # Step 5: Verify the response
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["Post"]["title"] == "Testing GET Posts"


def test_get_one_post(client):
    # Step 1: Register a user
    client.post(
        "/users/",
        json={
            "email": "singlepost@example.com",
            "password": "testpassword123"
        }
    )

    # Step 2: Login
    login_response = client.post(
        "/login",
        data={
            "username": "singlepost@example.com",
            "password": "testpassword123"
        }
    )

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Step 3: Create a post
    create_response = client.post(
        "/posts/",
        json={
            "title": "My Specific Post",
            "content": "Testing retrieval by ID",
            "published": True
        },
        headers=headers
    )

    post_id = create_response.json()["id"]

    # Step 4: Retrieve that specific post
    response = client.get(
        f"/posts/{post_id}",
        headers=headers
    )

    # Step 5: Verify
    assert response.status_code == 200
    assert response.json()["Post"]["id"] == post_id
    assert response.json()["Post"]["title"] == "My Specific Post"


def test_update_post(client):
    # Step 1: Register a user
    client.post(
        "/users/",
        json={
            "email": "updatepost@example.com",
            "password": "testpassword123"
        }
    )

    # Step 2: Login
    login_response = client.post(
        "/login",
        data={
            "username": "updatepost@example.com",
            "password": "testpassword123"
        }
    )

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Step 3: Create a post
    create_response = client.post(
        "/posts/",
        json={
            "title": "Original Title",
            "content": "Original Content",
            "published": True
        },
        headers=headers
    )

    post_id = create_response.json()["id"]

    # Step 4: Update the post
    response = client.put(
        f"/posts/{post_id}",
        json={
            "title": "Updated Title",
            "content": "Updated Content",
            "published": True
        },
        headers=headers
    )

    # Step 5: Verify the update
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"
    assert response.json()["content"] == "Updated Content"


def test_delete_post(client):
    # Step 1: Register a user
    client.post(
        "/users/",
        json={
            "email": "deletepost@example.com",
            "password": "testpassword123"
        }
    )

    # Step 2: Login
    login_response = client.post(
        "/login",
        data={
            "username": "deletepost@example.com",
            "password": "testpassword123"
        }
    )

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Step 3: Create a post
    create_response = client.post(
        "/posts/",
        json={
            "title": "Post to Delete",
            "content": "This post will be deleted",
            "published": True
        },
        headers=headers
    )

    post_id = create_response.json()["id"]

    # Step 4: Delete the post
    response = client.delete(
        f"/posts/{post_id}",
        headers=headers
    )

    # Step 5: Verify deletion
    assert response.status_code == 204

    # Step 6: Confirm the post no longer exists
    get_response = client.get(
        f"/posts/{post_id}",
        headers=headers
    )

    assert get_response.status_code == 404


def test_unauthorized_user_get_posts(client):
    response = client.get("/posts/")

    assert response.status_code == 401


def test_update_other_users_post(client):
    # Step 1: Register User A
    client.post(
        "/users/",
        json={
            "email": "usera@example.com",
            "password": "testpassword123"
        }
    )

    # Step 2: Login as User A
    login_a = client.post(
        "/login",
        data={
            "username": "usera@example.com",
            "password": "testpassword123"
        }
    )

    token_a = login_a.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # Step 3: User A creates a post
    create_response = client.post(
        "/posts/",
        json={
            "title": "User A's Post",
            "content": "This belongs to User A",
            "published": True
        },
        headers=headers_a
    )

    post_id = create_response.json()["id"]

    # Step 4: Register User B
    client.post(
        "/users/",
        json={
            "email": "userb@example.com",
            "password": "testpassword123"
        }
    )

    # Step 5: Login as User B
    login_b = client.post(
        "/login",
        data={
            "username": "userb@example.com",
            "password": "testpassword123"
        }
    )

    token_b = login_b.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # Step 6: User B tries to update User A's post
    response = client.put(
        f"/posts/{post_id}",
        json={
            "title": "Hacked Title",
            "content": "Trying to modify someone else's post",
            "published": True
        },
        headers=headers_b
    )

    # Step 7: Verify access is forbidden
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized to perform requested action"


def test_delete_other_users_post(client):
    # Step 1: Register User A
    client.post(
        "/users/",
        json={
            "email": "deletea@example.com",
            "password": "testpassword123"
        }
    )

    # Step 2: Login as User A
    login_a = client.post(
        "/login",
        data={
            "username": "deletea@example.com",
            "password": "testpassword123"
        }
    )

    token_a = login_a.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # Step 3: User A creates a post
    create_response = client.post(
        "/posts/",
        json={
            "title": "User A's Post",
            "content": "This post belongs to User A",
            "published": True
        },
        headers=headers_a
    )

    post_id = create_response.json()["id"]

    # Step 4: Register User B
    client.post(
        "/users/",
        json={
            "email": "deleteb@example.com",
            "password": "testpassword123"
        }
    )

    # Step 5: Login as User B
    login_b = client.post(
        "/login",
        data={
            "username": "deleteb@example.com",
            "password": "testpassword123"
        }
    )

    token_b = login_b.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # Step 6: User B tries to delete User A's post
    response = client.delete(
        f"/posts/{post_id}",
        headers=headers_b
    )

    # Step 7: Verify deletion is forbidden
    assert response.status_code == 403

    # Step 8: Confirm User A's post still exists
    get_response = client.get(
        f"/posts/{post_id}",
        headers=headers_a
    )

    assert get_response.status_code == 200


def test_get_nonexistent_post(client):
    # Register a user
    client.post(
        "/users/",
        json={
            "email": "missingpost@example.com",
            "password": "testpassword123"
        }
    )

    # Login
    login_response = client.post(
        "/login",
        data={
            "username": "missingpost@example.com",
            "password": "testpassword123"
        }
    )

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Request a post that doesn't exist
    response = client.get("/posts/99999", headers=headers)

    # Verify 404 response
    assert response.status_code == 404
    assert response.json()["detail"] == "Post not found"


def test_update_nonexistent_post(client):
    # Step 1: Register a user
    client.post(
        "/users/",
        json={
            "email": "update_missing@example.com",
            "password": "testpassword123"
        }
    )

    # Step 2: Login
    login_response = client.post(
        "/login",
        data={
            "username": "update_missing@example.com",
            "password": "testpassword123"
        }
    )

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Step 3: Try updating a nonexistent post
    response = client.put(
        "/posts/99999",
        json={
            "title": "Updated Title",
            "content": "Updated Content",
            "published": True
        },
        headers=headers
    )

    # Step 4: Verify the response
    assert response.status_code == 404
    assert response.json()["detail"] == "Post with id 99999 not found"


def test_delete_nonexistent_post(client):
    # Step 1: Register a user
    client.post(
        "/users/",
        json={
            "email": "delete_missing@example.com",
            "password": "testpassword123"
        }
    )

    # Step 2: Login
    login_response = client.post(
        "/login",
        data={
            "username": "delete_missing@example.com",
            "password": "testpassword123"
        }
    )

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Step 3: Try deleting a nonexistent post
    response = client.delete(
        "/posts/99999",
        headers=headers
    )

    # Step 4: Verify the response
    assert response.status_code == 404
    assert response.json()["detail"] == "Post with id 99999 not found"
