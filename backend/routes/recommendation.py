from flask import Blueprint
from flask import jsonify
from flask import request

from flask_jwt_extended import (
    jwt_required
)

from ai.pipeline import generate_recommendations


recommendation_bp = Blueprint(

    "recommendation",

    __name__

)


##########################################################
# AI Recommendation API
##########################################################

@recommendation_bp.route(
    "/predict",
    methods=["POST"]
)
@jwt_required()
def recommend():

    data = request.get_json()

    donor_lat = data["latitude"]

    donor_lon = data["longitude"]

    food_type = data["food_type"]

    quantity = data["quantity"]

    recommendations = generate_recommendations(

        donor_lat,

        donor_lon,

        food_type,

        quantity

    )

    return jsonify({

        "success": True,

        "count": len(recommendations),

        "recommendations": recommendations

    })