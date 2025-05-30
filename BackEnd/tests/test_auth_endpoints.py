import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
from faker import Faker
import jwt
import uuid
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


class TestAuth:
    """Test the authentication endpoints and CRUD functions directly."""

    @pytest.mark.asyncio
    async def test_register_with_password_mismatch(self, client):
        """Test registration with mismatched passwords."""
        test_email = fake.email()
        test_password = fake.password()
        test_name = fake.name()

        register_response = await client.post("/api/auth/register", json={
            "email": test_email,
            "password": test_password,
            "confirm_password": test_password + "different",
            "name": test_name
        })

        assert register_response.status_code == 422
        assert "Password is not coinciding" in str(register_response.json())


    @pytest.mark.asyncio
    async def test_register_with_invalid_email(self, client):
        """Test registration with an invalid email format."""
        test_password = fake.password()
        test_name = fake.name()

        register_response = await client.post("/api/auth/register", json={
            "email": "invalid-email-format",
            "password": test_password,
            "confirm_password": test_password,
            "name": test_name
        })

        assert register_response.status_code == 422
        assert "email" in str(register_response.json())


    @pytest.mark.asyncio
    async def test_register_login_logout_flow(self, client):
        """Test the complete user registration, login, and logout flow."""
        # Generate test data
        test_email = fake.email()
        test_password = fake.password(length=12, special_chars=True)
        test_name = fake.name()

        # Step 1: Register a new user
        register_response = await client.post("/api/auth/register", json={
            "email": test_email,
            "password": test_password,
            "confirm_password": test_password,
            "name": test_name
        })

        assert register_response.status_code == 200
        assert register_response.json() == {"status": "success"}

        # Step 2: Login with the registered credentials
        login_response = await client.post("/api/auth/login", json={
            "email": test_email,
            "password": test_password
        })

        assert login_response.status_code == 200
        assert login_response.json() == {"status": "success"}

        # Verify cookies are set
        cookies = login_response.cookies
        assert "access_token" in cookies
        assert "refresh_token" in cookies

        # Verify token contents
        access_token = cookies["access_token"]
        payload = jwt.decode(access_token, settings.secret, algorithms=[settings.algorithm])
        assert payload["type"] == "access"

        # Step 3: Access a protected route (logout) with the token
        logout_response = await client.get(
            "/api/auth/logout",
            cookies={
                "access_token": cookies["access_token"],
                "refresh_token": cookies["refresh_token"]
            }
        )

        assert logout_response.status_code == 200
        assert logout_response.json() == {"status": "success"}


    @pytest.mark.asyncio
    async def test_login_with_nonexistent_user(self, client):
        """Test login with a user that doesn't exist."""
        # Use a random email that's unlikely to exist
        test_email = f"nonexistent_{fake.uuid4()}@example.com"
        test_password = fake.password()

        login_response = await client.post("/api/auth/login", json={
            "email": test_email,
            "password": test_password
        })

        assert login_response.status_code == 404
        assert "User doesn't exist or password doesn't match" in login_response.json()["detail"]


    @pytest.mark.asyncio
    async def test_forgot_password(self, client):
        """Test the forgot password functionality."""
        # First register a user
        test_email = fake.email()
        test_password = fake.password()
        test_name = fake.name()

        await client.post("/api/auth/register", json={
            "email": test_email,
            "password": test_password,
            "confirm_password": test_password,
            "name": test_name
        })

        # Now test forgot password with this email
        forgot_response = await client.post(
            "/api/auth/forgot_password",
            json={"email": test_email}
        )

        assert forgot_response.status_code == 200
        assert forgot_response.json() == {"status": "success"}


    @pytest.mark.asyncio
    async def test_forgot_password_nonexistent_user(self, client):
        """Test forgot password with non-existent user."""
        # Use a random email that's unlikely to exist
        test_email = f"nonexistent_{fake.uuid4()}@example.com"

        forgot_response = await client.post(
            "/api/auth/forgot_password",
            json={"email": test_email}
        )

        assert forgot_response.status_code == 401
        assert "There is no user" in forgot_response.json()["detail"]


    @pytest.mark.asyncio
    async def test_protected_route_without_token(self, client):
        """Test accessing a protected route without authentication."""
        logout_response = await client.get("/api/auth/logout")

        assert logout_response.status_code == 401
        assert "Some error on Auth Token!!!" in logout_response.json()["detail"]


    @pytest.mark.asyncio
    async def test_login_with_invalid_password(self, client):
        """Test login with correct email but wrong password."""
        # First register a user
        test_email = fake.email()
        test_password = fake.password()
        test_name = fake.name()

        await client.post("/api/auth/register", json={
            "email": test_email,
            "password": test_password,
            "confirm_password": test_password,
            "name": test_name
        })

        # Try to login with wrong password
        login_response = await client.post("/api/auth/login", json={
            "email": test_email,
            "password": test_password + "wrong"
        })

        assert login_response.status_code == 404
        assert "User doesn't exist or password doesn't match" in login_response.json()["detail"]


    @pytest.mark.asyncio
    async def test_login_token_with_invalid_token(self, client):
        """Test login with token using an invalid token."""
        # First register a user
        test_email = fake.email()
        test_password = fake.password()
        test_name = fake.name()

        await client.post("/api/auth/register", json={
            "email": test_email,
            "password": test_password,
            "confirm_password": test_password,
            "name": test_name
        })

        # Try to login with a random token
        random_token = str(uuid.uuid4())
        login_token_response = await client.post("/api/auth/login_token", json={
            "email": test_email,
            "token": random_token
        })

        assert login_token_response.status_code == 404
        assert "User doesn't exist or token doesn't match" in login_token_response.json()["detail"]


    @pytest.mark.asyncio
    async def test_refresh_token(self, client):
        """Test refreshing the access token using the refresh token."""
        # First register and login to get tokens
        test_email = fake.email()
        test_password = fake.password()
        test_name = fake.name()

        await client.post("/api/auth/register", json={
            "email": test_email,
            "password": test_password,
            "confirm_password": test_password,
            "name": test_name
        })

        login_response = await client.post("/api/auth/login", json={
            "email": test_email,
            "password": test_password
        })

        cookies = login_response.cookies

        # Test refresh endpoint
        refresh_response = await client.get(
            "/api/auth/refresh",
            cookies={"refresh_token": cookies["refresh_token"]}
        )

        assert refresh_response.status_code == 200
        assert refresh_response.json() == {"status": "success"}
        assert "access_token" in refresh_response.cookies

        # Verify the new token is valid
        new_access_token = refresh_response.cookies["access_token"]
        payload = jwt.decode(new_access_token, settings.secret, algorithms=[settings.algorithm])
        assert payload["type"] == "access"


    @pytest.mark.asyncio
    async def test_refresh_without_refresh_token(self, client):
        """Test refresh endpoint without providing a refresh token."""
        refresh_response = await client.get("/api/auth/refresh")

        assert refresh_response.status_code == 401
        assert "REFRESH TOKEN is missing." in refresh_response.json()["detail"]


    @pytest.mark.asyncio
    async def test_login_with_malformed_json(self, client):
        """Test login with malformed JSON."""
        response = await client.post(
            "/api/auth/login",
            content='{"email": "test@example.com", "password": "incomplete'
        )
        assert response.status_code == 422


    @pytest.mark.asyncio
    async def test_login_with_missing_fields(self, client):
        """Test login with missing required fields."""
        response = await client.post(
            "/api/auth/login",
            json={"email": fake.email()}  # Missing password
        )
        assert response.status_code == 422
