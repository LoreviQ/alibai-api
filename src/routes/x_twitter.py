"""Routes regarding x.com."""

import base64
import hashlib
import logging
import os
import secrets
import urllib.parse
from datetime import datetime, timedelta, timezone

import requests
from flask import jsonify, make_response, request

import database as db

from .main import bp

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

CLIENT_ID = os.getenv("X_CLIENT_ID")
CLIENT_SECRET = os.getenv("X_CLIENT_SECRET")
SCOPES = ["tweet.read", "tweet.write", "users.read", "offline.access"]
CALLBACK_URL = "https://alibai-client.onrender.com/link_account/x/callback"


session = {}


@bp.route("/v1/auth/oauth/x/redirect", methods=["GET"])
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
        "redirect_uri": CALLBACK_URL,
        "scope": " ".join(SCOPES),
        "state": state,
        "code_challenge_method": "S256",
        "code_challenge": code_challenge,
    }
    authorization_url = f"{auth_url}?{urllib.parse.urlencode(params)}"

    session["state"] = state
    session["code_verifier"] = code_verifier

    return make_response({"authorization_url": authorization_url}, 200)


@bp.route("/v1/auth/oauth/x/callback", methods=["POST"])
def x_auth_callback():
    """Store the data from the Twitter Oauth event."""
    data = request.json
    code = data.get("code")
    state = data.get("state")

    logger.debug("Received callback with code: %s, state: %s", code, state)

    if state != session["state"]:
        return make_response("Invalid state parameter", 400)

    # Exchange code for access token
    token_url = "https://api.twitter.com/2/oauth2/token"
    request_data = {
        "code": code,
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "redirect_uri": CALLBACK_URL,
        "code_verifier": session["code_verifier"],
    }

    logger.debug("Token request data: %s", request_data)
    logger.debug("Client ID length: %d", len(CLIENT_ID) if CLIENT_ID else 0)
    logger.debug("Client Secret length: %d", len(CLIENT_SECRET) if CLIENT_SECRET else 0)

    # Get tokens using the code
    token_response = requests.post(
        token_url, data=request_data, auth=(CLIENT_ID, CLIENT_SECRET), timeout=5
    )
    logger.debug("Token response status: %d", token_response.status_code)
    logger.debug("Token response body: %s", token_response.text)
    if token_response.status_code != 200:
        logger.error(
            "Token exchange failed with status %d: %s",
            token_response.status_code,
            token_response.text,
        )
        return make_response(
            f"Failed to exchange code for access token: {token_response.text}", 400
        )
    token_data = token_response.json()
    expires_at = datetime.now(timezone.utc) + timedelta(
        seconds=token_data["expires_in"]
    )
    access_token = token_data["access_token"]

    # Get user information using the access token
    user_response = requests.get(
        "https://api.twitter.com/2/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=5,
    )
    if user_response.status_code != 200:
        return make_response("Failed to get user information", 400)
    user_data = user_response.json()
    username = user_data["data"]["username"]
    # store user information in database
    user = db.User(
        x_user_id=user_data["data"]["id"],
        x_username=username,
    )
    matching_user = db.select_users(user)
    if matching_user:
        user_id = matching_user[0]["id"]
    else:
        user_id = db.insert_user(user)
    token = db.OAuthToken(
        user_id=user_id,
        access_token=access_token,
        refresh_token=token_data["refresh_token"],
        expires_at=expires_at,
    )
    db.update_or_insert_oauth_token(token)
    response = {"userid": str(user_id), "username": username}
    return make_response(jsonify(response), 200)
