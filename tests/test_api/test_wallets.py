from decimal import Decimal

from app.models import User, Wallet

def test_create_wallet_success(db_session, client):
    user = User(login="test")
    db_session.add(user)
    db_session.commit()

    response = client.post(
         "/api/v1/wallets",
        json={
            "name": "cash",
            "initial_balance": 100,
        },
        headers={"Authorization": f"Bearer {user.login}"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Wallet {wallet.name} successfully."
    assert response.json()["wallet"] == "cash"
    assert Decimal(str(response.json()["balance"])) == Decimal("100")


def test_create_wallet_already_exists(db_session, client, test_wallet, test_user):
    response = client.post(
         "/api/v1/wallets",
        json={
            "name": test_wallet.name,
            "initial_balance": 100,
        },
        headers={"Authorization": f"Bearer {test_user.login}"},
    )

    assert response.status_code == 400


def test_get_balance_for_one_wallet_success(db_session, client, test_wallet, test_user):
    response = client.get(
        "/api/v1/balance",
        params={"wallet_name": test_wallet.name},
        headers={"Authorization": f"Bearer {test_user.login}"},
    )


    assert response.status_code == 200
    assert response.json()["wallet"] == test_wallet.name
    assert Decimal(str(response.json()["balance"])) == Decimal("200")


def test_get_total_balance_success(db_session, client, test_user, test_wallet):
    second_wallet = Wallet(name="cash", balance=Decimal("150"), user_id=test_user.id)
    db_session.add(second_wallet)
    db_session.commit()

    response = client.get(
        "/api/v1/balance",
        headers={"Authorization": f"Bearer {test_user.login}"},
    )

    assert response.status_code == 200
    assert Decimal(str(response.json()["total_balance"])) == Decimal("350")


def test_get_balance_wallet_not_found(db_session, client):
    user = User(login="test")
    db_session.add(user)
    db_session.commit()

    response = client.get(
        "/api/v1/balance",
        params={"wallet_name": "unknown"},
        headers={"Authorization": f"Bearer {user.login}"},
    )

    assert response.status_code == 404

def test_get_balance_unauthorized(db_session, client, test_user, test_wallet):

    response = client.post(
        "/api/v1/wallets",
        json={
            "wallet_name": "card",
            "amount": 100.0,
            "description": "Food",
        },
        headers={"Authorization": f"Bearer notexists"},
    )

    assert response.status_code == 401

def test_get_balance_unauthorized(db_session, client, test_user, test_wallet):

    response = client.get(
        "/api/v1/balance",
        params={"wallet_name": "card"},
        headers={"Authorization": f"Bearer notexists"},
    )

    assert response.status_code == 401

def test_create_wallet_unauthorized(db_session, client, test_user, test_wallet):

    response = client.post(
        "/api/v1/wallets",
        json={
            "wallet_name": "card",
            "amount": 100.0,
            "description": "Food",
        },
        headers={"Authorization": f"Bearer notexists"},
    )

    assert response.status_code == 401