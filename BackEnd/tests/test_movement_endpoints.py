import pytest
import pytest_asyncio
import uuid
from decimal import ROUND_HALF_EVEN, Decimal, ROUND_DOWN
import json
from faker import Faker
from src.dependencies.pwHash import hash_password
from .test_utils import authenticated_user, client, test_bank_account, test_settings, test_bank_account_2


fake = Faker()


def valid_movement(
    bank_id,  # Required for both create and update
    mode="basic",
    id_param=None,
    record_param=None,
    type_param=None,
    total_param=None,
    status_param=None,
    ignore_in_totals_param=None,
    details_param=None,
    name_param=None,
    parts_param=None,
    cycle_param=None,
    interest_param=None,
    penalty_param=None,
    category_param=None,
    subcategory_param=None,
    payment_date_param=None, # Expects datetime.date object, ISO string, or None
    is_due_param=None,       # Expects datetime.date object, ISO string, or None
    unique_param=None
):
    """
    Generates a valid movement data payload for creation or update.

    Create Mode (movement_id_param is None):
    - Uses provided parameters or fakes data if a parameter is None.
    - Date fields (payment_date, is_due) are formatted to ISO strings.

    Update Mode (movement_id_param is provided):
    - Includes 'id' and 'bank_account'.
    - For all other fields, if a parameter is provided, its value is used.
    - If a parameter is not provided (or is explicitly None), the field
      will be set to None in the payload (translating to 'null' in JSON).
    - Date fields are formatted to ISO strings if they are datetime.date objects.
    """

    # --- CREATE Mode ---
    if id_param is None and mode=="basic":
        payload = {
            "type": fake.random_element(["income", "expense"]),
            "details": [
                {"title": "Description", "field": fake.sentence()},
                {"title": "Notes", "field": fake.paragraph()},
                {"title": "Category", "field": fake.random_element(["Primary", "Secondary", "Tertiary"])}
            ],
            "record": str(uuid.uuid4()),
            "parts": fake.random_int(min=1, max=10),
            "total": str(Decimal(fake.random_number(digits=4)) / Decimal(100)),
            "cycle": fake.random_element(["daily", "weekly", "monthly", "only"]),
            "bank_account": bank_id,
            "name": fake.word(),
            "interest": str(Decimal(fake.random_number(digits=2)) / Decimal(100)),
            "penalty": str(Decimal(fake.random_number(digits=2)) / Decimal(100)),
            "ignore_in_totals": False,
            "category": fake.word(),
            "subcategory": fake.word(),
            "payment_date": fake.date(),
            "is_due": fake.date(),
            "status": True
        }

        return payload

    elif id_param is None and mode=="custom":
        # Determine final_cycle
        if cycle_param is not None:
            final_cycle = cycle_param
        else:
            final_cycle = fake.random_element(["daily", "weekly", "monthly", "only", "custom"])

        # Determine final_unique
        if unique_param is not None: # Test explicitly provided unique_param
            final_unique = unique_param
        else: # unique_param was not provided by test, so default it based on final_cycle
            if final_cycle == "custom":
                final_unique = fake.random_int(min=1, max=30) # Default interval for "custom" cycle
            else:
                final_unique = None

        payload = {
            "type": type_param if type_param is not None else fake.random_element(["income", "expense"]),
            "details": details_param if details_param is not None else [
                {"title": "Description", "field": fake.sentence()},
                {"title": "Notes", "field": fake.paragraph()},
                {"title": "Category", "field": fake.random_element(["Primary", "Secondary", "Tertiary"])}
            ],
            "record": record_param if record_param is not None else str(uuid.uuid4()),
            "parts": parts_param if parts_param is not None else fake.random_int(min=1, max=10),
            "total": str(total_param) if total_param is not None else str(Decimal(fake.random_number(digits=4)) / Decimal(100)),
            "cycle": final_cycle,
            "bank_account": bank_id,
            "name": name_param if name_param is not None else fake.word(),
            "interest": interest_param if interest_param is not None else str(Decimal(fake.random_number(digits=2)) / Decimal(100)),
            "penalty": penalty_param if penalty_param is not None else str(Decimal(fake.random_number(digits=2)) / Decimal(100)),
            "ignore_in_totals": ignore_in_totals_param if ignore_in_totals_param is not None else False,
            "category": category_param if category_param is not None else fake.word(),
            "subcategory": subcategory_param if subcategory_param is not None else fake.word(),
            "payment_date": payment_date_param if payment_date_param is not None else fake.date(),
            "is_due": is_due_param if is_due_param is not None else fake.date(),
            "status": status_param if status_param is not None else True,
            "unique": final_unique
        }

        return payload

    # --- UPDATE Mode ---
    else:
        payload = {
            "id": id_param,
            "details": details_param,
        }
        return payload

