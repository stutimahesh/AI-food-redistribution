from datetime import datetime

import pandas as pd

from ai.predict_capacity import predict_capacity
from ai.predict_logistic import predict_acceptance

from utils.geo import haversine
from utils.osrm import get_route


NGO_DATA = "data/ngo_locations.csv"


def generate_recommendations(

    donor_lat,
    donor_lon,

    food_type,
    quantity

):

    ngos = pd.read_csv(NGO_DATA)

    recommendations = []

    today = datetime.now()

    day = today.weekday() + 1
    month = today.month

    for _, ngo in ngos.iterrows():

        predicted_capacity = predict_capacity(

            day,

            month,

            ngo["remaining_capacity"],

            ngo["remaining_capacity"] * 0.30

        )

        distance = haversine(

            donor_lat,
            donor_lon,

            ngo["latitude"],
            ngo["longitude"]

        )

        probability = predict_acceptance(

            food_type,

            distance,

            predicted_capacity,

            quantity

        )

        route = get_route(

            donor_lat,
            donor_lon,

            ngo["latitude"],
            ngo["longitude"]

        )

        if route:

            distance = route["distance_km"]
            eta = route["duration_minutes"]

        else:

            eta = round(distance * 2)

        capacity_score = min(
            predicted_capacity / quantity,
            1
        )

        final_score = (

            0.45 * probability["probability"]

            +

            0.35 * capacity_score

            +

            0.20 * (1 / (1 + distance))

        )

        recommendations.append({

            "ngo_id": int(ngo["ngo_id"]),

            "ngo_name": ngo["ngo_name"],

            "predicted_capacity":
            predicted_capacity,

            "distance_km":
            round(distance, 2),

            "eta":
            eta,

            "acceptance_probability":

            round(
                probability["probability"],
                2
            ),

            "score":

            round(
                final_score,
                4
            )

        })

    recommendations.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    return recommendations[:5]