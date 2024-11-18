"""Utility functions for flask app."""

from flask import Blueprint, Flask

bp = Blueprint("routes", __name__)


def register_routes(app: Flask) -> None:
    """Register all routes with the Flask app."""
    app.register_blueprint(bp)


# declare routes like:
#
# @bp.route("/example")
# def example():
#     return make_response("example response", 200)
