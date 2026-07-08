import os
import joblib
import pandas as pd
import numpy as np

from utils.geo import haversine
from utils.osrm import get_route

from ai.predict_logistic import predict_acceptance

MODEL_DIR = "saved_models"

knn = joblib.load(
    os.path.join(MODEL_DIR, "knn.pkl")
)

scaler = joblib.load(
    os.path.join(MODEL_DIR, "knn_scaler.pkl")
)

DATASET = "data/ngo_locations.csv"


def recommend_ngos(

    donor_lat,

    donor_lon,

    food_type,

    quantity

):

    ngos = pd.read_csv(DATASET)

    features = scaler.transform(

        ngos[
            [
                "latitude",
                "longitude",
                "remaining_capacity"
            ]
        ]

    )

    donor_feature = scaler.transform([[
        donor_lat,
        donor_lon,
        quantity
    ]])

    distances, indices = knn.kneighbors(
        donor_feature
    )

    recommendations = []

    for idx in indices[0]:

        ngo = ngos.iloc[idx]

        hav_distance = haversine(

            donor_lat,
            donor_lon,

            ngo["latitude"],
            ngo["longitude"]

        )

        prediction = predict_acceptance(

            food_type,

            hav_distance,

            ngo["remaining_capacity"],

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

            distance = hav_distance
            eta = round(distance * 1.5)

        capacity_score = min(

            ngo["remaining_capacity"] / quantity,

            1

        )

        final_score = (

            0.40 * prediction["probability"]

            +

            0.35 * capacity_score

            +

            0.25 * (1 / (1 + distance))

        )

        recommendations.append({

            "ngo_id": int(ngo["ngo_id"]),

            "ngo_name": ngo["ngo_name"],

            "distance_km": round(distance, 2),

            "eta_minutes": eta,

            "accept_probability":

                round(
                    prediction["probability"],
                    2
                ),

            "capacity":

                int(
                    ngo["remaining_capacity"]
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

    return recommendations


if __name__ == "__main__":

    result = recommend_ngos(

        donor_lat=12.9716,

        donor_lon=77.5946,

        food_type="Veg",

        quantity=60

    )

    for ngo in result:

        print(ngo)