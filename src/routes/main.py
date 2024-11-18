"""Utility functions for flask app."""

from flask import Blueprint, Flask, make_response

bp = Blueprint("routes", __name__)


def register_routes(app: Flask) -> None:
    """Register all routes with the Flask app."""
    app.register_blueprint(bp)


@bp.route("/ready")
def ready():
    """Return a 200 response."""
    return make_response("app is ready", 200)
