import logging
from flask import Blueprint, request, redirect, render_template, session
from zenora import APIClient

from  ..config import OAUTH_URL, REDIRECT_URI, CLIENT_SECRET, TOKEN


log = logging.getLogger(__name__)
account_sys = Blueprint("account_sys", __name__)
if TOKEN is not None: 
    client = APIClient(TOKEN, client_secret=CLIENT_SECRET, validate_token=False)


@account_sys.route("/oauth/callback")
def callback():
    if "code" in request.args:
        code = request.args["code"]
        access_token = client.oauth.get_access_token(code, REDIRECT_URI).access_token
        session["token"] = access_token
        session.permanent = True
        
    return redirect("/")


@account_sys.route("/login")
def login():
    if OAUTH_URL is None:
        return redirect("/")
    return redirect(OAUTH_URL)


@account_sys.route("/logout")
def logout():
    session.clear()
    return redirect("/")