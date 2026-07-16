import os
import joblib
import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

MODEL_DIR = "saved_models"
MODEL_PATH = os.path.join(MODEL_DIR, "lstm.keras")
SCALER_PATH = os.path.join(MODEL_DIR, "lstm_scaler.pkl")

DATASET = "data/donation_history.csv"

LOOKBACK = 7


def create_dataset(dataset, lookback):

    X = []
    y = []

    for i in range(len(dataset) - lookback):

        X.append(dataset[i:i + lookback])

        y.append(dataset[i + lookback])

    return np.array(X), np.array(y)


def train():

    df = pd.read_csv(DATASET)

    values = df["total_quantity"].values.reshape(-1, 1)

    scaler = MinMaxScaler()

    scaled = scaler.fit_transform(values)

    X, y = create_dataset(
        scaled,
        LOOKBACK
    )

    X = X.reshape(
        X.shape[0],
        X.shape[1],
        1
    )

    model = Sequential()

    model.add(
        LSTM(
            64,
            input_shape=(LOOKBACK, 1)
        )
    )

    model.add(Dense(32, activation="relu"))

    model.add(Dense(1))

    model.compile(

        optimizer="adam",

        loss="mse"

    )

    model.fit(

        X,

        y,

        epochs=50,

        batch_size=8,

        verbose=1

    )

    os.makedirs(
        MODEL_DIR,
        exist_ok=True
    )

    model.save(MODEL_PATH)

    joblib.dump(
        scaler,
        SCALER_PATH
    )

    print("LSTM Model Saved Successfully")


if __name__ == "__main__":
    train()