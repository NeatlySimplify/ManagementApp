import pytest
import pytest_asyncio
import uuid
import datetime
from decimal import Decimal
from faker import Faker
from .test_utils import authenticated_user, client, test_entity

fake = Faker()


class TestEntityEndpoints:
    """Test the entity endpoints."""

    @pytest.mark.asyncio
    async def test_create_get_update_delete_entity(self, client, authenticated_user):
        """Test the complete entity CRUD operations."""
        today = datetime.date.today()

        # Create entity
        entity_data = {
            "email": fake.email(),
            "type_entity": fake.random_element(["Person", "Company", "Institution"]),
            "id_type": fake.random_element(["SSN", "EIN", "Passport"]),
            "govt_id": str(fake.random_number(digits=9)),
            "name": fake.name(),
            "sex": fake.random_element(["Male", "Female", "Other"]),
            "relationship_status": fake.random_element(["Single", "Married", "Divorced"]),
            "birth": (today - datetime.timedelta(days=fake.random_int(min=7000, max=25000))).isoformat(),
            "status": fake.boolean(),
            "notes":{
                "Occupation": fake.job(),
                "Notes": fake.paragraph()
            }
        }

        create_response = await client.post(
            "/api/entity/",
            cookies=authenticated_user.get_auth_cookies(),
            json=entity_data
        )

        if create_response.status_code != 200:
            print(f"Create response status: {create_response.status_code}")
            print(f"Create response body: {create_response.text}")

        assert create_response.status_code == 200
        assert create_response.json()["status"] == "success"

        # Get the entity_id from the response
        entity = create_response.json()["result"]
        entity_id = entity["id"]

        # Get entity details
        get_response = await client.get(
            f"/api/entity/{entity_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        if get_response.status_code != 200:
            print(f"Get response status: {get_response.status_code}")
            print(f"Get response body: {get_response.text}")

        assert get_response.status_code == 200
        get_data = get_response.json()["result"]
        assert get_data["email"] == entity_data["email"]
        assert get_data["type_entity"] == entity_data["type_entity"]
        assert get_data["id_type"] == entity_data["id_type"]
        assert get_data["govt_id"] == entity_data["govt_id"]
        assert get_data["name"] == entity_data["name"]
        assert get_data["sex"] == entity_data["sex"]
        assert get_data["relationship_status"] == entity_data["relationship_status"]
        assert get_data["status"] == entity_data["status"]
        # Verify all details match
        assert len(get_data["notes"]) == len(entity_data["notes"])

        # Update entity
        update_data = {
            "id": entity_id,
            "email": fake.email(),
            "type_entity": fake.random_element(["Organization", "Government"]),
            "id_type": fake.random_element(["TIN", "VAT"]),
            "govt_id": str(fake.random_number(digits=8)),
            "name": fake.company(),
            "sex": fake.random_element(["Male", "Female", "Other"]),
            "relationship_status": fake.random_element(["Partnered", "Separated"]),
            "birth": (today - datetime.timedelta(days=fake.random_int(min=5000, max=20000))).isoformat(),
            "status": not entity_data["status"],
            "notes": {
                "Industry": fake.word(),
                "Updated Notes": fake.paragraph()
            }
        }
        update_response = await client.put(
            "/api/entity/",
            cookies=authenticated_user.get_auth_cookies(),
            json=update_data
        )

        assert update_response.status_code == 200
        assert update_response.json()["status"] == "success"

        # Verify update
        get_updated_response = await client.get(
            f"/api/entity/{entity_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        assert get_updated_response.status_code == 200
        updated_data = get_updated_response.json()["result"]
        assert updated_data["email"] == update_data["email"]
        assert updated_data["type_entity"] == update_data["type_entity"]
        assert updated_data["id_type"] == update_data["id_type"]
        assert updated_data["govt_id"] == update_data["govt_id"]
        assert updated_data["name"] == update_data["name"]
        assert updated_data["status"] == update_data["status"]

        # Delete entity
        delete_response = await client.delete(
            f"/api/entity/{entity_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        assert delete_response.status_code == 200
        assert delete_response.json()["status"] == "success"

        # Verify deletion
        get_deleted_response = await client.get(
            f"/api/entity/{entity_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        assert get_deleted_response.status_code != 200

    @pytest.mark.asyncio
    async def test_create_get_update_delete_address(self, client, authenticated_user, test_entity):
        """Test the complete address CRUD operations."""
        entity_id, _ = test_entity

        # Create address
        address_data = {
            "entity": entity_id,
            "state": fake.state(),
            "city": fake.city(),
            "district": fake.word(),
            "street": fake.street_name(),
            "number": fake.random_number(digits=4),
            "complement": fake.secondary_address(),
            "postal": fake.postcode()
        }

        create_response = await client.post(
            "/api/entity/address",
            cookies=authenticated_user.get_auth_cookies(),
            json=address_data
        )

        assert create_response.status_code == 200
        assert create_response.json()["status"] == "success"

        # Get the address_id from the response
        address = create_response.json()["result"]



        # Verify address was created by getting entity with addresses
        get_entity_response = await client.get(
            f"/api/entity/{entity_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        assert get_entity_response.status_code == 200
        entity_data = get_entity_response.json()["result"]


        # Check if addresses are included in entity response
        if "addresses" in entity_data:
            addresses = entity_data["addresses"]
            created_address = next((addr for addr in addresses if addr["id"] == address["id"]), None)
            assert created_address is not None
            assert created_address["state"] == address_data["state"]
            assert created_address["city"] == address_data["city"]

        # Update address
        update_address_data = {
            "id": address["id"],
            "state": fake.state(),
            "city": fake.city(),
            "district": fake.word(),
            "street": fake.street_name(),
            "number": fake.random_number(digits=3),
            "complement": fake.secondary_address(),
            "postal": fake.postcode()
        }

        update_response = await client.put(
            "/api/entity/address",
            cookies=authenticated_user.get_auth_cookies(),
            json=update_address_data
        )

        assert update_response.status_code == 200
        assert update_response.json()["status"] == "success"

        # Delete address
        delete_response = await client.delete(
            f"/api/entity/{entity_id}/address/",
            cookies=authenticated_user.get_auth_cookies(),
            params={"address": address["id"]}
        )

        assert delete_response.status_code == 200
        assert delete_response.json()["status"] == "success"


    @pytest.mark.asyncio
    async def test_create_get_update_delete_contact(self, client, authenticated_user, test_entity):
        """Test the complete contact CRUD operations."""
        entity_id, _ = test_entity

        # Create contact
        contact_data = {
            "entity": entity_id,
            "number": {str(fake.random_element(["Mobile", "Work", "Home"])): fake.phone_number()},
            "email": fake.email(),
            "name": fake.name(),
            "notes": {
                "Preferred": str(fake.boolean()),
                "Notes": fake.sentence()
            }
        }

        create_response = await client.post(
            "/api/entity/contact",
            cookies=authenticated_user.get_auth_cookies(),
            json=contact_data
        )

        assert create_response.status_code == 200
        assert create_response.json()["status"] == "success"

        # Get the contact_id from the response
        created_contact = create_response.json()["result"]
        create_contact_id = created_contact["contact"]["id"]
        contact_id = create_contact_id

        # Verify contact was created by getting entity with contacts
        get_entity_response = await client.get(
            f"/api/entity/{entity_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        assert get_entity_response.status_code == 200
        entity_data = get_entity_response.json()["result"]

        # Check if contacts are included in entity response
        if "contacts" in entity_data:
            contacts = entity_data["contacts"]
            created_contact = next((cont for cont in contacts if cont["id"] == contact_id), None)
            assert created_contact is not None
            assert len(created_contact["number"]) == len(contact_data["number"])
            assert created_contact["email"] == contact_data["email"]
            assert created_contact["name"] == contact_data["name"]
        # Update contact
        update_contact_data = {
            "id": create_contact_id,
            "email": fake.email(),
            "name": fake.name(),
        }
        update_response = await client.put(
            "/api/entity/contact",
            cookies=authenticated_user.get_auth_cookies(),
            json=update_contact_data
        )


        assert update_response.status_code == 200
        assert update_response.json()["status"] == "success"

        # Delete contact
        delete_response = await client.delete(
            f"/api/entity/{entity_id}/contact/",
            cookies=authenticated_user.get_auth_cookies(),
            params={"contact": create_contact_id}
        )

        assert delete_response.status_code == 200
        assert delete_response.json()["status"] == "success"

    @pytest.mark.asyncio
    async def test_partial_update_entity(self, client, authenticated_user, test_entity):
        """Test partial update of entity."""
        entity_id, original_data = test_entity

        # Update only some fields
        partial_update = {
            "id": entity_id,
            "name": fake.company(),
            "status": not original_data["status"]
        }

        update_response = await client.put(
            "/api/entity/",
            cookies=authenticated_user.get_auth_cookies(),
            json=partial_update
        )

        assert update_response.status_code == 200
        assert update_response.json()["status"] == "success"

        # Verify partial update
        get_response = await client.get(
            f"/api/entity/{entity_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        assert get_response.status_code == 200
        updated_data = get_response.json()["result"]
        assert updated_data["name"] == partial_update["name"]
        assert updated_data["status"] == partial_update["status"]
        # Original data should remain unchanged
        assert updated_data["email"] == original_data["email"]
        assert updated_data["type_entity"] == original_data["type_entity"]

    @pytest.mark.asyncio
    async def test_unauthorized_access(self, client):
        """Test accessing entity endpoints without authentication."""
        # Try to get entity data without authentication
        random_id = str(uuid.uuid4())
        response = await client.get(f"/api/entity/{random_id}")
        assert response.status_code == 401

        # Try to create entity without authentication
        entity_data = {
            "email": fake.email(),
            "type_entity": "Person",
            "name": fake.name(),
            "status": True
        }

        create_response = await client.post("/api/entity/", json=entity_data)
        assert create_response.status_code == 401

        # Try to create address without authentication
        address_data = {
            "entity": random_id,
            "state": fake.state(),
            "city": fake.city()
        }

        address_response = await client.post("/api/entity/address", json=address_data)
        assert address_response.status_code == 401

        # Try to create contact without authentication
        contact_data = {
            "entity": random_id,
            "number": {"Mobile": fake.phone_number()},
            "email": fake.email()
        }

        contact_response = await client.post("/api/entity/contact", json=contact_data)
        assert contact_response.status_code == 401

    @pytest.mark.asyncio
    async def test_nonexistent_entity(self, client, authenticated_user):
        """Test operations on nonexistent entity."""
        # Try to get an entity that doesn't exist
        fake_id = str(uuid.uuid4())
        response = await client.get(
            f"/api/entity/{fake_id}",
            cookies=authenticated_user.get_auth_cookies()
        )

        # Should return an error (likely 404 or 400)
        assert response.status_code >= 400

        # Try to update a nonexistent entity
        update_data = {
            "id": fake_id,
            "name": fake.name(),
            "email": fake.email()
        }

        update_response = await client.put(
            "/api/entity/",
            cookies=authenticated_user.get_auth_cookies(),
            json=update_data
        )

        assert update_response.status_code >= 400

    @pytest.mark.asyncio
    async def test_invalid_entity_data(self, client, authenticated_user):
        """Test creating entity with invalid data."""
        # Missing required fields
        invalid_entity_data = {
            "email": fake.email()
            # Missing name, type, and other required fields
        }

        response = await client.post(
            "/api/entity/",
            cookies=authenticated_user.get_auth_cookies(),
            json=invalid_entity_data
        )

        assert response.status_code == 422  # Validation error

        # Invalid email format
        invalid_email_data = {
            "email": "not-an-email",
            "type_entity": "Person",
            "name": fake.name(),
            "status": True
        }

        response = await client.post(
            "/api/entity/",
            cookies=authenticated_user.get_auth_cookies(),
            json=invalid_email_data
        )

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_invalid_address_data(self, client, authenticated_user, test_entity):
        """Test creating address with invalid data."""
        entity_id, _ = test_entity

        # Missing required fields
        invalid_address_data = {
            "entity": entity_id
            # Missing state, city, and other required fields
        }

        response = await client.post(
            "/api/entity/address",
            cookies=authenticated_user.get_auth_cookies(),
            json=invalid_address_data
        )

        assert response.status_code == 422  # Validation error

        # Invalid entity UUID
        invalid_entity_data = {
            "entity": "not-a-valid-uuid",
            "state": fake.state(),
            "city": fake.city()
        }

        response = await client.post(
            "/api/entity/address",
            cookies=authenticated_user.get_auth_cookies(),
            json=invalid_entity_data
        )

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_invalid_contact_data(self, client, authenticated_user, test_entity):
        """Test creating contact with invalid data."""
        entity_id, _ = test_entity

        # Missing required fields
        invalid_contact_data = {
            "entity": entity_id
            # Missing number, email, and name
        }

        response = await client.post(
            "/api/entity/contact",
            cookies=authenticated_user.get_auth_cookies(),
            json=invalid_contact_data
        )

        assert response.status_code == 422  # Validation error

        # Invalid entity UUID
        invalid_entity_data = {
            "entity": "not-a-valid-uuid",
            "number": {
                "Mobile": fake.phone_number(),
            },
            "email": fake.email(),
            "name": fake.name()
        }

        response = await client.post(
            "/api/entity/contact",
            cookies=authenticated_user.get_auth_cookies(),
            json=invalid_entity_data
        )

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_create_address_for_nonexistent_entity(self, client, authenticated_user):
        """Test creating address for nonexistent entity."""
        fake_entity_id = str(uuid.uuid4())

        address_data = {
            "entity": fake_entity_id,
            "state": fake.state(),
            "city": fake.city(),
            "district": fake.word(),
            "street": fake.street_name(),
            "number": fake.random_number(digits=4),
            "complement": fake.secondary_address(),
            "postal": fake.postcode()
        }
        print(fake_entity_id)
        print(address_data["postal"])

        response = await client.post(
            "/api/entity/address",
            cookies=authenticated_user.get_auth_cookies(),
            json=address_data
        )
        print(response.json())


        # Should fail due to foreign key constraint
        assert response.status_code >= 400

    @pytest.mark.asyncio
    async def test_create_contact_for_nonexistent_entity(self, client, authenticated_user):
        """Test creating contact for nonexistent entity."""
        fake_entity_id = str(uuid.uuid4())

        contact_data = {
            "entity": fake_entity_id,
            "number": {
                "Mobile": fake.phone_number(),
            },
            "email": fake.email(),
            "name": fake.name(),
            "notes": {"Notes": "Test contact"}
        }

        response = await client.post(
            "/api/entity/contact",
            cookies=authenticated_user.get_auth_cookies(),
            json=contact_data
        )

        # Should fail due to foreign key constraint
        assert response.status_code >= 400

    @pytest.mark.asyncio
    async def test_entity_with_special_characters(self, client, authenticated_user):
        """Test creating entity with special characters and unicode."""
        today = datetime.date.today()

        entity_data = {
            "email": fake.email(),
            "type_entity": "Person",
            "id_type": "Passport",
            "govt_id": "ABC-123-456",
            "name": "José María Ñoño-Pérez",
            "sex": "Male",
            "relationship_status": "Single",
            "birth": (today - datetime.timedelta(days=10000)).isoformat(),
            "status": True,
            "notes":{
                "Occupation": "Software Engineer",
                "Notes": "Special chars: áéíóú ñ üç @#$%"
            }
        }

        create_response = await client.post(
            "/api/entity/",
            cookies=authenticated_user.get_auth_cookies(),
            json=entity_data
        )

        assert create_response.status_code == 200
        assert create_response.json()["status"] == "success"

        entity_id = create_response.json()["result"]["id"]

        # Verify the entity was created correctly
        get_response = await client.get(
            f"/api/entity/{entity_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        assert get_response.status_code == 200
        get_data = get_response.json()["result"]
        assert get_data["name"] == entity_data["name"]

        # Clean up
        await client.delete(
            f"/api/entity/{entity_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )
