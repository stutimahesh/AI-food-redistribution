from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from database.db import init_db

# Import Routes
from routes.auth import auth_bp
from routes.donor import donor_bp
from routes.ngo import ngo_bp
from routes.driver import driver_bp
from routes.recommendation import recommendation_bp


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    # Enable CORS
    CORS(
        app,
        resources={r"/*": {"origins": "*"}}
    )

    # JWT
    JWTManager(app)

    # Initialize Database
    init_db(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(donor_bp, url_prefix="/api/donor")
    app.register_blueprint(ngo_bp, url_prefix="/api/ngo")
    app.register_blueprint(driver_bp, url_prefix="/api/driver")
    app.register_blueprint(
        recommendation_bp,
        url_prefix="/api/recommendation"
    )

    @app.route("/")
    def home():
        return {
            "project": "NourishNet",
            "version": "1.0",
            "status": "Running"
        }

    @app.route("/health")
    def health():
        return {
            "database": "Connected",
            "server": "Healthy"
        }

    return app


app = create_app()

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )