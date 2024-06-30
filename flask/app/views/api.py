import logging
from flask import Blueprint, request, render_template, jsonify
from flask_socketio import SocketIO

from ..core import core, Station
from .socketio import socketio
from ..modules.checker import is_admin, is_player


log = logging.getLogger(__name__)
api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/graph")
def graph():
    return jsonify(core.metro.graph)


@api.route("/stations")
def stations():
    data = []
    graph = core.metro.graph
    for station_name in graph.keys():
        station = core.metro.find_station(station_name)
        data.append({
            "sequence": station.sequence,
            "id": station.id,
            "name": station.name,
            "english_name": station.english_name,
            "point": station.point,
            "is_special": station.is_special,
            "neighbors": graph.get(station.name, []),
        })
    return jsonify(data)


@api.route("/collapse_status")
def collapse_status():
    return jsonify(core.collapse_status)


@api.route("/create_team", methods=["POST"])
def create_team():
    
    if not is_admin():
        return "You are not an admin."
    
    if request.method == "POST":
        if "name" not in request.form:
            return "Name not provided."
        if "players" not in request.form:
            return "Players not provided."
        if "admins" not in request.form:
            return "Admins not provided."
        
        core.create_team(**request.form)
        return "Team created."
    
    
@api.route("/delete_team", methods=["POST"])
def delete_team():
        
    if not is_admin():
        return "You are not an admin."
    
    if request.method == "POST":
        if "name" not in request.form:
            return "Name not provided."
        
        core.teams.pop(request.form["name"], None)
        return "Team deleted."
    
    
@api.route("/move", methods=["POST"])
def move():
    
    if not is_player():
        return "You are not a player."
    
    if request.method == "POST":
        if "id" not in request.form:
            return "ID not provided."
        
        return jsonify(core.move(request.form["id"]))