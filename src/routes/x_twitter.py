"""Routes regarding x.com."""

import base64
import hashlib
import os
import secrets
import urllib.parse
from datetime import datetime, timedelta, timezone

import requests
from flask import make_response, redirect, request, url_for

import database as db

from .main import bp

CLIENT_ID = os.getenv("X_CLIENT_ID")
CLIENT_SECRET = os.getenv("X_CLIENT_SECRET")
SCOPES = ["tweet.read", "tweet.write", "users.read", "offline.access"]
CALLBACK = url_for("main.x_auth_callback", _external=True)

session = {}


@bp.route("/auth/link_account/x")
def x_auth():
    """Redirect to Twitter authorization page."""
    # Generate state parameter for security
    state = secrets.token_urlsafe(32)
    auth_url = "https://twitter.com/i/oauth2/authorize"
    code_verifier = secrets.token_urlsafe(32)
    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest())
        .rstrip(b"=")
        .decode()
    )
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": CALLBACK,
        "scope": " ".join(SCOPES),
        "state": state,
        "code_challenge_method": "S256",
        "code_challenge": code_challenge,
    }
    authorization_url = f"{auth_url}?{urllib.parse.urlencode(params)}"

    session["state"] = state
    session["code_verifier"] = code_verifier

    return redirect(authorization_url)


@bp.route("/auth/link_account/x/callback")
def x_auth_callback():
    """Handle callback from Twitter authorization page."""
    error = request.args.get("error")
    if error:
        return make_response(f"Authorization failed: {error}", 400)

    code = request.args.get("code")
    state = request.args.get("state")

    if state != session["state"]:
        return make_response("Invalid state parameter", 400)

    # Exchange code for access token
    token_url = "https://api.twitter.com/2/oauth2/token"
    data = {
        "code": code,
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "redirect_uri": CALLBACK,
        "code_verifier": session["code_verifier"],
    }

    response = requests.post(
        token_url, data=data, auth=(CLIENT_ID, CLIENT_SECRET), timeout=5
    )
    if response.status_code != 200:
        return make_response("Failed to exchange code for access token", 400)

    tokens = response.json()
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=tokens["expires_in"])
    user_id = db.insert_user(db.User(x_user_id=tokens["user_id"]))
    token = db.OAuthToken(
        user_id=user_id,
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        expires_at=expires_at,
    )
    db.insert_oauth_token(token)
    return redirect("/success")


@bp.route("/success")
def success():
    """Return a 200 response."""
    return make_response("Success", 200)
