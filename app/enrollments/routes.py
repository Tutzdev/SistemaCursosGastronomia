from flask import Blueprint, Response, jsonify
from flask_jwt_extended import jwt_required

from app.auth.service import get_current_user
from app.enrollments.service import enroll_user
from app.serializers import serialize_enrollment

enrollments_blueprint = Blueprint("enrollments", __name__, url_prefix="/api")


@enrollments_blueprint.post("/courses/<int:course_id>/enroll")
@jwt_required()
def enroll(course_id: int) -> tuple[Response, int]:
    enrollment = enroll_user(get_current_user(), course_id)

    return jsonify({"data": serialize_enrollment(enrollment)}), 201
