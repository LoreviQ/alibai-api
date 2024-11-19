"""Routes regarding x.com."""

from flask import make_response

from .main import bp


@bp.route("/auth/link_account/x")
def x_auth():
    return make_response("", 200)
