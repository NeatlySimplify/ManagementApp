# ruff: noqa: F811
import pytest
import pytest_asyncio
import uuid
import datetime
from decimal import Decimal
from faker import Faker
from .test_utils import authenticated_user, client, test_entity, test_scheduler, test_bank_account, test_movement

fake = Faker()


class TestRecordEndpoints:
    """Test the record endpoints."""

    @pytest.mark.asyncio
    async def test_create_get_update_delete_record(self, client, authenticated_user, test_entity):
        """Test the complete record CRUD operations."""
        # Get entity ID from fixture - this creates a real entity in the database
        # The test_entity fixture makes an actual API call to create an entity
        # This is necessary because record creation checks if the entity exists in the database
        entity_id, _ = test_entity

        def record_stub(entity: str | None = None, record: str | None = None):
            if entity:
                return {
                    "name": fake.sentence(nb_words=3),
                    "id_service": f"REC-{fake.random_number(digits=6)}",
                    "active": True,
                    "status": fake.random_element(["Pending", "Completed", "Canceled"]),
                    "type_tag": fake.random_element(["Invoice", "Receipt", "Contract", "Statement"]),
                    "value": str(Decimal(fake.random_number(digits=5)) / Decimal(100)),
                    "notes": {"Note": fake.paragraph(), "Reference": str(fake.uuid4()), "Category": fake.random_element(["Business", "Personal", "Education"])},
                    "entity": entity  # Entity is required - record must be associated with a client/organization
                }
            else:
                return {
                    "id": record,
                    "name": fake.sentence(nb_words=3),
                    "id_service": f"REC-{fake.random_number(digits=6)}",
                    "active": True,
                    "status": fake.random_element(["Pending", "Completed", "Canceled"]),
                    "type_tag": fake.random_element(["Invoice", "Receipt", "Contract", "Statement"]),
                    "value": str(Decimal(fake.random_number(digits=5)) / Decimal(100)),
                    "notes": {},
                }
        data = record_stub(entity=entity_id)
        create_response = await client.post(
            "/api/record/",
            cookies=authenticated_user.get_auth_cookies(),
            json=data
        )

        assert create_response.status_code == 200
        assert create_response.json()["status"] == "success"

        # Get the record_id from the response
        record = create_response.json()["result"]
        record_id = record["id"]

        # Get record details
        get_response = await client.get(
            f"/api/record/{record_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        assert get_response.status_code == 200
        get_data = get_response.json()["result"]
        assert get_data["name"] == data["name"]
        assert get_data["id_service"] == data["id_service"]
        assert get_data["active"] == data["active"]
        assert get_data["status"] == data["status"]
        assert get_data["type_tag"] == data["type_tag"]
        assert Decimal(get_data["str_value"]) == Decimal(data["value"])
        # Verify details structure
        assert len(get_data["notes"]) == len(data["notes"])
        assert len(get_data["entity"]) > 0
        assert get_data["entity"][0]["id"] == entity_id

        # Update record
        update_data = record_stub(record=record_id)
        update_response = await client.put(
            "/api/record/",
            cookies=authenticated_user.get_auth_cookies(),
            json=update_data
        )

        assert update_response.status_code == 200
        assert update_response.json()["id"]

        # Verify update
        get_updated_response = await client.get(
            f"/api/record/{record_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        assert get_updated_response.status_code == 200
        updated_data = get_updated_response.json()["result"]
        assert updated_data["name"] == update_data["name"]
        assert updated_data["id_service"] == update_data["id_service"]
        assert updated_data["active"] == update_data["active"]
        assert updated_data["status"] == update_data["status"]
        assert updated_data["type_tag"] == update_data["type_tag"]
        assert Decimal(updated_data["str_value"]) == Decimal(update_data["value"])
        assert len(updated_data["entity"]) > 0
        assert updated_data["entity"][0]["id"] == entity_id

        # Delete record
        delete_response = await client.delete(
            f"/api/record/{record_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        assert delete_response.status_code == 200
        assert delete_response.json()["status"] == "success"

        # Verify deletion
        get_deleted_response = await client.get(
            f"/api/record/{record_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        assert get_deleted_response.status_code != 200

    @pytest.mark.asyncio
    async def test_partial_update_record(self, client, authenticated_user, test_entity):
        """Test partial update of record."""
        # Get a real entity from the database - created through the fixture
        entity_id, _ = test_entity

        # Create a record first - note entity is required
        data = {
            "name": fake.sentence(nb_words=3),
            "id_service": f"REC-{fake.random_number(digits=6)}",
            "active": True,
            "status": fake.random_element(["Pending", "Completed"]),
            "type_tag": fake.random_element(["Invoice", "Receipt"]),
            "value": str(Decimal(fake.random_number(digits=5)) / Decimal(100)),
            "notes": {
                "Note": fake.paragraph()
            },
            "entity": entity_id  # Entity is required - represents the client/organization
        }
        print("On create\n")
        print("Record data: ", data)
        create_response = await client.post(
            "/api/record/",
            cookies=authenticated_user.get_auth_cookies(),
            json=data
        )

        assert create_response.status_code == 200
        record_id = create_response.json()["result"]["id"]

        # Update only some fields
        partial_update = {
            "id": record_id,
            "name": fake.sentence(nb_words=4),
            "active": False,
            "notes": { "Note": fake.paragraph(), "Additional Info": fake.sentence()},
        }
        print("On update\n")
        print("Entity: ", entity_id)
        print("Record data: ", partial_update)
        update_response = await client.put(
            "/api/record/",
            cookies=authenticated_user.get_auth_cookies(),
            json=partial_update
        )

        assert update_response.status_code == 200
        assert update_response.json()["id"]

        # Verify partial update
        get_response = await client.get(
            f"/api/record/{record_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        assert get_response.status_code == 200
        updated_data = get_response.json()["result"]
        assert updated_data["name"] == partial_update["name"]
        assert updated_data["active"] == partial_update["active"]
        assert updated_data["type_tag"] == data["type_tag"]  # This should remain unchanged

        # Clean up
        await client.delete(
            f"/api/record/{record_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

    @pytest.mark.asyncio
    async def test_link_unlink_event(self, client, authenticated_user, test_entity, test_scheduler):
        """Test linking and unlinking a scheduler event to a record."""
        # Get real entity and scheduler created in the database through fixtures
        entity_id, _ = test_entity
        scheduler_id, _ = test_scheduler

        # Create a record with an entity (required)
        record_data = {
            "name": fake.sentence(nb_words=3),
            "id_service": f"REC-{fake.random_number(digits=6)}",
            "active": True,
            "status": "Active",
            "type_tag": "Invoice",
            "value": str(Decimal(fake.random_number(digits=5)) / Decimal(100)),
            "notes": {"Note": fake.paragraph()},
            "entity": entity_id  # Required - record must be associated with a client/organization
        }

        record_response = await client.post(
            "/api/record/",
            cookies=authenticated_user.get_auth_cookies(),
            json=record_data
        )

        assert record_response.status_code == 200
        record_id = record_response.json()["result"]["id"]

        # Link event to record
        link_response = await client.put(
            f"/api/record/{record_id}/add-event/?event={scheduler_id}",
            cookies=authenticated_user.get_auth_cookies()
        )

        assert link_response.status_code == 200
        assert link_response.json()["status"] == "success"

        # Verify link
        get_response = await client.get(
            f"/api/record/{record_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        assert get_response.status_code == 200
        record_data = get_response.json()["result"]
        assert "event" in record_data
        assert any(event["id"] == scheduler_id for event in record_data["event"])

        # Unlink event from record
        unlink_response = await client.put(
            f"/api/record/{record_id}/del-event/?event={scheduler_id}",
            cookies=authenticated_user.get_auth_cookies()
        )

        assert unlink_response.status_code == 200
        assert unlink_response.json()["status"] == "success"

        # Verify unlink
        get_response_after_unlink = await client.get(
            f"/api/record/{record_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        assert get_response_after_unlink.status_code == 200
        record_data_after_unlink = get_response_after_unlink.json()["result"]
        assert not any(event["id"] == scheduler_id for event in record_data_after_unlink["event"])

        # Clean up
        await client.delete(
            f"/api/record/{record_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

    @pytest.mark.asyncio
    async def test_link_unlink_entity(self, client, authenticated_user, test_entity):
        # Test linking and unlinking an additional entity to a record.
        entity_id, _ = test_entity

        # Create another real entity in the database for linking (e.g., another client or organization involved in the record)
        # Note: Entity creation endpoint has changed from /api/entity/create to /api/entity/
        another_entity_data = {
            "email": fake.email(),
            "type_entity": "Person",
            "id_type": "ID",
            "govt_id": str(fake.random_number(digits=9)),
            "name": fake.name(),
            "status": True
        }

        another_entity_response = await client.post(
            "/api/entity/",
            cookies=authenticated_user.get_auth_cookies(),
            json=another_entity_data
        )

        assert another_entity_response.status_code == 200
        another_entity_id = another_entity_response.json()["result"]["id"]

        # Create a record with the first entity - a record must have at least one entity
        # The system verifies that this entity exists in the database during record creation
        record_data = {
            "name": fake.sentence(nb_words=3),
            "id_service": f"REC-{fake.random_number(digits=6)}",
            "active": True,
            "status": "Active",
            "type_tag": "Invoice",  # Type of service/action
            "value": str(Decimal(fake.random_number(digits=5)) / Decimal(100)),  # Financial value
            "notes": {"Notes": fake.paragraph()},
            "entity": entity_id  # Primary client/organization (required and must exist in DB)
        }

        record_response = await client.post(
            "/api/record/",
            cookies=authenticated_user.get_auth_cookies(),
            json=record_data
        )

        assert record_response.status_code == 200
        record_id = record_response.json()["result"]["id"]

        # Link the second entity to the record
        link_response = await client.put(
            f"/api/record/{record_id}/add-entity/?entity={another_entity_id}",
            cookies=authenticated_user.get_auth_cookies()
        )

        assert link_response.status_code == 200
        assert link_response.json()["status"] == "success"

        # Verify the link
        get_response = await client.get(
            f"/api/record/{record_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        assert get_response.status_code == 200
        record_data = get_response.json()["result"]
        entity_ids = [entity["id"] for entity in record_data["entity"]]
        assert entity_id in entity_ids
        assert another_entity_id in entity_ids

        # Unlink the second entity
        unlink_response = await client.put(
            f"/api/record/{record_id}/del-entity/?entity={another_entity_id}",
            cookies=authenticated_user.get_auth_cookies()
        )

        assert unlink_response.status_code == 200
        assert unlink_response.json()["status"] == "success"

        # Verify the unlink
        get_after_unlink = await client.get(
            f"/api/record/{record_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        assert get_after_unlink.status_code == 200
        record_after_unlink = get_after_unlink.json()["result"]
        entity_ids_after = [entity["id"] for entity in record_after_unlink["entity"]]
        assert entity_id in entity_ids_after  # First entity should still be there
        assert another_entity_id not in entity_ids_after  # Second entity should be removed

        # Clean up
        await client.delete(
            f"/api/record/{record_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        await client.delete(
            f"/api/entity/{another_entity_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

    @pytest.mark.asyncio
    async def test_link_unlink_movement(self, client, authenticated_user, test_movement):
        """Test linking and unlinking a movement to a record."""
        # Get the pre-created movement, its data, and the record it's linked to
        movement_id, movement_data, record_id = test_movement

        # The movement is already linked to the record from the fixture,
        # so we first unlink it to test both operations
        unlink_response = await client.put(
            f"/api/record/{record_id}/del-movement/?movement={movement_id}",
            cookies=authenticated_user.get_auth_cookies()
        )

        assert unlink_response.status_code == 200
        assert unlink_response.json()["status"] == "success"

        # Now link it back
        link_response = await client.put(
            f"/api/record/{record_id}/add-movement/?movement={movement_id}",
            cookies=authenticated_user.get_auth_cookies()
        )

        assert link_response.status_code == 200
        assert link_response.json()["status"] == "success"

        # Verify the link
        get_record_response = await client.get(
            f"/api/record/{record_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        assert get_record_response.status_code == 200
        record_data = get_record_response.json()["result"]
        print(record_data["movement"])
        movement_ids = [movement["id"] for movement in record_data["movement"]]
        assert movement_id in movement_ids

        # Unlink again for verification
        unlink_response = await client.put(
            f"/api/record/{record_id}/del-movement/?movement={movement_id}",
            cookies=authenticated_user.get_auth_cookies()
        )

        assert unlink_response.status_code == 200
        assert unlink_response.json()["status"] == "success"

        # Verify the unlink
        get_record_response = await client.get(
            f"/api/record/{record_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        assert get_record_response.status_code == 200
        record_data = get_record_response.json()["result"]
        movement_ids = [movement["id"] for movement in record_data["movement"]]
        assert movement_id not in movement_ids

    @pytest.mark.asyncio
    async def test_unauthorized_access(self, client):
        """Test accessing record endpoints without authentication."""
        # Try to get record data without authentication
        random_id = str(uuid.uuid4())
        response = await client.get(f"/api/record/{random_id}")
        assert response.status_code == 401

        # Try to create record without authentication
        record_data = {
            "name": "Test Record",
            "active": True,
            "type_tag": "Invoice",  # Type of service/action
            "value": "100.00",   # Financial value
            "entity": str(uuid.uuid4())  # Required client/organization
        }

        create_response = await client.post("/api/record/", json=record_data)
        assert create_response.status_code == 401

    @pytest.mark.asyncio
    async def test_nonexistent_record(self, client, authenticated_user):
        """Test operations on nonexistent record."""
        # Try to get a record that doesn't exist
        fake_id = str(uuid.uuid4())
        response = await client.get(
            f"/api/record/{fake_id}",
            cookies=authenticated_user.get_auth_cookies()
        )

        # Should return an error (likely 404 or 400)
        assert response.status_code >= 400

    @pytest.mark.asyncio
    async def test_invalid_record_data(self, client, authenticated_user, test_entity):
        """Test creating record with invalid data."""
        entity_id, _ = test_entity

        # Missing required fields
        invalid_data = {
            "name": "Test Record",
            # Missing active, type, value
            "entity": entity_id
        }

        response = await client.post(
            "/api/record/",
            cookies=authenticated_user.get_auth_cookies(),
            json=invalid_data
        )

        assert response.status_code == 422  # Validation error

        # Missing entity field - entity is required as records must be associated with a client/organization
        # The database checks for both the existence of the entity field and whether that entity exists in the DB
        invalid_entity_missing = {
            "name": "Test Record",
            "active": True,
            "type_tag": "Invoice",
            "value": "100.00"
            # No entity provided
        }

        response = await client.post(
            "/api/record/",
            cookies=authenticated_user.get_auth_cookies(),
            json=invalid_entity_missing
        )

        assert response.status_code == 422  # Validation error

        # Invalid entity ID format - must be a valid UUID even though entity validation occurs after format validation
        invalid_entity_data = {
            "name": "Test Record",
            "active": True,
            "type_tag": "Invoice",
            "value": "100.00",
            "entity": "not-a-valid-uuid"  # Entity must be a valid UUID format
        }

        response = await client.post(
            "/api/record/",
            cookies=authenticated_user.get_auth_cookies(),
            json=invalid_entity_data
        )

        assert response.status_code == 422  # Validation error
