import pygeohash as pgh
import logging
from flask import abort, Blueprint, jsonify

from ..core import core
from ..modules.checker import is_admin, is_player, is_game_admin
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
        if station.hidden:
            data[-1]["mission"] = "隱藏"
            data[-1]["tips"] = "隱藏"
            data[-1]["exit"] = "隱藏"
    
    return jsonify(data)


@api.route("/station/<name>")
def station(name: str):
    station = core.metro.find_station(name)
    
    if station is None:
        return jsonify({})
    
    data = station.__dict__
    if station.hidden:
        data["mission"] = "隱藏"
        data["tips"] = "隱藏"
        data["exit"] = "隱藏"
        
    return jsonify(data)


@api.route("/collapse_status")
def collapse_status():
    return jsonify({
        "status":core.collapse.status,
        "warning":core.collapse.warning
    })


@api.route("/next_collapse_time")
def next_collapse_time():
    return jsonify(core.collapse.next_time)


@api.route("/combo")
def combo():
    return jsonify(load_data("combo"))


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
        
    if core.metro.find_station(location) is None:
        return "Location does not exist."
        
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


@api.route("/leave_team/<player_name>")
def leave_team(player_name: str):
    
    if not is_player():
        abort(403)
        
    for team in core.teams.values():
        if player_name in team.players:
            team.players.remove(player_name)
            return "Player left team."
        if player_name in team.admins:
            team.admins.remove(player_name)
            return "Player left team."
            
    return "Player not in any team."
    
    
@api.route("/move/<name>")
def move(name: str):
    
    if not is_player():
        abort(403)
        
    if name not in core.teams:
        return "Team does not exist."
        
    if core.teams[name].is_imprisoned:
        return "Team is imprisoned."
    
    if not core.teams[name].current_mission_finished:
        return "Mission not finished."
    
    if core.teams[name].step == 0:
        core.teams[name].step = core.dice()
        
    return jsonify({
        "step": core.teams[name].step,
        "choice": core.move(name=name, step=core.teams[name].step)
    })


@api.route("/move_to_location/<name>/<location>")
def move_to_location(name: str, location: str):
    
    if not is_admin():
        abort(403)
        
    if name not in core.teams:
        return "Team does not exist."
        
    if core.teams[name].is_imprisoned:
        return "Team is imprisoned."
    
    if not core.teams[name].current_mission_finished:
        return "Mission not finished."
        
    if location not in core.teams[name].choice:
        return "Invalid location."
    
    core.teams[name].choice = []
    core.teams[name].step = 0
        
    return jsonify(core.move_to_location(name=name, location=location))


@api.route("/add_point/<name>/<point>")
def add_point(name: str, point: int):
    
    if not is_admin():
        abort(403)
        
    core.teams[name].point += int(point)
    return "Point added."


@api.route("/set_point/<name>/<point>")
def set_point(name: str, point: int):
    
    if not is_admin():
        abort(403)
        
    core.teams[name].point = point
    return "Point set."


@api.route("/finish_mission/<name>")
def finish_mission(name: str):
    
    if not is_admin():
        abort(403)
    
    if name not in core.teams:
        return "Team does not exist."
    
    if core.teams[name].is_imprisoned:
        return "Team is imprisoned."
    
    if core.teams[name].current_mission_finished:
        return "Mission already finished."
    
    if core.teams[name].target_location == core.teams[name].location:
        card = core.finish_mission(name=name)
        return "Mission finished." if card is None else card
    
    return "Location not reached."


@api.route("/GPSLocation/<name>/<location1>/<location2>")
def GPSLocation(name: str, location1: float, location2: float):
    
    if not is_admin():
        abort(403)

    if name not in core.teams:
        return "Team does not exist."
        
    if core.teams[name].is_imprisoned:
        return "Team is imprisoned."
    
    log.debug(f"Team {name} is at {location1}, {location2}")
    
    return core.check_pos(name, pgh.encode(location1, location2))


@api.route("/default_admin/<name>")
def default_admin(name: str):

    if not is_game_admin():
        abort(403)
    
    if name not in core.teams["admins"].admins:
        core.teams["admins"].admins.append(name)
    else:
        core.teams["admins"].admins.remove(name)
    return "ok"