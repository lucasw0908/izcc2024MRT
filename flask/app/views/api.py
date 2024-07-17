import logging
from flask import abort, Blueprint, request, render_template, jsonify

from ..core import core
from ..modules.checker import is_admin, is_player
from ..data import load_data


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
        data.append(station.__dict__)
    
    return jsonify(data)


@api.route("/station/<name>")
def station(name: str):
    station = core.metro.find_station(name)
    
    if station is None:
        return jsonify({})
    
    return jsonify(station.__dict__)


@api.route("/collapse_status")
def collapse_status():
    return jsonify({
        "status":core.collapse.status,
        "warning":core.collapse.warning
    })


@api.route("/next_collapse_time")
def next_collapse_time():
    return jsonify(core.collapse.next_time)


@api.route("/teams")
def teams():
    return jsonify([team.__dict__ for team in core.teams.values()])


@api.route("/team/<name>")
def team(name: str):
    if name in core.teams:
        return jsonify(core.teams[name].__dict__)
    return jsonify({})


@api.route("/create_team/<name>/<location>")
def create_team(name: str, location: str):
           
    if not is_admin():
        abort(403)
        
    core.create_team(name=name, location=location)
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
    
    
@api.route("/move/<name>")
def move(name: str):
    
    if not is_player():
        abort(403)
        
    step = core.dice()
    
    if name not in core.teams:
        return "Team does not exist."
        
    return jsonify({
        "step": step,
        "choice": core.move(name=name, step=step)
    })


@api.route("/move_to_location/<name>/<location>")
def move_to_location(name: str, location: str):
    
    if not is_admin():
        abort(403)
        
    if location not in core.teams[name].choice:
        return "Invalid location."
    
    core.teams[name].choice = []
        
    return jsonify(core.move_to_location(name=name, location=location))


@api.route("/add_point/<name>/<point>")
def add_point(name: str, point: int):
    
    if not is_admin():
        abort(403)
        
    core.teams[name].point += point
    return "Point added."


@api.route("/set_point/<name>/<point>")
def set_point(name: str, point: int):
    
    if not is_admin():
        abort(403)
        
    core.teams[name].point = point
    return "Point set."


@api.route("/finish_mission/<name>")
def finish_mission(name: str):
    
    # if not is_admin():
    #     abort(403)
    
    if name not in core.teams:
        return "Team does not exist."
    
    card = core.finish_mission(name=name)
    if card is None:
        return "Mission finished."
    return card


@api.route("/combo")
def combo():
    return jsonify(load_data("combo"))