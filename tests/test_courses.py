from flask import Flask

from app.extensions import db
from app.models import Course, CourseStatus, Lesson, Module


def test_empty_catalog(client) -> None:
    response = client.get("/api/courses")
    assert response.status_code == 200
    assert response.get_json() == {"data": []}


def test_catalog_search_and_filters(client, create_course) -> None:
    pizza = create_course(title="Pizza Napolitana")
    create_course(title="Bolos Decorados", level="INTERMEDIATE")

    response = client.get("/api/courses?search=pIzZa&category=pizzas&level=beginner")

    assert response.status_code == 200
    assert [item["id"] for item in response.get_json()["data"]] == [pizza.id]
    assert response.get_json()["data"][0]["category"]["slug"] == "pizzas"
    assert set(response.get_json()["data"][0]) == {
        "id",
        "title",
        "description",
        "thumbnail_url",
        "level",
        "category",
        "instructor",
    }


def test_catalog_hides_drafts(client, app: Flask, create_course) -> None:
    course = create_course()
    with app.app_context():
        db.session.get(Course, course.id).status = CourseStatus.DRAFT
        db.session.commit()

    assert client.get("/api/courses").get_json() == {"data": []}


def test_invalid_level_is_consistent_error(client) -> None:
    response = client.get("/api/courses?level=expert")
    assert response.status_code == 422
    assert response.get_json()["error"]["code"] == "VALIDATION_ERROR"


def test_course_detail_orders_modules_and_lessons(client, app, create_course) -> None:
    course = create_course()
    with app.app_context():
        stored = db.session.get(Course, course.id)
        second = Module(course=stored, title="Segundo", position=2)
        first = Module(course=stored, title="Primeiro", position=1)
        second.lessons.extend(
            [
                Lesson(title="B", video_url="https://example.com/b", position=2),
                Lesson(title="A", video_url="https://example.com/a", position=1),
            ]
        )
        db.session.add(first)
        db.session.commit()

    response = client.get(f"/api/courses/{course.id}")
    data = response.get_json()["data"]
    assert response.status_code == 200
    assert [module["position"] for module in data["modules"]] == [1, 2]
    assert [lesson["position"] for lesson in data["modules"][1]["lessons"]] == [1, 2]


def test_course_not_found(client) -> None:
    response = client.get("/api/courses/999")
    assert response.status_code == 404
    assert response.get_json()["error"]["code"] == "COURSE_NOT_FOUND"


def test_categories(client, create_course) -> None:
    create_course()
    assert client.get("/api/categories").get_json() == {
        "data": [{"id": 1, "name": "Pizzas", "slug": "pizzas"}]
    }


def test_real_course_integrates_with_enrollment(
    client, auth_headers, create_course
) -> None:
    course = create_course()
    enrolled = client.post(
        f"/api/courses/{course.id}/enroll", headers=auth_headers
    )
    mine = client.get("/api/users/me/courses", headers=auth_headers)

    assert enrolled.status_code == 201
    assert mine.status_code == 200
    assert mine.get_json()["data"] == [
        {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "thumbnail_url": course.thumbnail_url,
            "level": "BEGINNER",
        }
    ]
