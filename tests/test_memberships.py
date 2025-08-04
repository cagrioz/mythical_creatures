from typing import Dict, Any
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from uuid import uuid4

@pytest.fixture
def creature_and_realm(client: TestClient) -> Dict[str, str]:
    """
    Fixture to create a creature and a realm for testing memberships.
    """
    creature_response = client.post(
        "/creatures/",
        json={"name": "Dragon", "species": "Fire Drake"}
    )
    realm_response = client.post(
        "/realms/",
        json={"name": "Olympus"}
    )
    return {
        "creature_id": creature_response.json()["id"],
        "realm_id": realm_response.json()["id"]
    }

def test_create_membership(client: TestClient, creature_and_realm: Dict[str, str]) -> None:
    """
    Test creating a new membership between a creature and a realm.
    Should return 201 Created.
    """
    response = client.post(
        "/memberships/",
        json=creature_and_realm
    )
    assert response.status_code == status.HTTP_201_CREATED

def test_create_duplicate_membership(client: TestClient, creature_and_realm: Dict[str, str]) -> None:
    """
    Test creating a duplicate membership.
    Should return 400 Bad Request.
    """
    # Create first membership
    client.post("/memberships/", json=creature_and_realm)
    
    # Try to create duplicate
    response = client.post("/memberships/", json=creature_and_realm)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_create_membership_invalid_ids(client: TestClient) -> None:
    """
    Test creating a membership with invalid UUIDs.
    Should return 400 Bad Request.
    """
    response = client.post(
        "/memberships/",
        json={
            "creature_id": "not-a-uuid",
            "realm_id": "not-a-uuid"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_create_membership_non_existent_entities(client: TestClient) -> None:
    """
    Test creating a membership with non-existent creature/realm.
    Should return 404 Not Found.
    """
    response = client.post(
        "/memberships/",
        json={
            "creature_id": str(uuid4()),
            "realm_id": str(uuid4())
        }
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_membership(client: TestClient, creature_and_realm: Dict[str, str]) -> None:
    """
    Test deleting an existing membership.
    Should return 204 No Content.
    """
    # First create the membership
    client.post("/memberships/", json=creature_and_realm)
    
    # Then delete it
    response = client.delete(
        f"/memberships/?creature_id={creature_and_realm['creature_id']}&realm_id={creature_and_realm['realm_id']}"
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_delete_non_existent_membership(client: TestClient, creature_and_realm: Dict[str, str]) -> None:
    """
    Test deleting a non-existent membership.
    Should return 404 Not Found.
    """
    response = client.delete(
        f"/memberships/?creature_id={creature_and_realm['creature_id']}&realm_id={creature_and_realm['realm_id']}"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_realm_creatures(client: TestClient, creature_and_realm: Dict[str, str]) -> None:
    """
    Test getting all creatures in a realm.
    Should return 200 and a list of creatures.
    """
    # Create the membership
    client.post("/memberships/", json=creature_and_realm)
    
    # Get creatures in realm
    response = client.get(f"/realms/{creature_and_realm['realm_id']}/creatures/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == creature_and_realm["creature_id"]

def test_cascade_delete_realm(client: TestClient, creature_and_realm: Dict[str, str]) -> None:
    """
    Test that deleting a realm cascades to memberships.
    Should return 204 and remove all associated memberships.
    """
    # Create the membership
    client.post("/memberships/", json=creature_and_realm)
    
    # Delete the realm
    client.delete(f"/realms/{creature_and_realm['realm_id']}")
    
    # Check that the creature no longer has the realm
    response = client.get(f"/creatures/{creature_and_realm['creature_id']}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["realms"]) == 0

def test_cascade_delete_creature(client: TestClient, creature_and_realm: Dict[str, str]) -> None:
    """
    Test that deleting a creature cascades to memberships.
    Should return 204 and remove all associated memberships.
    """
    # Create the membership
    client.post("/memberships/", json=creature_and_realm)
    
    # Delete the creature
    client.delete(f"/creatures/{creature_and_realm['creature_id']}")
    
    # Check that the realm no longer has the creature
    response = client.get(f"/realms/{creature_and_realm['realm_id']}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["creatures"]) == 0
