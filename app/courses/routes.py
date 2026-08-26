from flask import Blueprint, Response, jsonify, request

from app.courses.serializers import serialize_category, serialize_course
from app.courses.service import get_course, list_categories, list_courses

courses_blueprint = Blueprint("courses", __name__, url_prefix="/api")


@courses_blueprint.get("/courses")
def courses() -> tuple[Response, int]:
    items = list_courses(
        request.args.get("search"),
        request.args.get("category"),
        request.args.get("level"),
    )
    return jsonify({"data": [serialize_course(item) for item in items]}), 200


@courses_blueprint.get("/courses/<int:course_id>")
def course_detail(course_id: int) -> tuple[Response, int]:
    return jsonify({"data": serialize_course(get_course(course_id), detailed=True)}), 200


@courses_blueprint.get("/categories")
def categories() -> tuple[Response, int]:
    return jsonify({"data": [serialize_category(item) for item in list_categories()]}), 200
