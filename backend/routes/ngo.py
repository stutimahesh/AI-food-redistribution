from flask import Blueprint
from flask import request
from flask import jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from database.db import db

from models.ngo import NGO
from models.user import User
from models.donation import Donation

ngo_bp = Blueprint(
    "ngo",
    __name__
)

##################################################
# Create NGO Profile
##################################################

@ngo_bp.route("/profile", methods=["POST"])
@jwt_required()
def create_profile():

    user_id = get_jwt_identity()

    existing = NGO.query.filter_by(
        user_id=user_id
    ).first()

    if existing:

        return jsonify({

            "message":
            "NGO profile already exists."

        }), 400

    data = request.get_json()

    ngo = NGO(

        user_id=user_id,

        ngo_name=data["ngo_name"],

        address=data["address"],

        latitude=data["latitude"],

        longitude=data["longitude"],

        max_capacity=data["max_capacity"]

    )

    db.session.add(ngo)

    db.session.commit()

    return jsonify({

        "message":
        "NGO profile created",

        "ngo":
        ngo.to_dict()

    })


##################################################
# View Available Donations
##################################################

@ngo_bp.route("/donations", methods=["GET"])
@jwt_required()
def available_donations():

    donations = Donation.query.filter_by(
        status="Pending"
    ).all()

    return jsonify([

        donation.to_dict()

        for donation in donations

    ])


##################################################
# Accept Donation
##################################################

@ngo_bp.route(
    "/accept/<int:donation_id>",
    methods=["POST"]
)
@jwt_required()
def accept_donation(donation_id):

    user_id = get_jwt_identity()

    ngo = NGO.query.filter_by(
        user_id=user_id
    ).first()

    if ngo is None:

        return jsonify({

            "message":
            "NGO profile not found"

        }), 404

    donation = Donation.query.get(
        donation_id
    )

    if donation is None:

        return jsonify({

            "message":
            "Donation not found"

        }), 404

    if donation.status != "Pending":

        return jsonify({

            "message":
            "Already processed"

        }), 400

    donation.status = "Accepted"

    ngo.current_capacity += donation.quantity

    db.session.commit()

    return jsonify({

        "message":
        "Donation accepted",

        "ngo_capacity":
        ngo.remaining_capacity

    })


##################################################
# Reject Donation
##################################################

@ngo_bp.route(
    "/reject/<int:donation_id>",
    methods=["POST"]
)
@jwt_required()
def reject_donation(donation_id):

    donation = Donation.query.get(
        donation_id
    )

    if donation is None:

        return jsonify({

            "message":
            "Donation not found"

        }), 404

    donation.status = "Rejected"

    db.session.commit()

    return jsonify({

        "message":
        "Donation rejected"

    })


##################################################
# NGO Dashboard
##################################################

@ngo_bp.route("/dashboard")
@jwt_required()
def dashboard():

    user_id = get_jwt_identity()

    ngo = NGO.query.filter_by(
        user_id=user_id
    ).first()

    if ngo is None:

        return jsonify({

            "message":
            "Profile not found"

        }), 404

    pending = Donation.query.filter_by(
        status="Pending"
    ).count()

    accepted = Donation.query.filter_by(
        status="Accepted"
    ).count()

    return jsonify({

        "ngo": ngo.to_dict(),

        "pending_donations": pending,

        "accepted_donations": accepted

    })