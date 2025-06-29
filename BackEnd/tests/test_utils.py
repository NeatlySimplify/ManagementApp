# basedpyright: reportOptionalSubscript: false
# ruff: noqa: F811, F401
import datetime
import uuid
from decimal import Decimal
from typing import Any

import jwt
import pytest_asyncio
from asgi_lifespan import LifespanManager
from faker import Faker
from httpx import ASGITransport, AsyncClient

from src.main import app
from src.settings import get_settings

fake = Faker()
settings = get_settings()


@pytest_asyncio.fixture
async def client():
    """Create a test client for the app."""
    async with LifespanManager(app, startup_timeout=20):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client


class TestUser:
    """Reusable class for managing test user data and authentication."""

    def __init__(self):
        self.email = fake.email()
        self.password = fake.password(length=12, special_chars=True)
        self.name = fake.name()
        self.user_id = None
        self.access_token = None
        self.refresh_token = None
        self.type_user="is_individual"

    def get_auth_cookies(self):
        """Return the authentication cookies for requests."""
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token
        }

    def get_token_payload(self):
        """Decode and return the token payload."""
        if not self.access_token:
            return None
        return jwt.decode(self.access_token, settings.secret, algorithms=[settings.algorithm])


@pytest_asyncio.fixture
async def authenticated_user(client):
    """Create and authenticate a test user, then clean up by logging out."""
    user = TestUser()

    try:
        # Register the user
        register_response = await client.post("/api/auth/register", json={
            "email": user.email,
            "password": user.password,
            "confirm_password": user.password,
            "name": user.name,
            "type_user": user.type_user
        })
        assert register_response.status_code == 200

        # Login to get tokens
        login_response = await client.post("/api/auth/login", json={
            "email": user.email,
            "password": user.password
        })
        assert login_response.status_code == 200

        user.access_token = login_response.cookies["access_token"]
        user.refresh_token = login_response.cookies["refresh_token"]

        # Extract user ID from the token
        payload: Any = user.get_token_payload()
        user.user_id = payload["sub"]

        yield user
    finally:
        # Logout the user
        if user.access_token: # Only attempt logout if user was authenticated
            try:
                await client.get(
                    "/api/auth/logout",
                    cookies=user.get_auth_cookies()
                )
            except Exception as e:
                print(f"Error logging out user during cleanup: {str(e)}")


class BankAccountData:
    """Helper class for bank account test data."""

    @staticmethod
    def generate_data():
        """Generate random bank account data."""
        random_number_in_range = fake.random_int(min=20000, max=1000000)
        return {
            "bank_name": fake.company(),
            "account_name": fake.random_element(["Checking", "Savings", "Investment"]),
            "type_tag": fake.random_element(["Personal", "Business", "Joint"]),
            "balance": str(Decimal(random_number_in_range) / Decimal(100)),
            "notes":{
                "Account Number": str(fake.random_number(digits=10)),
                "Routing Number": str(fake.random_number(digits=9))
            },
            "ignore_on_totals": False,
            "category_tag": fake.random_element(["Primary", "Secondary", "Emergency"])
        }


@pytest_asyncio.fixture
async def test_bank_account(client, authenticated_user):
    """Create a test bank account, yield its ID and data, then clean up.

    This fixture creates an actual bank account in the database.
    It cleans up the bank account afterwards.
    """
    bank_data = BankAccountData.generate_data()
    bank_id_to_yield = str(uuid.uuid4())  # Default to dummy if creation fails
    created_bank_id = None

    try:
        response = await client.post(
            "/api/user/bank-account",
            cookies=authenticated_user.get_auth_cookies(),
            json=bank_data
        )

        if response.status_code == 200:
            result = response.json()["result"]
            created_bank_id = result["id"]
            bank_id_to_yield = created_bank_id
            yield bank_id_to_yield, bank_data
        else:
            print(f"Failed to create bank account: {response.status_code}, {response.text}")
            yield bank_id_to_yield, bank_data  # Yield dummy ID
    except Exception as e:
        print(f"Exception during bank account creation: {str(e)}")
        yield bank_id_to_yield, bank_data  # Yield dummy ID
    finally:
        if created_bank_id:  # Only attempt delete if successfully created
            try:
                await client.delete(
                    f"/api/user/bank-account/{created_bank_id}",
                    cookies=authenticated_user.get_auth_cookies()
                )
            except Exception as e:
                print(f"Error deleting bank account {created_bank_id} during cleanup: {str(e)}")


