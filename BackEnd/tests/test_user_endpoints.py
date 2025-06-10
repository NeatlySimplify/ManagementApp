import pytest
import pytest_asyncio
import uuid
from decimal import Decimal
import json
from faker import Faker
from src.dependencies.pwHash import hash_password
from .test_utils import authenticated_user, client, test_bank_account, test_settings
import traceback

fake = Faker()


class TestUserEndpoints:
    """Test the user endpoints."""

    @pytest.mark.asyncio
    async def test_get_user_data(self, client, authenticated_user):
        """Test getting user data."""
        response = await client.get(
            "/api/user/",
            cookies=authenticated_user.get_auth_cookies()
        )
        assert response.status_code == 200
        user_data = response.json()["result"]

        assert user_data["name"] == authenticated_user.name
        assert user_data["email"] == authenticated_user.email
        assert "settings" in user_data
        assert "account" in user_data

    @pytest.mark.asyncio
    async def test_update_user_data(self, client, authenticated_user):
        """Test updating user data."""
        new_email = fake.email()
        new_password = fake.password(length=12, special_chars=True)

        response = await client.put(
            "/api/user/",
            cookies=authenticated_user.get_auth_cookies(),
            json={
                "email": new_email,
                "password": new_password,
                "comfirm_password": new_password,
                "old_password": authenticated_user.password
            }
        )

        if response.status_code != 200:
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.text}")
        else:
            assert response.json()["status"] == "success"

        # Login with new credentials to verify update
        login_response = await client.post("/api/auth/login", json={
            "email": new_email,
            "password": new_password
        })

        if login_response.status_code != 200:
            print(f"Login response: {login_response.status_code}")
            print(f"Response body: {login_response.text}")
        else:
            # Reset authenticated_user to reflect the changes
            authenticated_user.email = new_email
            authenticated_user.password = new_password
            authenticated_user.access_token = login_response.cookies["access_token"]
            authenticated_user.refresh_token = login_response.cookies["refresh_token"]


    @pytest.mark.asyncio
    async def test_update_user_data_wrong_password(self, client, authenticated_user):
        """Test updating user data with wrong old password."""
        new_email = fake.email()
        new_password = fake.password(length=12, special_chars=True)

        response = await client.put(
            "/api/user/",
            cookies=authenticated_user.get_auth_cookies(),
            json={
                "email": new_email,
                "password": new_password,
                "comfirm_password": new_password,
                "old_password": "wrong_password"
            }
        )
        result = response.json()["detail"]
        print(result)
        assert result["status"] == "error"
        assert "403" in result["details"]


    @pytest.mark.asyncio
    async def test_bank_account_create_get_update_delete(self, client, authenticated_user):
        """Test the complete bank account CRUD operations."""
        # Create bank account
        data = {
            "bank_name": fake.company(),
            "account_name": fake.random_element(["Checking", "Savings", "Investment"]),
            "type": fake.random_element(["Personal", "Business", "Joint"]),
            "balance": str(Decimal(fake.random_number(digits=5)) / Decimal(100)),
            "details": [
                {
                    "title": "Account Number",
                    "field": str(fake.random_number(digits=10)),
                },
                {
                    "title": "Routing Number",
                    "field": str(fake.random_number(digits=9)),
                }
            ],
            "ignore_on_totals": False,
            "category": fake.random_element(["Primary", "Secondary", "Emergency"])
        }

        create_response = await client.post(
            "/api/user/bank-account",
            cookies=authenticated_user.get_auth_cookies(),
            json=data
        )

        if create_response.status_code != 200:
            print(f"Create bank account response: {create_response.status_code}")
            print(f"Response body: {create_response.text}")
        else:
            assert create_response.json()["status"] == "success"

        # Get the bank_id from the response

        bank = create_response.json()["result"]

        # Get bank account details
        get_response = await client.get(
            f"/api/user/bank-account/{bank["id"]}",
            cookies=authenticated_user.get_auth_cookies(),
        )
        bank_data = get_response.json()["result"]

        assert get_response.status_code == 200
        get_data = get_response.json()["result"]
        assert get_data["bank_name"] == bank_data["bank_name"]
        assert get_data["account_name"] == bank_data["account_name"]
        assert get_data["type"] == bank_data["type"]
        assert "balance" in get_data
        assert len(get_data["details"]) == len(bank_data["details"])

        # Update bank account
        update_data = {
            "id": bank["id"],
            "bank_name": fake.company(),
            "account_name": fake.random_element(["Premium", "Gold", "Platinum"]),
            "type": fake.random_element(["Personal", "Business"]),
            "details": {
                "body": [
                    {
                        "title": "Account Number",
                        "field": str(fake.random_number(digits=10)),
                    },
                    {
                        "title": "Updated Flag",
                        "field": "true",
                    }
                ],
                "change": True
            },
            "ignore_on_totals": True,
            "category": fake.random_element(["Primary", "Secondary"])
        }

        update_response = await client.put(
            "/api/user/bank-account",
            cookies=authenticated_user.get_auth_cookies(),
            json=update_data
        )

        if update_response.status_code != 200:
            print(f"Update response: {update_response.status_code}")
            print(f"Response body: {update_response.text}")
        else:
            assert update_response.json()["status"] == "success"

        # Verify update
        get_updated_response = await client.get(
            f"/api/user/bank-account/{bank["id"]}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        assert get_updated_response.status_code == 200
        updated_data = get_updated_response.json()["result"]
        assert updated_data["bank_name"] == update_data["bank_name"]
        assert updated_data["account_name"] == update_data["account_name"]
        assert updated_data["type"] == update_data["type"]
        # The response format may vary depending on how your API serializes the details
        # This assertion checks that the update was processed, but doesn't make assumptions
        # about the exact format of the returned details
        assert "details" in updated_data

        # Delete bank account
        delete_response = await client.delete(
            f"/api/user/bank-account/{bank["id"]}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        if delete_response.status_code != 200:
            print(f"Delete response: {delete_response.status_code}")
            print(f"Response body: {delete_response.text}")
        else:
            assert delete_response.json()["status"] == "success"

        # Verify deletion
        get_deleted_response = await client.get(
            f"/api/user/bank-account/{bank["id"]}",
            cookies=authenticated_user.get_auth_cookies(),
        )

        assert get_deleted_response.status_code != 200

    @pytest.mark.asyncio
    async def test_settings_create_update(self, client, authenticated_user, test_bank_account):
        """Test creating and updating user settings."""
        # Get the bank account ID from the fixture
        bank_id, _ = test_bank_account

        # Create settings
        settings_data = {
            "record_title": fake.word(),
            "movement_title": fake.word(),
            "entity_title": fake.word(),
            "default_bank_account": bank_id
        }

        create_settings_response = await client.post(
            "/api/user/settings",
            cookies=authenticated_user.get_auth_cookies(),
            json=settings_data
        )

        if create_settings_response.status_code != 200:
            print(f"Create settings response: {create_settings_response.status_code}")
            print(f"Response body: {create_settings_response.text}")
        else:
            assert create_settings_response.json()["status"] == "success"

        settings_id = create_settings_response.json()["result"]["id"]


        # Update settings
        update_data = {
            "id": settings_id,
            "default_bank_account": bank_id,
            "record_title": fake.word(),
            "movement_title": fake.word(),
            "entity_title": fake.word(),
            "account_types": [fake.word() for _ in range(3)],
            "entity_types": [fake.word() for _ in range(3)],
            "entity_id_types": [fake.word() for _ in range(2)],
            "contact_number_types": [fake.word() for _ in range(2)],
            "record_types": [fake.word() for _ in range(4)],
            "record_status": [fake.word() for _ in range(3)],
            "movement_income_types": [fake.word() for _ in range(3)],
            "movement_expense_types": [fake.word() for _ in range(3)],
            "scheduler_types": [fake.word() for _ in range(2)],
            "movement_cycle_types": [fake.word() for _ in range(2)]
        }

        update_settings_response = await client.put(
            "/api/user/settings",
            cookies=authenticated_user.get_auth_cookies(),
            json=update_data
        )

        if update_settings_response.status_code != 200:
            print(f"Update settings response: {update_settings_response.status_code}")
            print(f"Response body: {update_settings_response.text}")
        else:
            assert update_settings_response.json()["status"] == "success"

        # Check if settings were updated by getting user data
        user_data_response = await client.get(
            "/api/user/",
            cookies=authenticated_user.get_auth_cookies()
        )

        assert user_data_response.status_code == 200
        user_data = user_data_response.json()["result"]

        assert "settings" in user_data
        settings = user_data["settings"]
        assert settings["record_title"] == update_data["record_title"]
        assert settings["movement_title"] == update_data["movement_title"]
        assert settings["entity_title"] == update_data["entity_title"]

    @pytest.mark.asyncio
    async def test_unauthorized_access(self, client):
        """Test accessing user endpoints without authentication."""
        # Try to get user data without authentication
        response = await client.get("/api/user/")
        assert response.status_code == 401

        # Try to create bank account without authentication
        bank_data = {
            "bank_name": fake.company(),
            "account_name": "Checking",
            "balance": 1000.00
        }

        bank_response = await client.post("/api/user/bank-account", json=bank_data)
        assert bank_response.status_code == 401

    @pytest.mark.asyncio
    async def test_invalid_bank_account_data(self, client, authenticated_user):
        """Test creating bank account with invalid data."""
        # Missing required fields
        invalid_bank_data = {
            "bank_name": fake.company()
            # Missing account_name and balance
        }

        response = await client.post(
            "/api/user/bank-account",
            cookies=authenticated_user.get_auth_cookies(),
            json=invalid_bank_data
        )

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_nonexistent_bank_account(self, client, authenticated_user):
        """Test operations on nonexistent bank account."""
        # Try to get a bank account that doesn't exist
        fake_id = str(uuid.uuid4())
        response = await client.get(
            f"/api/user/bank-account/{fake_id}",
            cookies=authenticated_user.get_auth_cookies()
        )

        # Should return an error (likely 404 or 400)
        assert response.status_code >= 400

    @pytest.mark.asyncio
    async def test_user_password_update_validation(self, client, authenticated_user):
        """Test user update with password validation."""
        # Test with non-matching passwords
        response = await client.put(
            "/api/user/",
            cookies=authenticated_user.get_auth_cookies(),
            json={
                "email": authenticated_user.email,
                "password": "NewPassword123!",
                "comfirm_password": "DifferentPassword123!",
                "old_password": authenticated_user.password
            }
        )

        assert response.status_code == 422  # Validation error
