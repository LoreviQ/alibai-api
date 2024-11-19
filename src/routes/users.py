"""Routes regarding users."""

from flask import make_response

import database as db

from .main import bp


@bp.route("/v1/users", methods=["POST"])
def post_user():
    """Create a new user (Currently hardcoded for testing)"""
    user = db.User(
        x_user_id="123456789",
        x_username="loreviq",
    )
    db.insert_user(user)
    return make_response("user created", 201)