def valid_payment(
    payment_id,
    bank_id=None,
    value_param=None,
    status_param=None,
    ignore_in_totals_param=None,
    name_param=None,
    interest_param=None,
    penalty_param=None,
    category_param=None,
    subcategory_param=None,
    payment_date_param=None, # Expects datetime.date object, ISO string, or None
    is_due_param=None,
):
    return {
        "id": payment_id,
        "account": bank_id,
        "name": name_param,
        "value": value_param if value_param is None else str(value_param),
        "interest": interest_param,
        "penalty": penalty_param,
        "ignore_in_totals": ignore_in_totals_param,
        "category": category_param,
        "subcategory": subcategory_param,
        "payment_date": payment_date_param,
        "is_due": is_due_param,
        "status": status_param
    }

async def get_bank_account(bank_id, client, authenticated_user):
    """Helper function to get bank account details."""
    response = await client.get(f"/api/user/bank-account/{bank_id}", cookies=authenticated_user.get_auth_cookies()) # Corrected endpoint
    return response.status_code, response.json()


async def get_movement(movement_id, client, authenticated_user):
    """Helper function to get movement details."""
    response = await client.get(f"/api/movement/{movement_id}", cookies=authenticated_user.get_auth_cookies()) # Corrected endpoint
    return response.status_code, response.json()


async def get_payment(payment_id, client, authenticated_user):
    """Helper function to get payment details."""
    response = await client.get(f"/api/movement/payment/{payment_id}", cookies=authenticated_user.get_auth_cookies()) # Corrected endpoint
    return response.status_code, response.json()


async def post_movement(movement, client, authenticated_user):
    """Helper function to post movement."""
    response = await client.post("/api/movement/", json=movement, cookies=authenticated_user.get_auth_cookies()) # Corrected endpoint
    return response.status_code, response.json()


async def update_movement(movement, client, authenticated_user):
    """Helper function to update movement."""
    response = await client.put("/api/movement/", json=movement, cookies=authenticated_user.get_auth_cookies()) # Corrected endpoint
    return response.status_code, response.json()


async def update_payment(payment, client, authenticated_user):
    """Helper function to update payment."""
    response = await client.put("/api/movement/payment", json=payment, cookies=authenticated_user.get_auth_cookies()) # Corrected endpoint
    return response.status_code, response.json()


async def delete_movement(movement_id, client, authenticated_user):
    """Helper function to delete movement."""
    response = await client.delete(f"/api/movement/{movement_id}", cookies=authenticated_user.get_auth_cookies()) # Corrected endpoint
    return response.status_code, response.json()


async def delete_payment(payment_id, client, authenticated_user):
    """Helper function to delete payment."""
    response = await client.get(f"/api/movement/payment/{payment_id}", cookies=authenticated_user.get_auth_cookies()) # Corrected endpoint
    return response.status_code, response.json()


