import io
import os
import logging
import json
from flask import abort, Blueprint, Response, render_template, redirect, send_file, send_from_directory, session
from zenora import APIClient

from ..core import core
from ..data import load_data
from ..config import BASEDIR
from ..modules.checker import is_game_admin, is_admin


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
        team, _ = core.check_player(current_user.username)
        return render_template("index.html", current_user=current_user.username, team=team, graph=core.metro.graph)
    
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


@main.route("/download_graph")
def download_graph():
    with io.StringIO() as file:
        json.dump(core.metro.graph, file, ensure_ascii=False, indent=4)
        response = send_file(file.name, as_attachment=True, download_name="graph.json")
        
    return response


@main.route("/combo")
def combo():
    if "token" in session:
        bearer_client = APIClient(session.get("token"), bearer=True)
        current_user = bearer_client.users.get_current_user()
        team, _ = core.check_player(current_user.username)
        return render_template("combo.html", current_user=current_user.username, team=team, graph=core.metro.graph, combos=load_data("combo"))
    
    return redirect("/")


@main.route("/team_admin")
def team_admin():
    if "token" in session:
        bearer_client = APIClient(session.get("token"), bearer=True)
        current_user = bearer_client.users.get_current_user()
        team, _ = core.check_player(current_user.username)
        
        if is_admin():
            return render_template("team_admin.html", current_user=current_user.username, team=team, graph=core.metro.graph)
        
    return redirect("/")


@main.route("/card")
def card():
    if "token" in session:
        bearer_client = APIClient(session.get("token"), bearer=True)
        current_user = bearer_client.users.get_current_user()
        team, _ = core.check_player(current_user.username)
        
        if is_admin():
            return render_template("card.html", current_user=current_user.username, team=team, graph=core.metro.graph)
        
    return redirect("/")


@main.route("/dice")
def dice():
    if "token" in session:
        bearer_client = APIClient(session.get("token"), bearer=True)
        current_user = bearer_client.users.get_current_user()
        team, _ = core.check_player(current_user.username)
        
        if is_admin():
            return render_template("dice.html", current_user=current_user.username, team=team, graph=core.metro.graph)

    return redirect("/")


@main.route("/initialization")
def initialization():
    if "token" in session:
        bearer_client = APIClient(session.get("token"), bearer=True)
        current_user = bearer_client.users.get_current_user()
        team, _ = core.check_player(current_user.username)
        
        if is_admin():
            return render_template("initialization.html", current_user=current_user.username, team=team, graph=core.metro.graph)

    return redirect("/")


@main.route("/log")
def serve_log():
    log_directory = os.path.join(BASEDIR, "logs")
    log_filename = "app.log"
    
    if is_game_admin():
        
        bearer_client = APIClient(session.get("token"), bearer=True)
        current_user = bearer_client.users.get_current_user()
        
        log.info(f"{current_user.username}({current_user.id}) is checking the log file")
        
        return send_from_directory(log_directory, log_filename)
    
    abort(404)