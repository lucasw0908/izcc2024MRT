import logging
from flask import Blueprint, Response, render_template, redirect, session, request
from zenora import APIClient

from ..core import core

core.create_team("test", ["0"], ["e04._.40e", "a.uuu", "lucasw0"])

log = logging.getLogger(__name__)
main = Blueprint("main", __name__)


@main.after_request
def checking(response: Response):
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "deny"
    return response
    

@main.route("/")
def index():
    message = request.args.get("message")
    if message == "No OAuth":
        return render_template("index.html")
    if session.get("token"):
        bearer_client = APIClient(session.get("token"), bearer=True)
        current_user = bearer_client.users.get_current_user()
        team, _ = core.check_player(current_user.username)
        return render_template("index.html", current_user=current_user.username, team=team)
    return redirect("/login")


@main.route("/admin")
def admin():
    if "token" in session:
        bearer_client = APIClient(session.get("token"), bearer=True)
        current_user = bearer_client.users.get_current_user()
        team, is_admin = core.check_player(current_user.username)
    
        if is_admin:
            return render_template("admin.html", current_user=current_user.username, team=team)
    return redirect("/")