class TestMovementEndpoints:
    """Test the movement endpoints."""

    @pytest.mark.asyncio
    async def test_create_get_update_delete_movement(self, client, authenticated_user, test_bank_account):
        """Test the complete movement CRUD operations."""
        bank_id, _ = test_bank_account

        # Create movement
        data = valid_movement(bank_id=bank_id)

        status, create_response = await post_movement(data, client, authenticated_user)

        assert status == 200
        assert create_response["status"] == "success"

        movement = create_response["result"]

        # Get movement details
        status, get_response = await get_movement(movement["id"], client, authenticated_user)

        assert status < 300
        get_data = get_response["result"]
        assert get_data["type"] == data["type"]
        # Verify details array contains expected items
        description_found = False
        for detail in get_data["details"]:
            if detail["title"] == "Description":
                # Find the matching detail from the input data
                for input_detail in data["details"]:
                    if input_detail["title"] == "Description":
                        assert detail["field"] == input_detail["field"]
                        description_found = True
                        break
        assert description_found, "Description detail not found in response"

        details = {
            "body": get_data["details"],
            "change": True
        }
        update_data = valid_movement(bank_id, id_param=movement["id"], details_param=details)


        status, update_response = await update_movement(update_data, client, authenticated_user)

        assert status < 300

        # Verify update
        status, get_updated_response = await get_movement(movement["id"], client, authenticated_user)

        assert status < 300
        assert get_updated_response["status"] == "success"
        updated_data_2 = get_updated_response["result"]
        # Verify the details were updated correctly
        assert len(updated_data_2["details"]) == len(get_data["details"])
        for detail in updated_data_2["details"]:
            assert any(d["title"] == detail["title"] for d in get_data["details"])

        # Delete movement
        status, delete_response = await delete_movement(movement["id"], client, authenticated_user)

        assert status < 300
        assert delete_response["status"] == "success"

        # Verify deletion
        status, _ = await get_movement(movement["id"], client, authenticated_user)
        assert status != 200


    @pytest.mark.asyncio
    async def test_create_get_update_delete_payment(self, client, authenticated_user, test_bank_account):
        """Test the complete payment CRUD operations."""
        bank_id, _ = test_bank_account

        # Create movement
        data = valid_movement(bank_id)

        status, create_response = await post_movement(data, client, authenticated_user)

        assert status == 200
        assert create_response["status"] == "success"

        movement = create_response["result"]

        # Get movement details
        status, get_response = await get_movement(movement["id"], client, authenticated_user)

        assert status < 300
        get_data = get_response["result"]
        payment = get_data["payment"][0]["id"]


        status, get_response = await get_payment(payment, client, authenticated_user)
        assert status == 200
        assert get_response["status"] == "success"

        # Update payment
        update_data = valid_payment(payment, name_param=(fake.word() + " updated"), is_due_param=fake.date())

        status_update, _ = await update_payment(update_data, client, authenticated_user)
        assert status_update == 200

        status, get_response = await get_payment(payment, client, authenticated_user)
        assert status == 200
        assert get_response["status"] == "success"
        updated_payment = get_response["result"]
        print(updated_payment)
        assert updated_payment["name"] == update_data["name"]
        assert updated_payment["is_due"] == update_data["is_due"]

        # Delete payment
        status, delete_response = await delete_payment(payment, client, authenticated_user)

        assert status == 200
        assert delete_response["status"] == "success"


    @pytest.mark.asyncio
    async def test_movement_invalid_uuid(self, client, authenticated_user):
        """Test that invalid UUIDs return a 422 status code."""
        invalid_uuid = "invalid-uuid"  # A string that is not a valid UUID

        response, _ = await get_movement(invalid_uuid, client, authenticated_user)

        assert response == 422

    @pytest.mark.asyncio
    async def test_unauthorized_access_movement(self, client, test_bank_account):
        bank_id, _ = test_bank_account
        # Try to get movement data without authentication

        fake_id = str(uuid.uuid4())
        response = await client.get(f"/api/movement/{fake_id}")
        assert response.status_code == 401

        # Try to create movement without authentication
        movement_data = valid_movement(bank_id)

        movement_response = await client.post("/api/movement/", json=movement_data)
        assert movement_response.status_code == 401


    @pytest.mark.asyncio
    async def test_unauthorized_access_payment(self, client):
        # Try to get payment data without authentication

        fake_id = str(uuid.uuid4())
        response = await client.get(f"/api/movement/payment/{fake_id}")
        assert response.status_code == 401

        # Try to update payment without authentication
        payment_data = valid_payment(fake_id)

        payment_response = await client.put("/api/movement/payment", json=payment_data)
        assert payment_response.status_code == 401


    @pytest.mark.asyncio
    async def test_balance_after_movement_creation(self, client, authenticated_user, test_bank_account):
        """Test bank account balance updates correctly after a movement is created."""
        bank_id, _ = test_bank_account

        _, initial_bank_details = await get_bank_account(bank_id, client, authenticated_user)
        initial_balance = Decimal(initial_bank_details["result"]["balance"]).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)
        movement_type = fake.random_element(["income", "expense"])
        movement_total = (Decimal(fake.random_number(digits=3, fix_len=True)) / Decimal('100')).quantize(Decimal('0.01'))


        movement_data = valid_movement(
            bank_id,
            mode="custom",
            total_param=movement_total,
            type_param=movement_type,
            cycle_param="only",
            parts_param=1,
            status_param=True,
            ignore_in_totals_param=False
        )

        status, create_response = await post_movement(movement_data, client, authenticated_user)
        assert status == 200

        _, updated_bank_details = await get_bank_account(bank_id, client, authenticated_user)
        new_balance = Decimal(updated_bank_details["result"]["balance"]).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)

        if movement_type == "income":
            expected_balance = initial_balance + movement_total
        else: # expense
            expected_balance = initial_balance - movement_total

        assert new_balance == expected_balance, f"Resposta da criação: {create_response['result']}"


    @pytest.mark.asyncio
    async def test_balance_on_payment_value_update(self, client, authenticated_user, test_bank_account):
        """Test bank account balance updates correctly when a payment's value is changed."""
        bank_id, _ = test_bank_account

        # Create an initial movement
        initial_payment_value = Decimal("50.00").quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)

        movement_data = valid_movement(bank_id, mode="custom", total_param="50.00", cycle_param="only", type_param="expense", parts_param=1)
        status, create_movement_response = await post_movement(movement_data, client, authenticated_user)

        assert status == 200, f"Movement creation failed: {create_movement_response}"
        movement_id = create_movement_response["result"]["id"]

        # Get movement details to find the payment ID
        status, get_movement_response = await get_movement(movement_id, client, authenticated_user)
        assert status == 200
        movement_details = get_movement_response["result"]

        assert "payment" in movement_details and len(movement_details["payment"]) > 0, "No payment list found in movement details"
        payment_to_update = movement_details["payment"][0] # Assuming first payment
        payment_id = payment_to_update["id"]
        status, payment_details = await get_payment(payment_id, client, authenticated_user)
        assert status == 200
        # Ensure the payment is associated with the correct bank account initially
        assert payment_details["result"]["account"]["id"] == bank_id

        status, initial_bank_details = await get_bank_account(bank_id, client, authenticated_user)
        balance_before_update = Decimal(initial_bank_details["result"]["balance"]).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)

        # Update the payment's value
        new_payment_value = Decimal("70.00").quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)

        # Fetch the full payment to update it, as PUT might require all fields
        payment_update_data = valid_payment(payment_id, value_param=new_payment_value)
        status, update_response = await update_payment(payment_update_data, client, authenticated_user)
        assert status == 200, f"Payment update failed: {update_response}"

        status, updated_bank_details = await get_bank_account(bank_id, client, authenticated_user)
        balance_after_update = Decimal(updated_bank_details["result"]["balance"]).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)

        # Original movement was expense. Initial value was 50. New value is 70.
        # Balance change = old_value - new_value (since it's an expense, higher value means more deduction)
        expected_balance_after_update = balance_before_update - (new_payment_value - initial_payment_value)

        assert balance_after_update == expected_balance_after_update, \
            f"Balance mismatch after payment update: Initial {balance_before_update}, New {balance_after_update}, Expected {expected_balance_after_update}"


    @pytest.mark.asyncio
    async def test_balance_of_two_bank_accounts_on_payment_account_update(self, client, authenticated_user, test_bank_account, test_bank_account_2):
        """Test balances of two bank accounts on update of a Payment's account_id."""
        bank_id_1, _ = test_bank_account
        bank_id_2, _ = test_bank_account_2

        payment_value = Decimal("30.00").quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)
        balance = {
            "before movement acc1": 0,
            "before movement acc2": 0,
            "after movement acc1": 0,
            "after movement acc2": 0,
            "after update acc1": 0,
            "after update acc2": 0,
        }
        # Create an initial movement (expense) from bank_id_1
        _, initial_balance = await get_bank_account(bank_id_1, client, authenticated_user)
        balance["before movement acc1"] = Decimal(initial_balance["result"]["balance"]).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)
        _, initial_balance = await get_bank_account(bank_id_2, client, authenticated_user)
        balance["before movement acc2"] = Decimal(initial_balance["result"]["balance"]).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)

        movement_data = valid_movement(bank_id_1, mode="custom", parts_param=1, cycle_param="only", total_param=payment_value, type_param="expense")
        status, create_response = await post_movement(movement_data, client, authenticated_user)
        assert status == 200, f"Movement creation failed: {create_response}"
        movement_id = create_response["result"]["id"]

        status, get_movement_response = await get_movement(movement_id, client, authenticated_user)
        assert status == 200
        movement_details = get_movement_response["result"]
        assert "payment" in movement_details and len(movement_details["payment"]) > 0, "Payment list not found in movement"
        payment_to_update = movement_details["payment"][0]
        payment_id = payment_to_update["id"]

        # Get initial balances (after the payment has been posted from account 1)
        _, initial_details_acc1 = await get_bank_account(bank_id_1, client, authenticated_user)
        balance["after movement acc1"] = Decimal(initial_details_acc1["result"]["balance"]).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)
        _, initial_details_acc2 = await get_bank_account(bank_id_2, client, authenticated_user)
        balance["after movement acc2"] = Decimal(initial_details_acc2["result"]["balance"]).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)


        payment_update_data = valid_payment(payment_id, bank_id=bank_id_2)
        status, update_response = await update_payment(payment_update_data, client, authenticated_user)
        assert status == 200, f"Payment account update failed: {update_response}"

        # Get new balances
        _, final_details_acc1 = await get_bank_account(bank_id_1, client, authenticated_user)
        balance["after update acc1"] = Decimal(final_details_acc1["result"]["balance"]).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)
        _, final_details_acc2 = await get_bank_account(bank_id_2, client, authenticated_user)
        balance["after update acc2"] = Decimal(final_details_acc2["result"]["balance"]).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)


        assert balance["after movement acc1"] == balance["before movement acc1"] - payment_value
        assert balance["after update acc1"] == balance["after movement acc1"] + payment_value
        assert payment_value == balance["after movement acc2"] - balance["after update acc2"]


    @pytest.mark.asyncio
    async def test_schedule_entry_creation_on_payment_insert(self, client, authenticated_user, test_bank_account):
        """Test that a schedule entry is created when a recurring movement/payment is made."""
        bank_id, _ = test_bank_account
        movement_data = valid_movement(bank_id)

        status, create_response = await post_movement(movement_data, client, authenticated_user)
        assert status == 200, f"Movement creation for schedule test failed: {create_response}"

        movement_id = create_response["result"]["id"]
        status, get_movement_response = await get_movement(movement_id, client, authenticated_user)
        assert status == 200

        movement_details = get_movement_response["result"]
        assert "payment" in movement_details and len(movement_details["payment"]) > 0, \
            "Payment list not found in movement details for scheduled movement."

        # Iterate through payments to check for scheduler_id (event id)
        scheduler_id_found = False
        for payment_item in movement_details["payment"]:
            payment_id = payment_item["id"]
            status, get_pay = await get_payment(payment_id, client, authenticated_user)
            assert status == 200
            print(get_pay["result"])
            payment = get_pay["result"]
            # Check for event and event id
            if "event" in payment and "id" in payment["event"]:
                scheduler_id_found = True

        assert scheduler_id_found, "Scheduler ID (event_id) not found in any payment for a recurring movement."
