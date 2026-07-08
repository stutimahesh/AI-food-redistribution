import os
import joblib
import pandas as pd

from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

MODEL_DIR = "saved_models"
MODEL_PATH = os.path.join(MODEL_DIR, "knn.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "knn_scaler.pkl")

DATASET = "data/ngo_locations.csv"


def train():

    df = pd.read_csv(DATASET)

    features = df[
        [
            "latitude",
            "longitude",
            "remaining_capacity"
        ]
    ]

    scaler = StandardScaler()

    X = scaler.fit_transform(features)

    model = NearestNeighbors(

        n_neighbors=5,

        algorithm="ball_tree"

    )

    model.fit(X)

    os.makedirs(
        MODEL_DIR,
        exist_ok=True
    )

    joblib.dump(model, MODEL_PATH)

    joblib.dump(scaler, SCALER_PATH)

    print("---------------------------------")
    print("KNN Model Trained Successfully")
    print("---------------------------------")


if __name__ == "__main__":
    train()