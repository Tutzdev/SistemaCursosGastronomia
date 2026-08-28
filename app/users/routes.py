from flask import Blueprint, Response, jsonify
from flask_jwt_extended import jwt_required

from app.auth.service import get_current_user
from app.enrollments.service import list_user_courses
from app.serializers import serialize_scalar

users_blueprint = Blueprint("users", __name__, url_prefix="/api/users")


@users_blueprint.get("/me/courses")
@jwt_required()
def my_courses() -> tuple[Response, int]:
    courses = list_user_courses(get_current_user())
    data = [
        {key: serialize_scalar(value) for key, value in course.items()}
        for course in courses
    ]

    return jsonify({"data": data}), 200
