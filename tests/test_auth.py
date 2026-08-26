from collections.abc import Callable
from datetime import timedelta

from flask import Flask
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token, decode_token
from sqlalchemy import select

from app.extensions import db
from app.models import User, UserRole
from app.security import verify_password

REGISTER_URL = "/api/auth/register"
LOGIN_URL = "/api/auth/login"
ME_URL = "/api/auth/me"


def registration_payload(**changes: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "name": "  Arthur   Silva  ",
        "email": "  Arthur@Example.COM ",
        "password": "secure-password",
        "password_confirmation": "secure-password",
    }
    payload.update(changes)
    return payload


def test_register_creates_student_and_returns_public_normalized_data(
    client: FlaskClient,
) -> None:
    response = client.post(REGISTER_URL, json=registration_payload(role="ADMIN"))

    assert response.status_code == 201
    data = response.get_json()["data"]
    assert data["name"] == "Arthur Silva"
    assert data["email"] == "arthur@example.com"
    assert data["role"] == "STUDENT"
    assert data["created_at"].endswith("Z")
    assert "password" not in data
    assert "password_hash" not in data


def test_register_stores_argon2_hash_instead_of_plaintext(
    app: Flask, client: FlaskClient
) -> None:
    password = "secure-password"
    client.post(REGISTER_URL, json=registration_payload(password=password))

    with app.app_context():
        user = db.session.scalar(select(User))
        assert user is not None
        assert user.password_hash != password
        assert user.password_hash.startswith("$argon2")
        assert verify_password(password, user.password_hash)
        assert user.role is UserRole.STUDENT


def test_register_returns_conflict_for_normalized_duplicate_email(
    client: FlaskClient,
) -> None:
    first_response = client.post(REGISTER_URL, json=registration_payload())
    second_response = client.post(
        REGISTER_URL, json=registration_payload(email="ARTHUR@example.com")
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.get_json()["error"]["code"] == ("EMAIL_ALREADY_REGISTERED")


def test_register_rejects_different_password_confirmation(
    client: FlaskClient,
) -> None:
    response = client.post(
        REGISTER_URL,
        json=registration_payload(password_confirmation="different-password"),
    )

    assert response.status_code == 422
    assert response.get_json()["error"]["code"] == "VALIDATION_ERROR"


def test_register_rejects_short_password(client: FlaskClient) -> None:
    response = client.post(
        REGISTER_URL,
        json=registration_payload(password="short", password_confirmation="short"),
    )

    assert response.status_code == 422


def test_register_rejects_missing_required_field(client: FlaskClient) -> None:
    payload = registration_payload()
    del payload["email"]

    response = client.post(REGISTER_URL, json=payload)

    assert response.status_code == 422
    assert "email" in response.get_json()["error"]["details"]


def test_register_rejects_invalid_email(client: FlaskClient) -> None:
    response = client.post(
        REGISTER_URL, json=registration_payload(email="not-an-email")
    )

    assert response.status_code == 422


def test_login_returns_bearer_token_with_user_identity(
    app: Flask,
    client: FlaskClient,
    register: Callable[..., dict[str, object]],
) -> None:
    user = register(email="mixed@example.com")

    response = client.post(
        LOGIN_URL,
        json={"email": "  MIXED@EXAMPLE.COM ", "password": "secure-password"},
    )

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["token_type"] == "bearer"
    assert data["access_token"]
    with app.app_context():
        payload = decode_token(data["access_token"])
    assert payload["sub"] == str(user["id"])
    assert payload["exp"] > payload["iat"]


def test_login_uses_same_public_error_for_unknown_email_and_wrong_password(
    client: FlaskClient, register: Callable[..., dict[str, object]]
) -> None:
    register()

    wrong_password = client.post(
        LOGIN_URL,
        json={"email": "student@example.com", "password": "wrong-password"},
    )
    unknown_email = client.post(
        LOGIN_URL,
        json={"email": "unknown@example.com", "password": "wrong-password"},
    )

    assert wrong_password.status_code == 401
    assert unknown_email.status_code == 401
    assert wrong_password.get_json() == unknown_email.get_json()
    assert wrong_password.get_json()["error"]["code"] == "INVALID_CREDENTIALS"


def test_auth_me_returns_public_user_data(
    client: FlaskClient, auth_headers: dict[str, str]
) -> None:
    response = client.get(ME_URL, headers=auth_headers)

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["email"] == "student@example.com"
    assert "password" not in data
    assert "password_hash" not in data


def test_auth_me_requires_token(client: FlaskClient) -> None:
    response = client.get(ME_URL)

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"
    assert response.get_json()["error"]["code"] == "AUTHENTICATION_REQUIRED"


def test_auth_me_rejects_invalid_token(client: FlaskClient) -> None:
    response = client.get(ME_URL, headers={"Authorization": "Bearer invalid"})

    assert response.status_code == 401
    assert response.get_json()["error"]["code"] == "INVALID_TOKEN"


def test_auth_me_rejects_expired_token(app: Flask, client: FlaskClient) -> None:
    with app.app_context():
        token = create_access_token(identity="1", expires_delta=timedelta(seconds=-1))

    response = client.get(ME_URL, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 401
    assert response.get_json()["error"]["code"] == "TOKEN_EXPIRED"


def test_auth_me_returns_not_found_when_token_user_no_longer_exists(
    app: Flask, client: FlaskClient
) -> None:
    with app.app_context():
        token = create_access_token(identity="999")

    response = client.get(ME_URL, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 404
    assert response.get_json()["error"]["code"] == "USER_NOT_FOUND"


def test_auth_me_rejects_non_numeric_subject(app: Flask, client: FlaskClient) -> None:
    with app.app_context():
        token = create_access_token(identity="not-a-user-id")

    response = client.get(ME_URL, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 401
    assert response.get_json()["error"]["code"] == "INVALID_TOKEN"
