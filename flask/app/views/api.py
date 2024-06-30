import logging
from flask import abort, Blueprint, request, render_template, jsonify

from ..core import core
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
        abort(403)
    
    if request.method == "POST":
        if "name" not in request.form:
            return "Name not provided."
        if "players" not in request.form:
            return "Players not provided."
        if "admins" not in request.form:
            return "Admins not provided."
        
        core.create_team(**request.form)
        return "Team created."
    
    
@api.route("/delete_team/<name>")
def delete_team(name):
        
    if not is_admin():
        abort(403)
        
    core.teams.pop(name, None)
    return "Team deleted."
    
    
@api.route("/move/<name>/<step>")
def move(name: str, step: int):
    
    if not is_player():
        abort(403)
        
    return jsonify(core.move(name=name, step=step))