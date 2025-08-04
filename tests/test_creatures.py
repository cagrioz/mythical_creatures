from typing import Dict, Any
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from uuid import uuid4

def test_create_creature(client: TestClient) -> None:
    """
    Test creating a new creature with valid data.
    Should return 200 and the created creature.
    """
    response = client.post(
        "/creatures/",
        json={"name": "Dragon", "species": "Fire Drake"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Dragon"
    assert data["species"] == "Fire Drake"
    assert "id" in data

def test_create_creature_invalid_data(client: TestClient) -> None:
    """
    Test creating a creature with missing required fields.
    Should return 422 Unprocessable Entity.
    """
    response = client.post(
        "/creatures/",
        json={"name": "Dragon"}  # Missing species
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_get_creature(client: TestClient) -> None:
    """
    Test retrieving a creature by ID.
    Should return 200 and the creature data.
    """
    # First create a creature
    create_response = client.post(
        "/creatures/",
        json={"name": "Phoenix", "species": "Immortal Bird"}
    )
    creature_id = create_response.json()["id"]
    
    # Then retrieve it
    response = client.get(f"/creatures/{creature_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Phoenix"
    assert data["species"] == "Immortal Bird"
    assert data["id"] == creature_id

def test_get_creature_not_found(client: TestClient) -> None:
    """
    Test retrieving a non-existent creature.
    Should return 404 Not Found.
    """
    non_existent_id = str(uuid4())
    response = client.get(f"/creatures/{non_existent_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_creature_invalid_uuid(client: TestClient) -> None:
    """
    Test retrieving a creature with invalid UUID format.
    Should return 400 Bad Request.
    """
    response = client.get("/creatures/not-a-uuid")
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_update_creature(client: TestClient) -> None:
    """
    Test updating an existing creature.
    Should return 200 and the updated creature data.
    """
    # First create a creature
    create_response = client.post(
        "/creatures/",
        json={"name": "Dragon", "species": "Fire Drake"}
    )
    creature_id = create_response.json()["id"]
    
    # Then update it
    response = client.put(
        f"/creatures/{creature_id}",
        json={"name": "Golden Dragon", "species": "Celestial Drake"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Golden Dragon"
    assert data["species"] == "Celestial Drake"
    assert data["id"] == creature_id

def test_delete_creature(client: TestClient) -> None:
    """
    Test deleting an existing creature.
    Should return 204 No Content and the creature should no longer exist.
    """
    # First create a creature
    create_response = client.post(
        "/creatures/",
        json={"name": "Dragon", "species": "Fire Drake"}
    )
    creature_id = create_response.json()["id"]
    
    # Then delete it
    response = client.delete(f"/creatures/{creature_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify it's gone
    get_response = client.get(f"/creatures/{creature_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_list_creatures(client: TestClient) -> None:
    """
    Test listing all creatures with pagination.
    Should return 200 and a list of creatures.
    """
    # Create multiple creatures
    creatures = [
        {"name": "Dragon", "species": "Fire Drake"},
        {"name": "Phoenix", "species": "Immortal Bird"},
        {"name": "Unicorn", "species": "Magical Horse"}
    ]
    for creature in creatures:
        client.post("/creatures/", json=creature)
    
    # Test pagination
    response = client.get("/creatures/?skip=1&limit=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2  # Should return only 2 creatures
