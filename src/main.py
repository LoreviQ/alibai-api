"""Main file setsup and runs the flask app."""

import os

from flask import Flask
from flask_cors import CORS

from routes import register_routes

app = Flask(__name__)
CORS(app)
register_routes(app)
port = int(os.getenv("PORT", "5000"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
