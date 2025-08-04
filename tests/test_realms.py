import pytest
from fastapi import status
from fastapi.testclient import TestClient
from uuid import uuid4

def test_create_realm(client: TestClient) -> None:
    """
    Test creating a new realm with valid data.
    Should return 200 and the created realm.
    """
    response = client.post(
        "/realms/",
        json={"name": "Olympus"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Olympus"
    assert "id" in data

def test_create_realm_invalid_data(client: TestClient) -> None:
    """
    Test creating a realm with missing required fields.
    Should return 422 Unprocessable Entity.
    """
    response = client.post(
        "/realms/",
        json={}  # Missing name
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_get_realm(client: TestClient) -> None:
    """
    Test retrieving a realm by ID.
    Should return 200 and the realm data with its creatures.
    """
    # First create a realm
    create_response = client.post(
        "/realms/",
        json={"name": "Atlantis"}
    )
    realm_id = create_response.json()["id"]
    
    # Then retrieve it
    response = client.get(f"/realms/{realm_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Atlantis"
    assert data["id"] == realm_id
    assert "creatures" in data
    assert isinstance(data["creatures"], list)

def test_get_realm_not_found(client: TestClient) -> None:
    """
    Test retrieving a non-existent realm.
    Should return 404 Not Found.
    """
    non_existent_id = str(uuid4())
    response = client.get(f"/realms/{non_existent_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_realm(client: TestClient) -> None:
    """
    Test updating an existing realm.
    Should return 200 and the updated realm data.
    """
    # First create a realm
    create_response = client.post(
        "/realms/",
        json={"name": "Olympus"}
    )
    realm_id = create_response.json()["id"]
    
    # Then update it
    response = client.put(
        f"/realms/{realm_id}",
        json={"name": "Mount Olympus"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Mount Olympus"
    assert data["id"] == realm_id

def test_delete_realm(client: TestClient) -> None:
    """
    Test deleting an existing realm.
    Should return 204 No Content and the realm should no longer exist.
    """
    # First create a realm
    create_response = client.post(
        "/realms/",
        json={"name": "Olympus"}
    )
    realm_id = create_response.json()["id"]
    
    # Then delete it
    response = client.delete(f"/realms/{realm_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify it's gone
    get_response = client.get(f"/realms/{realm_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_list_realms(client: TestClient) -> None:
    """
    Test listing all realms with pagination.
    Should return 200 and a list of realms.
    """
    # Create multiple realms
    realms = [
        {"name": "Olympus"},
        {"name": "Atlantis"},
        {"name": "Avalon"}
    ]
    for realm in realms:
        client.post("/realms/", json=realm)
    
    # Test pagination
    response = client.get("/realms/?skip=1&limit=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2  # Should return only 2 realms
