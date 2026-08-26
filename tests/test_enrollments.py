from collections.abc import Callable
from unittest.mock import patch

import pytest
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.enrollments.service import enroll_user
from app.errors import AlreadyEnrolledError
from app.extensions import db
from app.models import Enrollment, User
from tests.conftest import Course


def enroll_url(course_id: int) -> str:
    return f"/api/courses/{course_id}/enroll"


def login_headers(client: FlaskClient, email: str) -> dict[str, str]:
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": "secure-password"},
    )
    token = response.get_json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_enroll_creates_enrollment_for_authenticated_user(
    app: Flask,
    client: FlaskClient,
    auth_headers: dict[str, str],
    create_course: Callable[..., Course],
) -> None:
    course = create_course()

    response = client.post(enroll_url(course.id), headers=auth_headers)

    assert response.status_code == 201
    data = response.get_json()["data"]
    assert data["course_id"] == course.id
    assert data["user_id"] == 1
    with app.app_context():
        enrollment = db.session.scalar(select(Enrollment))
        assert enrollment is not None
        assert enrollment.course_id == course.id


def test_enroll_requires_authentication(
    client: FlaskClient, create_course: Callable[..., Course]
) -> None:
    course = create_course()

    response = client.post(enroll_url(course.id))

    assert response.status_code == 401
    assert response.get_json()["error"]["code"] == "AUTHENTICATION_REQUIRED"


def test_enroll_returns_not_found_for_unknown_course(
    client: FlaskClient, auth_headers: dict[str, str]
) -> None:
    response = client.post(enroll_url(999), headers=auth_headers)

    assert response.status_code == 404
    assert response.get_json()["error"]["code"] == "COURSE_NOT_FOUND"


def test_enroll_returns_conflict_for_duplicate_enrollment(
    client: FlaskClient,
    auth_headers: dict[str, str],
    create_course: Callable[..., Course],
) -> None:
    course = create_course()
    first_response = client.post(enroll_url(course.id), headers=auth_headers)

    second_response = client.post(enroll_url(course.id), headers=auth_headers)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.get_json()["error"]["code"] == "ALREADY_ENROLLED"


def test_database_unique_constraint_prevents_duplicate_enrollment(
    app: Flask,
    auth_headers: dict[str, str],
    create_course: Callable[..., Course],
) -> None:
    course = create_course()

    with app.app_context(), pytest.raises(IntegrityError):
        db.session.add_all(
            [
                Enrollment(user_id=1, course_id=course.id),
                Enrollment(user_id=1, course_id=course.id),
            ]
        )
        db.session.commit()


def test_enroll_ignores_user_id_from_request_body(
    app: Flask,
    client: FlaskClient,
    register: Callable[..., dict[str, object]],
    create_course: Callable[..., Course],
) -> None:
    first_user = register(email="first@example.com")
    second_user = register(email="second@example.com")
    course = create_course()
    headers = login_headers(client, "first@example.com")

    response = client.post(
        enroll_url(course.id),
        headers=headers,
        json={"user_id": second_user["id"]},
    )

    assert response.status_code == 201
    assert response.get_json()["data"]["user_id"] == first_user["id"]
    with app.app_context():
        enrollment = db.session.scalar(select(Enrollment))
        assert enrollment is not None
        assert enrollment.user_id == first_user["id"]


def test_session_is_usable_after_duplicate_enrollment_rollback(
    client: FlaskClient,
    auth_headers: dict[str, str],
    create_course: Callable[..., Course],
) -> None:
    first_course = create_course(title="Pães Artesanais")
    second_course = create_course(title="Massas Frescas")
    client.post(enroll_url(first_course.id), headers=auth_headers)
    duplicate = client.post(enroll_url(first_course.id), headers=auth_headers)

    next_enrollment = client.post(enroll_url(second_course.id), headers=auth_headers)

    assert duplicate.status_code == 409
    assert next_enrollment.status_code == 201


def test_enroll_rolls_back_when_unique_constraint_wins_a_race(
    app: Flask,
    auth_headers: dict[str, str],
    create_course: Callable[..., Course],
) -> None:
    course = create_course()

    with app.app_context():
        user = db.session.get(User, 1)
        assert user is not None
        integrity_error = IntegrityError("insert", {}, RuntimeError("duplicate"))

        with (
            patch.object(db.session, "commit", side_effect=integrity_error),
            patch.object(db.session, "rollback", wraps=db.session.rollback) as rollback,
            pytest.raises(AlreadyEnrolledError),
        ):
            enroll_user(user, course.id)

        rollback.assert_called_once_with()


