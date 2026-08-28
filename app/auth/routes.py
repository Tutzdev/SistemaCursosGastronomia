from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import jwt_required

from app.auth.service import authenticate_user, get_current_user, register_user
from app.auth.validation import validate_login_payload, validate_registration_payload
from app.serializers import serialize_user

auth_blueprint = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_blueprint.post("/register")
def register() -> tuple[Response, int]:
    data = validate_registration_payload(request.get_json(silent=True))
    user = register_user(data)

    return jsonify({"data": serialize_user(user)}), 201


@auth_blueprint.post("/login")
def login() -> tuple[Response, int]:
    data = validate_login_payload(request.get_json(silent=True))
    access_token = authenticate_user(data)

    return jsonify(
        {"data": {"access_token": access_token, "token_type": "bearer"}}
    ), 200


@auth_blueprint.get("/me")
@jwt_required()
def me() -> tuple[Response, int]:
    return jsonify({"data": serialize_user(get_current_user())}), 200
