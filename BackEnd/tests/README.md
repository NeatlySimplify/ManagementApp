# Testing Guide for Backend API

This directory contains all the tests for the Backend API. Tests are written using pytest and pytest-asyncio for asynchronous testing capabilities.

## Overview

The test suite contains:

- Unit tests for individual components
- Integration tests for API endpoints
- Utilities for test data management and authentication

## Test Structure

- `test_auth_endpoints.py`: Tests for authentication endpoints
- `test_user_endpoints.py`: Tests for user management endpoints
- `test_utils.py`: Shared testing utilities and fixtures

## Key Utilities

### Fixtures

The test suite provides several fixtures to simplify testing:

- `client`: HTTP client for making requests to the API
- `authenticated_user`: Creates and authenticates a test user
- `test_bank_account`: Creates a test bank account
- `test_settings`: Creates test user settings

### TestUser Class

The `TestUser` class in `test_utils.py` centralizes user authentication and data management:

```python
user = TestUser()  # Create a new test user
cookies = user.get_auth_cookies()  # Get authentication cookies
payload = user.get_token_payload()  # Get JWT token payload
```

## Writing New Tests

1. Import required fixtures from test_utils:

```python
from .test_utils import authenticated_user, client, test_bank_account
```

2. Use fixtures in your test functions:

```python
@pytest.mark.asyncio
async def test_my_endpoint(client, authenticated_user):
    response = await client.get(
        "/api/my-endpoint",
        cookies=authenticated_user.get_auth_cookies()
    )
    assert response.status_code == 200
```

3. For tests requiring data setup, use the provided fixtures:

```python
@pytest.mark.asyncio
async def test_with_bank_account(client, authenticated_user, test_bank_account):
    bank_id, bank_data = test_bank_account
    # Test code using the bank account
```

## Running Tests

Run all tests:
```
pytest
```

Run specific test file:
```
pytest tests/test_user_endpoints.py
```

Run with verbose output:
```
pytest -v
```

## Best Practices

1. Always clean up test data created during tests
2. Use descriptive test names
3. Test both successful and error cases
4. Avoid mocking CRUD functions directly to ensure full integration testing
5. Use the fixtures from `test_utils.py` for consistent test setup
6. Add proper assertions to verify expected behavior