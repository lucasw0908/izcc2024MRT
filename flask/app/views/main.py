import io
import logging
import json
from flask import Blueprint, Response, render_template, redirect, send_file, session 
from zenora import APIClient

from ..core import core


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
    if "token" in session:
        bearer_client = APIClient(session.get("token"), bearer=True)
        current_user = bearer_client.users.get_current_user()
        team, is_admin = core.check_player(current_user.username)
        return render_template("index.html", current_user=current_user.username, team=team, graph=core.metro.graph)
    return redirect("/login")


@main.route("/admin")
def admin():
    # if "token" in session:
    #     bearer_client = APIClient(session.get("token"), bearer=True)
    #     current_user = bearer_client.users.get_current_user()
    #     team, is_admin = core.check_player(current_user.username)
    
    #     if is_admin:
    #         return render_template("admin.html", current_user=current_user.username, team=team, graph=core.metro.graph)
    # return redirect("/")
    
    bearer_client = APIClient(session.get("token"), bearer=True)
    current_user = bearer_client.users.get_current_user()
    team, is_admin = core.check_player(current_user.username)
    return render_template("/admin.html" , current_user=current_user.username, team=team, graph=core.metro.graph)

@main.route("/download_graph")
def download_graph():
    with io.StringIO() as file:
        json.dump(core.metro.graph, file, ensure_ascii=False, indent=4)
        response = send_file(file.name, as_attachment=True, download_name="graph.json")
        
    return response

@main.route("/combo")
def combo():
    bearer_client = APIClient(session.get("token"), bearer=True)
    current_user = bearer_client.users.get_current_user()
    team = core.check_player(current_user.username)
    return render_template("combo.html", current_user=current_user.username, team=team, graph=core.metro.graph)

@main.route("/team_leader")
def team_leader():
    bearer_client = APIClient(session.get("token"), bearer=True)
    current_user = bearer_client.users.get_current_user()
    team = core.check_player(current_user.username)
    return render_template("team_leader.html", current_user=current_user.username, team=team, graph=core.metro.graph)

@main.route("/card")
def card():
    bearer_client = APIClient(session.get("token"), bearer=True)
    current_user = bearer_client.users.get_current_user()
    team = core.check_player(current_user.username)
    return render_template("card.html", current_user=current_user.username, team=team, graph=core.metro.graph)


@main.route("/dice")
def dice():
    bearer_client = APIClient(session.get("token"), bearer=True)
    current_user = bearer_client.users.get_current_user()
    team = core.check_player(current_user.username)
    return render_template("dice.html", current_user=current_user.username, team=team, graph=core.metro.graph)