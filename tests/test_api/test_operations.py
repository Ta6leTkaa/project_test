from decimal import Decimal

from app.models import User, Wallet


def test_add_expense_success(db_session, client, test_user, test_wallet):

    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 50.0,
            "description": "Food",
        },
        headers={"Authorization": f"Bearer {test_user.login}"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Expense successfully added."
    assert response.json()["wallet"] == test_wallet.name
    assert Decimal(str(response.json()["amount"])) == Decimal(50)
    assert response.json()["description"] == "Food"
    assert Decimal(str(response.json()["new_balance"])) == Decimal(150)

def test_add_expense_negative_amount(db_session, client, test_user, test_wallet):

    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": -50.0,
            "description": "Food",
        },
        headers={"Authorization": f"Bearer {test_user.login}"},
    )

    assert response.status_code == 422

def test_add_expense_empty_name(db_session, client, test_user, test_wallet):

    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "   ",
            "amount": 100.0,
            "description": "Food",
        },
        headers={"Authorization": f"Bearer {test_user.login}"},
    )

    assert response.status_code == 422

def test_add_expense_wallet_not_exists(db_session, client):
    user = User(login="test")
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 100.0,
            "description": "Food",
        },
        headers={"Authorization": f"Bearer {user.login}"},
    )

    assert response.status_code == 404

def test_add_expense_unauthorized(db_session, client, test_user, test_wallet):

    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 100.0,
            "description": "Food",
        },
        headers={"Authorization": f"Bearer notexists"},
    )

    assert response.status_code == 401

def test_add_expense_not_enough_money(db_session, client, test_user, test_wallet):

    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 250.0,
            "description": "Food",
        },
        headers={"Authorization": f"Bearer {test_user.login}"},
    )

    assert response.status_code == 400


def test_add_income_success(db_session, client, test_user, test_wallet):

    response = client.post(
        "/api/v1/operations/income",
        json={
            "wallet_name": "card",
            "amount": 50.0,
            "description": "Food",
        },
        headers={"Authorization": f"Bearer {test_user.login}"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Income successfully added."
    assert response.json()["wallet"] == test_wallet.name
    assert Decimal(str(response.json()["amount"])) == Decimal(50)
    assert response.json()["description"] == "Food"
    assert Decimal(str(response.json()["new_balance"])) == Decimal(250)

def test_add_income_wallet_not_exists(db_session, client):
    user = User(login="test")
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/api/v1/operations/income",
        json={
            "wallet_name": "card",
            "amount": 100.0,
            "description": "Food",
        },
        headers={"Authorization": f"Bearer {user.login}"},
    )

    assert response.status_code == 400

def test_add_income_unauthorized(db_session, client, test_user, test_wallet):

    response = client.post(
        "/api/v1/operations/income",
        json={
            "wallet_name": "card",
            "amount": 100.0,
            "description": "Food",
        },
        headers={"Authorization": f"Bearer notexists"},
    )

    assert response.status_code == 401

def test_add_income_negative_amount(db_session, client, test_user, test_wallet):

    response = client.post(
        "/api/v1/operations/income",
        json={
            "wallet_name": "card",
            "amount": -50.0,
            "description": "Food",
        },
        headers={"Authorization": f"Bearer {test_user.login}"},
    )

    assert response.status_code == 422

def test_add_income_empty_name(db_session, client, test_user, test_wallet):

    response = client.post(
        "/api/v1/operations/income",
        json={
            "wallet_name": "   ",
            "amount": 100.0,
            "description": "Food",
        },
        headers={"Authorization": f"Bearer {test_user.login}"},
    )

