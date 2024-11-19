"""Main file setsup and runs the flask app."""

from flask import Flask
from flask_cors import CORS

from routes import register_routes

app = Flask(__name__)
CORS(app)
register_routes(app)
