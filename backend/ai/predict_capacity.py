import os
import joblib
import numpy as np

MODEL_DIR = "saved_models"

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "random_forest.pkl"
)

model = joblib.load(MODEL_PATH)


def predict_capacity(

    day_of_week,

    month,

    historical_avg,

    current_load

):

    features = np.array(
        [[

            day_of_week,

            month,

            historical_avg,

            current_load

        ]]
    )

    prediction = model.predict(
        features
    )[0]

    prediction = max(
        0,
        round(float(prediction))
    )

    return prediction


if __name__ == "__main__":

    capacity = predict_capacity(

        day_of_week=3,

        month=7,

        historical_avg=250,

        current_load=80

    )

    print("Predicted Capacity:", capacity)