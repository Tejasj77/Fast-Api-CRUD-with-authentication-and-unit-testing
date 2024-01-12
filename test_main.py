from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

# Replace these values with actual test data
test_user = {"username": "testuser", "hashed_password": "testpassword"}

def test_create_user():
    response = client.post("/users/", json=test_user)
    assert response.status_code == 201
    assert response.json()["username"] == test_user["username"]

def test_read_user():
    # Create a user to test reading
    create_response = client.post("/users/", json=test_user)
    created_user = create_response.json()
   
    # Retrieve the user using the created ID
    response = client.get(f"/users/{created_user['id']}")
    assert response.status_code == 200
    assert response.json()["username"] == test_user["username"]

def test_update_user():
    # Create a user to test updating
    create_response = client.post("/users/", json=test_user)
    created_user = create_response.json()

    # Update the user's data
    new_data = {"username": "newusername", "password": "newpassword"}
    response = client.put(f"/users/{created_user['id']}", json=new_data)
    assert response.status_code == 200
    assert response.json()["username"] == new_data["username"]

def test_delete_user():
    # Create a user to test deleting
    create_response = client.post("/users/", json=test_user)
    created_user = create_response.json()

    # Delete the user
    response = client.delete(f"/users/{created_user['id']}")
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}

# JWT Authentication Test Cases

def test_get_token():
    response = client.post("/token", data={"username": test_user["username"], "password": test_user["password"]})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_access_protected_endpoint():
    # Get the access token
    token_response = client.post("/token", data={"username": test_user["username"], "password": test_user["password"]})
    access_token = token_response.json()["access_token"]

    # Access a protected endpoint with the token
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["username"] == test_user["username"]