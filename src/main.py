"""Main file setsup and runs the flask app."""

import os

from flask import Flask
from flask_cors import CORS

import database as db
from routes import register_routes


def initialize_app() -> Flask:
    """Initialize the flask app."""
    app = Flask(__name__)
    CORS(app)
    register_routes(app)
    return app


def run_app(app: Flask) -> None:
    """Run the flask app."""
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    db.create_db()
    flask_app = initialize_app()
    run_app(flask_app)
