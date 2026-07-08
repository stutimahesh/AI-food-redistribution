import os
import joblib
import numpy as np


MODEL_DIR = "saved_models"

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "logistic.pkl"
)

ENCODER_PATH = os.path.join(
    MODEL_DIR,
    "food_encoder.pkl"
)


model = joblib.load(MODEL_PATH)

encoder = joblib.load(ENCODER_PATH)


def predict_acceptance(

    food_type,

    distance,

    remaining_capacity,

    quantity

):

    try:

        food = encoder.transform(
            [food_type]
        )[0]

    except Exception:

        food = 0

    features = np.array(
        [[

            food,

            distance,

            remaining_capacity,

            quantity

        ]]
    )

    probability = model.predict_proba(
        features
    )[0][1]

    prediction = model.predict(
        features
    )[0]

    return {

        "accepted": bool(prediction),

        "probability": round(
            float(probability),
            4
        )

    }


if __name__ == "__main__":

    result = predict_acceptance(

        "Veg",

        4.5,

        300,

        50

    )

    print(result)