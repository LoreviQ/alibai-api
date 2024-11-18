"""Flask app setup."""

import os

from flask import Flask
from flask_cors import CORS

from routes import register_routes


class App:
    """Class for flask app"""

    def __init__(self) -> None:
        self.port = int(os.getenv("PORT", "5000"))
        self.app = Flask(__name__)
        CORS(self.app)
        register_routes(self.app)

    def serve(self) -> None:
        """Start the Flask app."""
        self.app.run(host="0.0.0.0", port=self.port)
