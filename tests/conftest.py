from collections.abc import Callable, Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app import create_app
from app.extensions import db


class Course(db.Model):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500))
    thumbnail_url: Mapped[str | None] = mapped_column(String(500))
    level: Mapped[str] = mapped_column(String(30), nullable=False)


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    application = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "JWT_SECRET_KEY": "test-only-secret-key-with-sufficient-length",
            "JWT_ACCESS_TOKEN_EXPIRES": 3600,
            "CORS_ALLOWED_ORIGINS": ["http://localhost:3000"],
        }
    )

    with application.app_context():
        db.create_all()

    yield application

    with application.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture
def register(client: FlaskClient) -> Callable[..., dict[str, object]]:
    def register_user(
        email: str = "student@example.com",
        password: str = "secure-password",
        name: str = "Student User",
    ) -> dict[str, object]:
        response = client.post(
            "/api/auth/register",
            json={
                "name": name,
                "email": email,
                "password": password,
                "password_confirmation": password,
            },
        )
        assert response.status_code == 201
        return response.get_json()["data"]

    return register_user


@pytest.fixture
def auth_headers(
    client: FlaskClient, register: Callable[..., dict[str, object]]
) -> dict[str, str]:
    register()
    response = client.post(
        "/api/auth/login",
        json={"email": "student@example.com", "password": "secure-password"},
    )
    token = response.get_json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def create_course(app: Flask) -> Callable[..., Course]:
    def factory(
        title: str = "Pizza Napolitana",
        description: str = "Fermentação e cocção da pizza napolitana.",
        thumbnail_url: str = "https://example.com/pizza.jpg",
        level: str = "BEGINNER",
    ) -> Course:
        with app.app_context():
            course = Course(
                title=title,
                description=description,
                thumbnail_url=thumbnail_url,
                level=level,
            )
            db.session.add(course)
            db.session.commit()
            db.session.refresh(course)
            db.session.expunge(course)
            return course

    return factory
