from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from database.db import db

from models.driver import Driver
from models.delivery import Delivery

driver_bp = Blueprint(
    "driver",
    __name__
)


###################################################
# Create Driver Profile
###################################################

@driver_bp.route("/profile", methods=["POST"])
@jwt_required()
def create_driver():

    user_id = get_jwt_identity()

    if Driver.query.filter_by(
        user_id=user_id
    ).first():

        return jsonify({
            "message":
            "Driver profile already exists."
        }), 400

    data = request.get_json()

    driver = Driver(

        user_id=user_id,

        vehicle_type=data["vehicle_type"],

        vehicle_number=data["vehicle_number"],

        phone=data["phone"],

        current_latitude=data["latitude"],

        current_longitude=data["longitude"]

    )

    db.session.add(driver)

    db.session.commit()

    return jsonify({

        "message":
        "Driver Created",

        "driver":
        driver.to_dict()

    })


###################################################
# Update Driver Location
###################################################

@driver_bp.route(
    "/location",
    methods=["PUT"]
)
@jwt_required()
def update_location():

    user_id = get_jwt_identity()

    driver = Driver.query.filter_by(
        user_id=user_id
    ).first()

    if driver is None:

        return jsonify({

            "message":
            "Driver not found"

        }),404

    data = request.get_json()

    driver.current_latitude = data["latitude"]

    driver.current_longitude = data["longitude"]

    db.session.commit()

    return jsonify({

        "message":
        "Location Updated"

    })


###################################################
# Assigned Deliveries
###################################################

@driver_bp.route(
    "/deliveries"
)
@jwt_required()
def deliveries():

    user_id = get_jwt_identity()

    driver = Driver.query.filter_by(
        user_id=user_id
    ).first()

    assigned = Delivery.query.filter_by(

        driver_id=driver.id

    ).all()

    return jsonify([

        item.to_dict()

        for item in assigned

    ])


###################################################
# Start Delivery
###################################################

@driver_bp.route(
    "/start/<int:id>",
    methods=["POST"]
)
@jwt_required()
def start_delivery(id):

    delivery = Delivery.query.get(id)

    if delivery is None:

        return jsonify({

            "message":
            "Delivery not found"

        }),404

    delivery.delivery_status = "In Transit"

    delivery.pickup_time = datetime.utcnow()

    db.session.commit()

    return jsonify({

        "message":
        "Delivery Started"

    })


###################################################
# Complete Delivery
###################################################

@driver_bp.route(
    "/complete/<int:id>",
    methods=["POST"]
)
@jwt_required()
def complete_delivery(id):

    delivery = Delivery.query.get(id)

    if delivery is None:

        return jsonify({

            "message":
            "Delivery not found"

        }),404

    delivery.delivery_status = "Delivered"

    delivery.delivered_time = datetime.utcnow()

    driver = Driver.query.get(
        delivery.driver_id
    )

    driver.available = True

    db.session.commit()

    return jsonify({

        "message":
        "Delivery Completed"

    })


###################################################
# Driver Dashboard
###################################################

@driver_bp.route(
    "/dashboard"
)
@jwt_required()
def dashboard():

    user_id = get_jwt_identity()

    driver = Driver.query.filter_by(
        user_id=user_id
    ).first()

    assigned = Delivery.query.filter_by(

        driver_id=driver.id

    ).count()

    completed = Delivery.query.filter_by(

        driver_id=driver.id,

        delivery_status="Delivered"

    ).count()

    return jsonify({

        "driver":
        driver.to_dict(),

        "assigned":
        assigned,

        "completed":
        completed

    })