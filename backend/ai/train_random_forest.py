import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

MODEL_DIR = "saved_models"
MODEL_PATH = os.path.join(MODEL_DIR, "random_forest.pkl")

DATASET = "data/ngo_capacity.csv"


def train():

    df = pd.read_csv(DATASET)

    X = df[
        [
            "day_of_week",
            "month",
            "historical_avg",
            "current_load"
        ]
    ]

    y = df["remaining_capacity"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        random_state=42
    )

    model.fit(X_train, y_train)

    prediction = model.predict(X_test)

    rmse = mean_squared_error(
        y_test,
        prediction,
        squared=False
    )

    r2 = r2_score(
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

    print("--------------------------------")
    print("Random Forest Trained")
    print("RMSE :", round(rmse,2))
    print("R2   :", round(r2,2))
    print("--------------------------------")


if __name__ == "__main__":
    train()