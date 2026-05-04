from app.models import User


def test_create_user_success(client):
    response = client.post(
        "/api/v1/users",
        json={"login": "test"},
    )

    assert response.status_code == 200
    assert response.json()["login"] == "test"


def test_create_user_already_exists(db_session, client):
    user = User(login="test")
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/api/v1/users",
        json={"login": "test"},
    )


    assert response.status_code == 400


def test_get_current_user_success(db_session, client):
    user = User(login="test")
    db_session.add(user)
    db_session.commit()

    response = client.get(
        "/api/v1/users",
        headers={"Authorization": f"Bearer {user.login}"},
    )


    assert response.status_code == 200
    assert response.json()["login"] == user.login

def test_get_current_user_unauthorized(client):
    response = client.get(
        "/api/v1/users",
        headers={"Authorization": "Bearer notexists"},
    )

    assert response.status_code == 401