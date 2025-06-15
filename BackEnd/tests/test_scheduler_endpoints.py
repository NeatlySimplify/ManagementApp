import pytest
import pytest_asyncio
import uuid
import datetime
from decimal import Decimal
from faker import Faker
from .test_utils import authenticated_user, client

fake = Faker()


class TestSchedulerEndpoints:
    """Test the scheduler endpoints."""

    @pytest.mark.asyncio
    async def test_create_get_update_delete_scheduler(self, client, authenticated_user):
        """Test the complete scheduler CRUD operations."""
        # Create a scheduler event
        today = datetime.date.today()
        start_time = datetime.time(10, 0)
        end_time = datetime.time(11, 0)

        data = {
            "type_entry": fake.random_element(["Meeting", "Appointment", "Deadline", "Reminder"]),
            "name": fake.sentence(nb_words=3),
            "status": fake.boolean(),
            "date": today.isoformat(),
            "beginning_time": start_time.isoformat(),
            "ending_time": end_time.isoformat(),
            "notes":{
                "Location": fake.address(),
                "Description": fake.paragraph(),
                "Priority": fake.random_element(["High", "Medium", "Low"])
            },
            "origin": None
        }

        create_response = await client.post(
            "/api/scheduler/",
            cookies=authenticated_user.get_auth_cookies(),
            json=data
        )
        print(data["notes"])

        assert create_response.status_code == 200
        assert create_response.json()["status"] == "success"

        # Get the scheduler_id from the response
        scheduler = create_response.json()["result"]
        scheduler_id = scheduler["id"]

        # Get scheduler event details
        get_response = await client.get(
            f"/api/scheduler/{scheduler_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        assert get_response.status_code == 200
        get_data = get_response.json()["result"]
        print(get_data["notes"])
        assert get_data["name"] == data["name"]
        assert get_data["type_entry"] == data["type_entry"]
        assert "date" in get_data
        assert "beginning_time" in get_data
        assert "ending_time" in get_data


        # Update scheduler event
        tomorrow = today + datetime.timedelta(days=1)
        new_start_time = datetime.time(14, 0)
        new_end_time = datetime.time(15, 30)

        update_data = {
            "id": scheduler_id,
            "name": fake.sentence(nb_words=4),
            "type_entry": fake.random_element(["Task", "Event", "Holiday"]),
            "status": not data["status"],
            "date": tomorrow.isoformat(),
            "beginning_time": new_start_time.isoformat(),
            "ending_time": new_end_time.isoformat(),
        }

        update_response = await client.put(
            "/api/scheduler/",
            cookies=authenticated_user.get_auth_cookies(),
            json=update_data
        )

        assert update_response.status_code == 200
        assert update_response.json()["status"] == "success"

        # Verify update
        get_updated_response = await client.get(
            f"/api/scheduler/{scheduler_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        assert get_updated_response.status_code == 200
        updated_data = get_updated_response.json()["result"]
        assert updated_data["name"] == update_data["name"]
        assert updated_data["type_entry"] == update_data["type_entry"]
        assert updated_data["status"] == update_data["status"]
        assert "date" in updated_data
        assert "beginning_time" in updated_data
        assert "ending_time" in updated_data
        # Compare details by checking each item
        assert len(updated_data["notes"]) == len(get_data["notes"])

        # Test with query parameters
        query_get_response = await client.get(
            f"/api/scheduler/{scheduler_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )
        assert query_get_response.status_code == 200

        # Delete scheduler event
        delete_response = await client.delete(
            f"/api/scheduler/{scheduler_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        assert delete_response.status_code == 200
        assert delete_response.json()["status"] == "success"

        # Verify deletion
        get_deleted_response = await client.get(
            f"/api/scheduler/{scheduler_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        assert get_deleted_response.status_code != 200

    @pytest.mark.asyncio
    async def test_partial_update_scheduler(self, client, authenticated_user):
        """Test partial update of scheduler event."""
        # Create a scheduler event first
        today = datetime.date.today()

        data = {
            "type_entry": fake.random_element(["Meeting", "Appointment"]),
            "name": fake.sentence(nb_words=3),
            "status": fake.boolean(),
            "date": today.isoformat(),
            "beginning_time": datetime.time(9, 0).isoformat(),
            "ending_time": datetime.time(10, 0).isoformat(),
            "notes": {
                "Description": fake.paragraph()
            },
            "origin": None
        }

        create_response = await client.post(
            "/api/scheduler/",
            cookies=authenticated_user.get_auth_cookies(),
            json=data
        )

        assert create_response.status_code == 200
        create_response = create_response.json()["result"]
        scheduler_id = create_response["id"]

        # Update only some fields
        partial_update = {
            "id": scheduler_id,
            "name": fake.sentence(nb_words=4),
            "status": not data["status"],
            "notes": {
                "Description": fake.paragraph(),
                "Location": fake.address()
            },
        }

        update_response = await client.put(
            "/api/scheduler/",
            cookies=authenticated_user.get_auth_cookies(),
            json=partial_update
        )

        assert update_response.status_code == 200
        update_response = update_response.json()
        assert update_response["status"] == "success"

        # Verify partial update
        get_response = await client.get(
            f"/api/scheduler/{scheduler_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        assert get_response.status_code == 200
        updated_data = get_response.json()["result"]
        assert updated_data["name"] == partial_update["name"]
        assert updated_data["status"] == partial_update["status"]
        assert updated_data["type_entry"] == data["type_entry"]

        assert updated_data["notes"]

        # Clean up
        await client.delete(
            f"/api/scheduler/{scheduler_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

    @pytest.mark.asyncio
    async def test_unauthorized_access(self, client):
        """Test accessing scheduler endpoints without authentication."""
        # Try to get scheduler data without authentication
        random_id = str(uuid.uuid4())
        response = await client.get(f"/api/scheduler/{random_id}")
        assert response.status_code == 401

        # Try to create scheduler without authentication
        scheduler_data = {
            "type_entry": "Meeting",
            "name": "Unauthorized test",
            "date": datetime.date.today().isoformat()
        }

        create_response = await client.post("/api/scheduler/", json=scheduler_data)
        assert create_response.status_code == 401

    @pytest.mark.asyncio
    async def test_nonexistent_scheduler(self, client, authenticated_user):
        """Test operations on nonexistent scheduler."""
        # Try to get a scheduler that doesn't exist
        fake_id = str(uuid.uuid4())
        response = await client.get(
            f"/api/scheduler/{fake_id}",
            cookies=authenticated_user.get_auth_cookies()
        )

        # Should return an error (likely 404 or 400)
        assert response.status_code >= 400

    @pytest.mark.asyncio
    async def test_invalid_scheduler_data(self, client, authenticated_user):
        """Test creating scheduler with invalid data."""
        # Missing required fields
        invalid_data = {
            "type_entry": "Meeting"
            # Missing name and date
        }

        response = await client.post(
            "/api/scheduler/",
            cookies=authenticated_user.get_auth_cookies(),
            json=invalid_data
        )

        assert response.status_code == 422  # Validation error

        # Invalid date format
        invalid_date_data = {
            "type_entry": "Meeting",
            "name": "Test Meeting",
            "date": "not-a-date",
            "status": True
        }

        response = await client.post(
            "/api/scheduler/",
            cookies=authenticated_user.get_auth_cookies(),
            json=invalid_date_data
        )

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_scheduler_with_origin(self, client, authenticated_user):
        """Test creating a scheduler event with an origin reference."""
        # Create a scheduler event
        today = datetime.date.today()
        start_time = datetime.time(10, 0)
        end_time = datetime.time(11, 0)
        origin_id = str(uuid.uuid4())  # Mock origin ID

        data = {
            "type_entry": fake.random_element(["Meeting", "Appointment"]),
            "name": fake.sentence(nb_words=3),
            "status": True,
            "date": today.isoformat(),
            "beginning_time": start_time.isoformat(),
            "ending_time": end_time.isoformat(),
            "origin": origin_id
        }

        create_response = await client.post(
            "/api/scheduler/",
            cookies=authenticated_user.get_auth_cookies(),
            json=data
        )

        assert create_response.status_code == 200
        assert create_response.json()["status"] == "success"

        # Get the scheduler_id from the response
        scheduler = create_response.json()["result"]
        scheduler_id = scheduler["id"]

        # Verify the event was created with the origin
        get_response = await client.get(
            f"/api/scheduler/{scheduler_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        assert get_response.status_code == 200
        get_data = get_response.json()["result"]
        assert "origin" in get_data

        # Clean up
        await client.delete(
            f"/api/scheduler/{scheduler_id}",
            cookies=authenticated_user.get_auth_cookies(),
        )
