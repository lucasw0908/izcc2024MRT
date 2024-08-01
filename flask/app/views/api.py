import pygeohash as pgh
import logging
from flask import abort, Blueprint, jsonify, session
from zenora import APIClient

from ..core import core
from ..modules.checker import is_admin, is_player
from ..data import load_data
from ..status_codes import STATUS_CODES, LANGUAGE


log = logging.getLogger(__name__)
api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/status_codes")
def status_codes_default():
    try: 
        data = STATUS_CODES.localization(language=LANGUAGE, is_return=True)
        return jsonify(data)
    
    except Exception as e:
        abort(404)


@api.route("/status_codes/<language>")
def status_codes(language: str):
    try: 
        data = STATUS_CODES.localization(language=language, is_return=True)
        return jsonify(data)
    
    except Exception as e:
        abort(404)


@api.route("/graph")
def graph():
    
    if not is_player():
        abort(403)
    
    return jsonify(core.metro.graph)


@api.route("/stations")
def stations():
    
    if not is_player():
        abort(403)
    
    data = []
    graph = core.metro.graph
    unlock_stations = []
    
    if "token" in session:
        bearer_client = APIClient(session.get("token"), bearer=True)
        current_user = bearer_client.users.get_current_user()
        team, _ = core.check_player(current_user.username)
        if team is not None:
            unlock_stations.extend(team.stations)
    
    for station_name in graph.keys():
        station = core.metro.find_station(station_name)
        data.append(station.__dict__)
        if station.hidden and station_name not in unlock_stations:
            data[-1]["mission"] = "隱藏"
            data[-1]["tips"] = "隱藏"
            data[-1]["exit"] = "隱藏"
    
    return jsonify(data)


@api.route("/station/<name>")
def station(name: str):
    
    if not is_player():
        abort(403)
    
    station = core.metro.find_station(name.replace("_", "/"))
    
    if station is None:
        return jsonify({})
    
    unlock_stations = []
    
    if "token" in session:
        bearer_client = APIClient(session.get("token"), bearer=True)
        current_user = bearer_client.users.get_current_user()
        team, _ = core.check_player(current_user.username)
        if team is not None:
            unlock_stations.extend(team.stations)
    
    data = station.__dict__
    if station.hidden and name not in unlock_stations:
        data["mission"] = "隱藏"
        data["tips"] = "隱藏"
        data["exit"] = "隱藏"
        
    return jsonify(data)


@api.route("/collapse_status")
def collapse_status():
    
    if not is_player():
        abort(403)
    
    return jsonify({
        "status": core.collapse.status,
        "warning": core.collapse.warning
    })


@api.route("/next_collapse_time")
def next_collapse_time():
    
    if not is_player():
        abort(403)
    
    return jsonify(core.collapse.next_time)


@api.route("/combo")
def combo():
    
    if not is_player():
        abort(403)
    
    return jsonify(load_data("combo"))


@api.route("/teams")
def teams():
    
    if not is_player():
        abort(403)
        
    return jsonify([team.__dict__ for team in core.teams.values()])


@api.route("/team/<name>")
def team(name: str):
    
    if not is_player():
        abort(403)
    
    if name in core.teams:
        return jsonify(core.teams[name].__dict__)
    
    return jsonify({})


@api.route("/join_team/<name>/<player_name>")
def join_team(name: str, player_name: str):
    
    if not is_admin():
        abort(403)
        
    if name not in core.teams:
        return STATUS_CODES.S00004

    core.teams[name].players.append(player_name)
        
    return STATUS_CODES.S00000


@api.route("/leave_team/<player_name>")
def leave_team(player_name: str):
    
    if not is_admin():
        abort(403)
        
    for team in core.teams.values():
        if player_name in team.players:
            team.players.remove(player_name)
            return STATUS_CODES.S00000
        
        if player_name in team.admins:
            team.admins.remove(player_name)
            return STATUS_CODES.S00000
            
    return STATUS_CODES.S30002
    
    
@api.route("/move/<name>")
def move(name: str):
    
    if not is_admin():
        abort(403)
        
    if name not in core.teams:
        return STATUS_CODES.S00004
        
    if core.teams[name].is_imprisoned:
        return STATUS_CODES.S20002
    
    if not core.teams[name].current_mission_finished:
        return STATUS_CODES.S50002
    
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
        return STATUS_CODES.S00004
        
    if core.teams[name].is_imprisoned:
        return STATUS_CODES.S20002
    
    if not core.teams[name].current_mission_finished:
        return STATUS_CODES.S50002
        
    if location not in core.teams[name].choice:
        return STATUS_CODES.S00006
    
    core.teams[name].choice = []
    core.teams[name].step = 0
        
    return jsonify(core.move_to_location(name=name, location=location))


@api.route("/add_point/<name>/<point>")
def add_point(name: str, point: int):
    
    if not is_admin():
        abort(403)
        
    if name not in core.teams:
        return STATUS_CODES.S00004
    
    point = int(point)
        
    core.teams[name].point += point
    core.teams[name].add_point_log(point, "By admin")
    
    return STATUS_CODES.S00000


@api.route("/set_point/<name>/<point>")
def set_point(name: str, point: int):
    
    if not is_admin():
        abort(403)
        
    if name not in core.teams:
        return STATUS_CODES.S00004
    
    point = int(point)
    
    core.teams[name].add_point_log(point - core.teams[name].point, "By admin")
    core.teams[name].point = point
    
    return STATUS_CODES.S00000


@api.route("/finish_mission/<name>")
def finish_mission(name: str):
    
    if not is_admin():
        abort(403)
    
    if name not in core.teams:
        return STATUS_CODES.S00004
    
    if core.teams[name].is_imprisoned:
        return STATUS_CODES.S20002
    
    if core.teams[name].current_mission_finished:
        return STATUS_CODES.S50003
    
    if core.teams[name].target_location != core.teams[name].location:
        return STATUS_CODES.S40002
    
    card = core.finish_mission(name=name)
    return STATUS_CODES.S00000 if card is None else card


@api.route("/skip_mission/<name>")
def skip_mission(name: str):
    
    if not is_admin():
        abort(403)
    
    if name not in core.teams:
        return STATUS_CODES.S00004
    
    if core.teams[name].is_imprisoned:
        return STATUS_CODES.S20002
    
    if core.teams[name].current_mission_finished:
        return STATUS_CODES.S50003
    
    if core.teams[name].target_location != core.teams[name].location:
        return STATUS_CODES.S40002
    
    core.skip_mission(name=name)
    return STATUS_CODES.S00000


@api.route("/gps_location/<name>/<latitude>/<longitude>")
def gps_location(name: str, latitude: float, longitude: float):
    
    if not is_admin():
        abort(403)
        
    latitude = float(latitude)
    longitude = float(longitude)

    if name not in core.teams:
        return STATUS_CODES.S00004
        
    if core.teams[name].is_imprisoned:
        return STATUS_CODES.S20002
    
    if longitude > 180 or longitude < -180 or latitude > 90 or latitude < -90:
        return STATUS_CODES.S00006
    
    log.debug(f"Team {name} is at {longitude}, {latitude}")
    
    return jsonify(core.check_pos(name, pgh.encode(latitude, longitude)))