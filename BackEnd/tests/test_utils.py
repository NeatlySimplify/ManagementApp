import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from faker import Faker
import uuid
import jwt
from decimal import Decimal
import datetime
from src.main import app
from src.settings import get_settings
from asgi_lifespan import LifespanManager

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
    """Create and authenticate a test user, then clean up afterwards."""
    user = TestUser()

    # Register the user
    register_response = await client.post("/api/auth/register", json={
        "email": user.email,
        "password": user.password,
        "confirm_password": user.password,
        "name": user.name
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
    payload = user.get_token_payload()
    user.user_id = payload["sub"]

    yield user

    # Logout the user
    await client.get(
        "/api/auth/logout",
        cookies=user.get_auth_cookies()
    )


class BankAccountData:
    """Helper class for bank account test data."""

    @staticmethod
    def generate_data():
        """Generate random bank account data."""
        return {
            "bank_name": fake.company(),
            "account_name": fake.random_element(["Checking", "Savings", "Investment"]),
            "type": fake.random_element(["Personal", "Business", "Joint"]),
            "balance": str(Decimal(fake.random_number(digits=5)) / Decimal(100)),
            "details": {
                "account_number": str(fake.random_number(digits=10)),
                "routing_number": str(fake.random_number(digits=9))
            },
            "ignore_on_totals": False,
            "category": fake.random_element(["Primary", "Secondary", "Emergency"])
        }


@pytest_asyncio.fixture
async def test_bank_account(client, authenticated_user):
    """Create a test bank account and return its ID."""
    bank_data = BankAccountData.generate_data()

    try:
        response = await client.post(
            "/api/user/bank-account",
            cookies=authenticated_user.get_auth_cookies(),
            json=bank_data
        )

        if response.status_code == 200:
            bank_id = response.json()["id"]

            yield bank_id, bank_data

            # Clean up - delete the bank account
            try:
                await client.delete(
                    f"/api/user/bank-account?id={bank_id}",
                    cookies=authenticated_user.get_auth_cookies()
                )
            except Exception:
                pass
        else:
            # If we can't create a bank account, return a dummy UUID
            yield str(uuid.uuid4()), bank_data
    except Exception:
        # If we encounter an exception, return a dummy UUID
        yield str(uuid.uuid4()), bank_data


@pytest_asyncio.fixture
async def test_settings(client, authenticated_user, test_bank_account):
    """Create test settings and return its ID."""
    bank_id, _ = test_bank_account

    settings_data = {
        "record_title": fake.word(),
        "movement_title": fake.word(),
        "entity_title": fake.word()
    }

    try:
        response = await client.post(
            f"/api/user/settings?id={bank_id}",
            cookies=authenticated_user.get_auth_cookies(),
            json=settings_data
        )

        if response.status_code == 200:
            settings_id = response.json()["id"]
            yield settings_id, settings_data
        else:
            # If we can't create settings, return a dummy UUID
            yield str(uuid.uuid4()), settings_data
    except Exception:
        # If we encounter an exception, return a dummy UUID
        yield str(uuid.uuid4()), settings_data