@pytest_asyncio.fixture
async def test_bank_account_2(client, authenticated_user):
    """Create a test bank account, yield its ID and data, then clean up.

    This fixture creates an actual bank account in the database.
    It cleans up the bank account afterwards.
    """
    bank_data = BankAccountData.generate_data()
    bank_id_to_yield = str(uuid.uuid4())  # Default to dummy if creation fails
    created_bank_id = None

    try:
        response = await client.post(
            "/api/user/bank-account",
            cookies=authenticated_user.get_auth_cookies(),
            json=bank_data
        )

        if response.status_code == 200:
            result = response.json()["result"]
            created_bank_id = result["id"]
            bank_id_to_yield = created_bank_id
            yield bank_id_to_yield, bank_data
        else:
            print(f"Failed to create bank account: {response.status_code}, {response.text}")
            yield bank_id_to_yield, bank_data  # Yield dummy ID
    except Exception as e:
        print(f"Exception during bank account creation: {str(e)}")
        yield bank_id_to_yield, bank_data  # Yield dummy ID
    finally:
        if created_bank_id:  # Only attempt delete if successfully created
            try:
                await client.delete(
                    f"/api/user/bank-account/{created_bank_id}",
                    cookies=authenticated_user.get_auth_cookies()
                )
            except Exception as e:
                print(f"Error deleting bank account {created_bank_id} during cleanup: {str(e)}")



@pytest_asyncio.fixture
async def test_settings(client, authenticated_user, test_bank_account):
    """Create test settings and return its ID and data.

    This fixture requires a bank_account to be set as the default account.
    It uses the test_bank_account fixture to get a valid bank account ID.
    No specific cleanup for the settings entity itself is performed here.
    """
    bank_id, _ = test_bank_account # bank_id might be a dummy if test_bank_account failed

    settings_data = {
        "record_title": fake.word(),
        "movement_title": fake.word(),
        "entity_title": fake.word(),
        "default_bank_account": bank_id
    }
    settings_id_to_yield = str(uuid.uuid4())

    try:
        response = await client.post(
            "/api/user/settings",
            cookies=authenticated_user.get_auth_cookies(),
            json=settings_data
        )

        if response.status_code == 200:
            settings_id_to_yield = response.json()["result"]["id"]
            yield settings_id_to_yield, settings_data
        else:
            print(f"Failed to create settings: {response.status_code}, {response.text}")
            yield settings_id_to_yield, settings_data
    except Exception as e:
        print(f"Exception during settings creation: {str(e)}")
        yield settings_id_to_yield, settings_data
    # No specific finally block for settings deletion itself.


@pytest_asyncio.fixture
async def test_entity(client, authenticated_user):
    """Create a test entity, yield its ID and data, then clean up.

    This fixture creates an actual entity in the database.
    It cleans up the entity afterwards.
    """
    today = datetime.date.today()
    entity_data = {
        "email": fake.email(),
        "type_tag": fake.random_element(["Person", "Company", "Institution"]),
        "document_type": fake.random_element(["SSN", "EIN", "Passport"]),
        "document": str(fake.random_number(digits=9)),
        "name": fake.name(),
        "sex": fake.random_element(["Male", "Female", "Other"]),
        "relationship_status": fake.random_element(["Single", "Married", "Divorced"]),
        "birth": (
            today - datetime.timedelta(
                days=fake.random_int(min=7000, max=25000)
            )
        ).isoformat(),
        "status": fake.boolean(),
    }
    entity_id_to_yield = str(uuid.uuid4())
    created_entity_id = None

    try:
        response = await client.post(
            "/api/entity/",
            cookies=authenticated_user.get_auth_cookies(),
            json=entity_data
        )

        if response.status_code == 200:
            result = response.json()["result"]
            created_entity_id = result["id"]
            entity_id_to_yield = created_entity_id
            yield entity_id_to_yield, entity_data
        else:
            print(f"Failed to create entity: {response.status_code}, {response.text}")
            yield entity_id_to_yield, entity_data
    except Exception as e:
        print(f"Exception during entity creation: {str(e)}")
        yield entity_id_to_yield, entity_data
    finally:
        if created_entity_id:
            try:
                await client.delete(
                    f"/api/entity/{created_entity_id}",
                    cookies=authenticated_user.get_auth_cookies()
                )
            except Exception as e:
                print(f"Error deleting entity {created_entity_id} during cleanup: {str(e)}")


