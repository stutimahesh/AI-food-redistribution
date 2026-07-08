import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


MODEL_DIR = "saved_models"
MODEL_PATH = os.path.join(MODEL_DIR, "logistic.pkl")

DATASET = "data/ngo_acceptance.csv"


def train():

    df = pd.read_csv(DATASET)

    # -------------------------
    # Encode food type
    # -------------------------

    encoder = LabelEncoder()

    df["food_type"] = encoder.fit_transform(
        df["food_type"]
    )

    X = df[
        [
            "food_type",
            "distance_km",
            "remaining_capacity",
            "quantity"
        ]
    ]

    y = df["accepted"]

    X_train, X_test, y_train, y_test = train_test_split(

        X,
        y,

        test_size=0.2,

        random_state=42

    )

    model = LogisticRegression(

        max_iter=1000

    )

    model.fit(

        X_train,
        y_train

    )

    prediction = model.predict(

        X_test

    )

    accuracy = accuracy_score(

        y_test,
        prediction

    )

    os.makedirs(
        MODEL_DIR,
        exist_ok=True
    )

    joblib.dump(

        model,
        MODEL_PATH

    )

    joblib.dump(

        encoder,

        os.path.join(
            MODEL_DIR,
            "food_encoder.pkl"
        )

    )

    print("--------------------------------")

    print("Training Completed")

    print("Accuracy :", round(accuracy * 100, 2), "%")

    print("--------------------------------")


if __name__ == "__main__":

    train()