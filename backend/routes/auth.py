from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token
)

from database.db import db
from models.user import User

auth_bp = Blueprint(
    "auth",
    __name__
)


# -----------------------------------------
# Register
# -----------------------------------------

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")
    role = data.get("role")

    if not full_name or not email or not password or not role:

        return jsonify({
            "message": "Missing required fields."
        }), 400

    existing = User.query.filter_by(
        email=email
    ).first()

    if existing:

        return jsonify({
            "message": "Email already exists."
        }), 409

    user = User(
        full_name=full_name,
        email=email,
        phone=phone,
        role=role
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({

        "message": "Registration Successful",

        "user": user.to_dict()

    }), 201


# -----------------------------------------
# Login
# -----------------------------------------

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:

        return jsonify({
            "message": "Email and Password required."
        }), 400

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:

        return jsonify({
            "message": "User not found."
        }), 404

    if not user.check_password(password):

        return jsonify({
            "message": "Incorrect Password."
        }), 401

    access_token = create_access_token(

        identity=user.id,

        additional_claims={
            "role": user.role
        }
    )

    return jsonify({

        "message": "Login Successful",

        "token": access_token,

        "user": user.to_dict()

    }), 200


# -----------------------------------------
# Get Current User
# -----------------------------------------

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    return jsonify(user.to_dict())