import logging
from flask import Blueprint, request, render_template, jsonify
from flask_socketio import SocketIO
from ..core import core
from .socketio import socketio


log = logging.getLogger(__name__)
api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/graph")
def graph():
    return jsonify(core.metro.graph)


@api.route("/create_team", method=["POST"])
def create_team():
    if request.method == "POST":
        if "name" not in request.form:
            return "Name not provided."
        if "players" not in request.form:
            return "Players not provided."
        if "admins" not in request.form:
            return "Admins not provided."
        
        core.create_team(**request.form)
        return "Team created."
    
    
@api.route("/delete_team", method=["POST"])
def delete_team():
    if request.method == "POST":
        if "name" not in request.form:
            return "Name not provided."
        
        core.teams.pop(request.form["name"], None)
        return "Team deleted."
    
    
@api.route("/move", method=["POST"])
def move():
    if request.method == "POST":
        if "id" not in request.form:
            return "ID not provided."
        
        return jsonify(core.move(request.form["id"]))
    
    
@api.route("/collapse_status")
def collapse_status():
    return jsonify(core.collapse_status)