def test_my_courses_returns_empty_list_for_user_without_enrollments(
    client: FlaskClient, auth_headers: dict[str, str]
) -> None:
    response = client.get("/api/users/me/courses", headers=auth_headers)

    assert response.status_code == 200
    assert response.get_json() == {"data": []}


def test_my_courses_returns_public_course_contract(
    client: FlaskClient,
    auth_headers: dict[str, str],
    create_course: Callable[..., Course],
) -> None:
    course = create_course()
    client.post(enroll_url(course.id), headers=auth_headers)

    response = client.get("/api/users/me/courses", headers=auth_headers)

    assert response.status_code == 200
    assert response.get_json()["data"] == [
        {
            "id": course.id,
            "title": "Pizza Napolitana",
            "description": "Fermentação e cocção da pizza napolitana.",
            "thumbnail_url": "https://example.com/pizza.jpg",
            "level": "BEGINNER",
        }
    ]


def test_my_courses_returns_multiple_courses_in_enrollment_order(
    client: FlaskClient,
    auth_headers: dict[str, str],
    create_course: Callable[..., Course],
) -> None:
    first_course = create_course(title="Panificação")
    second_course = create_course(title="Confeitaria")
    client.post(enroll_url(first_course.id), headers=auth_headers)
    client.post(enroll_url(second_course.id), headers=auth_headers)

    response = client.get("/api/users/me/courses", headers=auth_headers)

    assert [course["id"] for course in response.get_json()["data"]] == [
        first_course.id,
        second_course.id,
    ]


def test_my_courses_does_not_return_another_users_courses(
    client: FlaskClient,
    register: Callable[..., dict[str, object]],
    create_course: Callable[..., Course],
) -> None:
    register(email="first@example.com")
    register(email="second@example.com")
    first_course = create_course(title="Curso do primeiro usuário")
    second_course = create_course(title="Curso do segundo usuário")
    first_headers = login_headers(client, "first@example.com")
    second_headers = login_headers(client, "second@example.com")
    client.post(enroll_url(first_course.id), headers=first_headers)
    client.post(enroll_url(second_course.id), headers=second_headers)

    response = client.get("/api/users/me/courses", headers=first_headers)

    returned_ids = [course["id"] for course in response.get_json()["data"]]
    assert returned_ids == [first_course.id]


def test_my_courses_requires_authentication(client: FlaskClient) -> None:
    response = client.get("/api/users/me/courses")

    assert response.status_code == 401
    assert response.get_json()["error"]["code"] == "AUTHENTICATION_REQUIRED"


def test_enrollment_reports_unavailable_course_integration_when_table_is_missing(
    app: Flask, client: FlaskClient, auth_headers: dict[str, str]
) -> None:
    with app.app_context():
        Course.__table__.drop(db.engine)

    response = client.post(enroll_url(1), headers=auth_headers)

    assert response.status_code == 503
    assert response.get_json()["error"]["code"] == ("COURSE_INTEGRATION_UNAVAILABLE")


def test_health_check_returns_ok(client: FlaskClient) -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_cors_allows_configured_frontend_origin(client: FlaskClient) -> None:
    response = client.options(
        "/api/auth/register",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Authorization, Content-Type",
        },
    )

    assert response.headers["Access-Control-Allow-Origin"] == "http://localhost:3000"
    assert "Authorization" in response.headers["Access-Control-Allow-Headers"]


def test_cors_does_not_allow_unconfigured_origin(client: FlaskClient) -> None:
    response = client.options(
        "/api/auth/register",
        headers={
            "Origin": "https://untrusted.example",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert "Access-Control-Allow-Origin" not in response.headers


def test_user_email_has_database_unique_constraint(
    app: Flask,
) -> None:
    with app.app_context(), pytest.raises(IntegrityError):
        db.session.add_all(
            [
                User(
                    name="First",
                    email="duplicate@example.com",
                    password_hash="not-a-real-hash",
                ),
                User(
                    name="Second",
                    email="duplicate@example.com",
                    password_hash="not-a-real-hash",
                ),
            ]
        )
        db.session.commit()
