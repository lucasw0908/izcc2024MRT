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
            "team": station.team,
            "neighbors": graph.get(station.name, []),
        })
    return jsonify(data)


@api.route("/collapse_status")
def collapse_status():
    return jsonify(core.collapse_status)


@api.route("/create_team")
def create_team(name: str, location: str):
           
    if not is_admin():
        abort(403)
        
    core.create_team(name=name, location=location, players=[], admins=[])
    return "Team created."
    
    
@api.route("/delete_team/<name>")
def delete_team(name: str):
        
    if not is_admin():
        abort(403)
        
    core.teams.pop(name, None)
    return "Team deleted."


@api.route("/join_team/<name>/<player_name>/<is_admin>")
def join_team(name: str, player_name: str, is_admin: bool):
    
    if not is_player():
        abort(403)
        
    if is_admin:
        core.teams[name].admins.append(player_name)
    else:
        core.teams[name].players.append(player_name)
        
    return "Player joined team."
    
    
@api.route("/move/<name>/<step>")
def move(name: str, step: int):
    
    if not is_player():
        abort(403)
        
    return jsonify(core.move(name=name, step=step))


@api.route("/move_to_location/<name>/<station>")
def move_to_location(name: str, location: str):
    
    if not is_player():
        abort(403)
        
    return jsonify(core.move_to_location(name=name, location=location))


@api.route("/teams")
def teams():
    return jsonify([team.__dict__ for team in core.teams.values()])


@api.route("/team/<name>")
def team(name: str):
    if name in core.teams:
        return jsonify(core.teams[name].__dict__)
    return jsonify({})