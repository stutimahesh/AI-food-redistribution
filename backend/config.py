import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    # -----------------------------
    # Flask
    # -----------------------------
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "nourishnet_secret_key"
    )

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "jwt_secret_key"
    )

    # -----------------------------
    # PostgreSQL
    # -----------------------------
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "nourishnet")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # -----------------------------
    # Google Maps
    # -----------------------------
    GOOGLE_MAPS_API_KEY = os.getenv(
        "GOOGLE_MAPS_API_KEY",
        ""
    )

    # -----------------------------
    # OSRM
    # -----------------------------
    OSRM_BASE_URL = os.getenv(
        "OSRM_BASE_URL",
        "https://router.project-osrm.org"
    )

    # -----------------------------
    # AI Model Paths
    # -----------------------------
    MODEL_FOLDER = "saved_models"

    KNN_MODEL = os.path.join(
        MODEL_FOLDER,
        "knn.pkl"
    )

    RF_MODEL = os.path.join(
        MODEL_FOLDER,
        "rf.pkl"
    )

    LOGISTIC_MODEL = os.path.join(
        MODEL_FOLDER,
        "logistic.pkl"
    )

    LSTM_MODEL = os.path.join(
        MODEL_FOLDER,
        "lstm.keras"
    )

    # -----------------------------
    # Uploads
    # -----------------------------
    UPLOAD_FOLDER = "uploads"

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # -----------------------------
    # Logging
    # -----------------------------
    LOG_FILE = "logs/server.log"