import logging
from flask import Blueprint, request, redirect, url_for, session
from zenora import APIClient

from  ..config import OAUTH_URL, REDIRECT_URI, CLIENT_SECRET, TOKEN
from .api import core


log = logging.getLogger(__name__)
account_sys = Blueprint("account_sys", __name__)
if TOKEN is not None: 
    client = APIClient(TOKEN, client_secret=CLIENT_SECRET, validate_token=False)
else:
    log.warning("No token provided.")


@account_sys.route("/oauth/callback")
def callback():
    if "code" in request.args:
        code = request.args["code"]
        access_token = client.oauth.get_access_token(code, REDIRECT_URI).access_token
        bearer_client = APIClient(access_token, bearer=True)
        current_user = bearer_client.users.get_current_user()
        session["token"] = access_token
        session.permanent = True
        team, is_admin = core.check_player(current_user.id)
        
        if is_admin:
            return redirect("/admin")
        
    return redirect("/")


@account_sys.route("/login")
def login():
    if OAUTH_URL is None:
        return redirect(url_for("main.index", message="No OAuth"))
    return redirect(OAUTH_URL)


@account_sys.route("/logout")
def logout():
    session.clear()
    return redirect("/")