@pytest_asyncio.fixture
async def test_movement(client, authenticated_user, test_bank_account, test_entity):
    """Create a test movement and record, yield IDs and data, then clean up.

    This fixture requires both a bank_account and an entity.
    It cleans up the movement and its associated record afterwards.
    """
    bank_id, _ = test_bank_account
    entity_id, _ = test_entity
    today = datetime.date.today()

    # Default values to yield in case of failure
    movement_id_to_yield = str(uuid.uuid4())
    record_id_to_yield = str(uuid.uuid4())
    # Ensure movement_data_to_yield is always defined for the yield statement
    movement_data_to_yield = {
        "type_tag": "Expense", "name": "Dummy Movement", "parts": 1, "total": "0.00",
        "is_due": today.isoformat(), "payment_date": today.isoformat(),
        "bank_account": bank_id, "category_tag": "Dummy", "subcategory_tag": "Dummy",
        "status": False, "notes": {}, "cycle": "only", "record": record_id_to_yield
    }


    created_record_id = None
    created_movement_id = None

    try:
        # First create a record
        record_data = {
            "name": fake.sentence(nb_words=3),
            "id_service": f"REC-{fake.random_number(digits=6)}",
            "status": True,
            "optionalstatus": fake.random_element(["Pending", "Completed", "Canceled"]),
            "type_tag": fake.random_element(["Invoice", "Receipt"]),
            "value": str(Decimal(fake.random_number(digits=5)) / Decimal(100)),
            "notes": {"Note": fake.paragraph()},
            "entities": [entity_id]
        }

        record_response = await client.post(
            "/api/record/",
            cookies=authenticated_user.get_auth_cookies(),
            json=record_data
        )

        if record_response.status_code == 200:
            created_record_id = record_response.json()["result"]["id"]
            record_id_to_yield = created_record_id

            # Now create a movement linked to that record
            movement_data = {
                "type_tag": fake.random_element(["Income", "Expense"]),
                "name": fake.sentence(nb_words=3),
                "parts": 1,
                "total": str(Decimal(fake.random_number(digits=4)) / Decimal(100)),
                "is_due": today.isoformat(),
                "payment_date": today.isoformat(),
                "bank_account": bank_id,
                "category_tag": "Test Category",
                "subcategory_tag": "Test Subcategory",
                "status": False,
                "notes": {
                    "Description": fake.sentence(),
                    "Note": fake.paragraph(),
                    "Category": fake.random_element(["Primary", "Secondary", "Tertiary"])
                },
                "cycle": "Único",
                "unique": None,
                "interest": None,
                "penalty": None,
                "ignore_in_totals": False,
                "record": created_record_id
            }
            movement_data_to_yield = movement_data

            movement_response = await client.post(
                "/api/movement/",
                cookies=authenticated_user.get_auth_cookies(),
                json=movement_data
            )

            if movement_response.status_code == 200:
                created_movement_id = movement_response.json()["result"]["id"]
                movement_id_to_yield = created_movement_id
            else:
                print(
                    f"""Failed to create movement:
                    {movement_response.status_code},
                    {movement_response.text}
                    """)
                # movement_id_to_yield remains a dummy UUID
        else:
            print(f"Failed to create record: {record_response.status_code}, {record_response.text}")
            # record_id_to_yield and movement_id_to_yield remain dummy UUIDs
            # Update movement_data_to_yield's record field to the dummy record_id_to_yield
            movement_data_to_yield["record"] = record_id_to_yield


        yield movement_id_to_yield, movement_data_to_yield, record_id_to_yield

    except Exception as e:
        print(f"Exception during movement/record creation: {str(e)}")
        # Ensure movement_data_to_yield's record field is consistent if an exception occurs
        movement_data_to_yield["record"] = record_id_to_yield
        yield movement_id_to_yield, movement_data_to_yield, record_id_to_yield
    finally:
        # Clean up movement first, as it might depend on the record
        if created_movement_id:
            try:
                await client.delete(
                    f"/api/movement/{created_movement_id}",
                    cookies=authenticated_user.get_auth_cookies()
                )
            except Exception as e:
                print(f"Error deleting movement {created_movement_id} during cleanup: {str(e)}")

        # Then clean up record
        if created_record_id:
            try:
                await client.delete(
                    f"/api/record/{created_record_id}",
                    cookies=authenticated_user.get_auth_cookies()
                )
            except Exception as e:
                print(f"Error deleting record {created_record_id} during cleanup: {str(e)}")


@pytest_asyncio.fixture
async def test_scheduler(client, authenticated_user):
    """Create a test scheduler event, yield ID and data, then clean up.
    Cleans up the scheduler event afterwards.
    """
    today = datetime.date.today()
    scheduler_data = {
        "type_tag": fake.random_element(["Meeting", "Appointment", "Deadline", "Reminder"]),
        "name": fake.sentence(nb_words=3),
        "status": fake.boolean(),
        "date": today.isoformat(),
        "beginning_time": datetime.time(10, 0).isoformat(),
        "ending_time": datetime.time(11, 0).isoformat(),
        "notes": {
            "Location":fake.address()
        },
        "origin": None
    }
    scheduler_id_to_yield = str(uuid.uuid4())
    created_scheduler_id = None

    try:
        response = await client.post(
            "/api/scheduler/",
            cookies=authenticated_user.get_auth_cookies(),
            json=scheduler_data
        )

        if response.status_code == 200:
            result = response.json()["result"]
            created_scheduler_id = result["id"]
            scheduler_id_to_yield = created_scheduler_id
            yield scheduler_id_to_yield, scheduler_data
        else:
            print(f"Failed to create scheduler: {response.status_code}, {response.text}")
            yield scheduler_id_to_yield, scheduler_data
    except Exception as e:
        print(f"Exception during scheduler creation: {str(e)}")
        yield scheduler_id_to_yield, scheduler_data
    finally:
        if created_scheduler_id:
            try:
                await client.delete(
                    f"/api/scheduler/{created_scheduler_id}",
                    cookies=authenticated_user.get_auth_cookies()
                )
            except Exception as e:
                print(f"Error deleting scheduler {created_scheduler_id} during cleanup: {str(e)}")
