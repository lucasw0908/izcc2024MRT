import pygeohash as pgh
import logging
from logging import INFO
from flask import abort, Blueprint, jsonify, session
from zenora import APIClient

from ..core import core
from ..config import RESET_TEXT_COLOR, YELLOW_TEXT_COLOR
from ..modules.checker import is_admin, is_player
from ..data import load_data
from ..status_codes import STATUS_CODES, LANGUAGE


log = logging.getLogger(__name__)
api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/status_codes")
def status_codes_default():
    """Get status codes in default language."""
    
    try: 
        data = STATUS_CODES.localization(language=LANGUAGE, is_return=True)
        return jsonify(data)
    
    except Exception as e:
        abort(404)


@api.route("/status_codes/<language>")
def status_codes(language: str):
    """Get status codes in specified language."""
    
    try: 
        data = STATUS_CODES.localization(language=language, is_return=True)
        return jsonify(data)
    
    except Exception as e:
        abort(404)


@api.route("/graph")
def graph():
    """Get the graph of the metro system."""
    
    if not is_player():
        abort(403)
    
    return jsonify(core.metro.graph)


@api.route("/stations")
def stations():
    """Get the `list` of stations."""
    
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
        if station.hidden and (station_name not in unlock_stations):
            data[-1]["mission"] = "隱藏"
            data[-1]["tips"] = "隱藏"
            data[-1]["exit"] = "隱藏"
    
    return jsonify(data)


@api.route("/station/<name>")
def station(name: str):
    """Get the information of the station."""
    
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
    """Get the status of the collapse."""
    
    if not is_player():
        abort(403)
    
    return jsonify({
        "status": core.collapse.status,
        "warning": core.collapse.warning
    })


@api.route("/next_collapse_time")
def next_collapse_time():
    """Get the next collapse time."""
    
    if not is_player():
        abort(403)
    
    return jsonify(core.collapse.next_time)


@api.route("/combo")
def combo():
    """Get the combo of the game."""
    
    
    if not is_player():
        abort(403)
    
    return jsonify(load_data("combo"))


@api.route("/teams")
def teams():
    """Get the `list` of teams."""
    
    
    if not is_player():
        abort(403)
        
    return jsonify([team.__dict__ for team in core.teams.values()])


@api.route("/team/<name>")
def team(name: str):
    """Get the information of the team."""
    
    if not is_player():
        abort(403)
    
    if name in core.teams:
        return jsonify(core.teams[name].__dict__)
    
    return jsonify({})


@api.route("/join_team/<name>/<player_name>")
def join_team(name: str, player_name: str):
    """
    Join the team.
    
    Parameters
    ----------
    name: :type:`str`
        The name of the team.
        
    player_name: :type:`str`
        The name of the player.
        
    Returns
    -------
    result: :type:`str`
        The status code.
        
    Status Codes
    ------------
    - S00000: Success
    - S00004: The team does not exist.
    - S99999: The game is not running.
    """
    
    if not is_admin():
        abort(403)
                
    if core.is_running is False:
        return STATUS_CODES.S99999
        
    if name not in core.teams:
        return STATUS_CODES.S00004

    current_team, admin = core.check_player(player_name)
    
    if current_team is not None:
        if admin:
            core.teams[current_team].admins.remove(player_name)
        else:
            core.teams[current_team].players.remove(player_name)

    core.teams[name].players.append(player_name)
        
    return STATUS_CODES.S00000


@api.route("/leave_team/<player_name>")
def leave_team(player_name: str):
    """
    Leave the team.
    
    Parameters
    ----------
    player_name: :type:`str`
        The name of the player.
        
    Returns
    -------
    result: :type:`str`
        The status code.
        
    Status Codes
    ------------
    - S00000: Success
    - S30002: The player does not exist in any team.
    - S99999: The game is not running.
    """
    
    if not is_admin():
        abort(403)
                
    if core.is_running is False:
        return STATUS_CODES.S99999
        
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
    """
    The first stage of this round. \\
    Let the team dice and choose the station you can go next.
    
    Parameters
    ----------
    name: :type:`str`
        The name of the team.
        
    Returns
    -------
    result: :type:`str` | :type:`dict`
        The status code or the step and choice of the team.
        
        - step: :type:`int`
            The step of the team. e.g. `3`
            
        - choice: :type:`list`
            The choice of the team. e.g. `["七張", "景美"]`
            
    Status Codes
    ------------
    - S00004: The team does not exist.
    - S20002: The team is imprisoned.
    - S50002: The current mission is not finished.
    - S99999: The game is not running.
    """
    
    if not is_admin():
        abort(403)
                
    if core.is_running is False:
        return STATUS_CODES.S99999
        
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
    """
    The second stage of this round. \\
    Set the target station of the team.
    
    Parameters
    ----------
    name: :type:`str`
        The name of the team.
        
    location: :type:`str`
        The location of the team.
        
    Returns
    -------
    result: :type:`str`
        The status code.
        
    Status Codes
    ------------
    - S00000: Success
    - S00004: The team does not exist.
    - S20002: The team is imprisoned.
    - S50002: The current mission is not finished.
    - S00006: The location does not exist.
    - S99999: The game is not running.
    """
    
    if not is_admin():
        abort(403)
                
    if core.is_running is False:
        return STATUS_CODES.S99999
        
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
    
    core.move_to_location(name=name, location=location)
        
    return STATUS_CODES.S00000


@api.route("/add_point/<name>/<point>")
def add_point(name: str, point: int):
    """
    Add points to the team.
    
    Parameters
    ----------
    name: :type:`str`
        The name of the team.
        
    point: :type:`int`
        The point to add.
        
    Returns
    -------
    result: :type:`str`
        The status code.
        
    Status Codes
    ------------
    - S00000: Success
    - S00004: The team does not exist.
    - S99999: The game is not running.
    """
    
    if not is_admin():
        abort(403)
                
    if core.is_running is False:
        return STATUS_CODES.S99999
        
    if name not in core.teams:
        return STATUS_CODES.S00004
    
    point = int(point)
        
    core.teams[name].point += point
    
    bearer_client = APIClient(session.get("token"), bearer=True)
    current_user = bearer_client.users.get_current_user()        
    
    log.log(INFO, f"{YELLOW_TEXT_COLOR}User \"{current_user.username}\" added {point} point(s) to {name}{RESET_TEXT_COLOR}")
    core.teams[name].add_point_log(point, f"By {current_user.username}")
    
    return STATUS_CODES.S00000


@api.route("/set_point/<name>/<point>")
def set_point(name: str, point: int):
    """
    Set the point of the team.
    
    Parameters
    ----------
    name: :type:`str`
        The name of the team.
        
    point: :type:`int`
        The point to set.
        
    Returns
    -------
    result: :type:`str`
        The status code.
        
    Status Codes
    ------------
    - S00000: Success
    - S00004: The team does not exist.
    - S99999: The game is not running
    """
    
    if not is_admin():
        abort(403)
                
    if core.is_running is False:
        return STATUS_CODES.S99999
        
    if name not in core.teams:
        return STATUS_CODES.S00004
    
    point = int(point)
    
    bearer_client = APIClient(session.get("token"), bearer=True)
    current_user = bearer_client.users.get_current_user()

    log.log(INFO, f"{YELLOW_TEXT_COLOR}User \"{current_user.username}\" set {name}'s points to {point}{RESET_TEXT_COLOR}")
    core.teams[name].add_point_log(point - core.teams[name].point, f"By {current_user.username}")
    core.teams[name].point = point
    
    return STATUS_CODES.S00000


@api.route("/finish_mission/<name>")
def finish_mission(name: str):
    """
    The third stage of this round. Told system mission finished. \\
    If the station is special, you will get the `card` (filename) in response.
    
    Parameters
    ----------
    name: :type:`str`
        The name of the team.
        
    Returns
    -------
    result: :type:`str`
        The status code or the card.
        
    Status Codes
    ------------
    - S00000: Success
    - S00004: The team does not exist.
    - S20002: The team is imprisoned.
    - S50003: The current mission is finished.
    - S40002: The team is not at the target location.
    - S99999: The game is not running
    """
    
    if not is_admin():
        abort(403)
                
    if core.is_running is False:
        return STATUS_CODES.S99999
    
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
    """
    The third stage of this round. \\
    Skip the current mission of the team.
    
    Parameters
    ----------
    name: :type:`str`
        The name of the team.
        
    Returns
    -------
    result: :type:`str`
        The status code.
        
    Status Codes
    ------------
    - S00000: Success
    - S00004: The team does not exist.
    - S20002: The team is imprisoned.
    - S50003: The current mission is finished.
    - S40002: The team is not at the target location.
    - S99999: The game is not running
    """
    
    if not is_admin():
        abort(403)
                
    if core.is_running is False:
        return STATUS_CODES.S99999
    
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
    """
    Update the GPS location of the team.
    
    Parameters
    ----------
    name: :type:`str`
        The name of the team.
        
    latitude: :type:`float`
        The latitude of the team.
        
    longitude: :type:`float`
        The longitude of the team.
        
    Returns
    -------
    result: :type:`str` | :type:`dict`
        The status code or the result of the check position.
            
        - location: :type:`str`
            The current station of the team.
            
        - distance: :type:`str`
            The distance between the station and the position.
        
    Status Codes
    ------------
    - S00000: Success
    - S00004: The team does not exist.
    - S00006: The location does not exist.
    - S99999: The game is not running
    """
    
    if not is_admin():
        abort(403)
                
    if core.is_running is False:
        return STATUS_CODES.S99999
        
    latitude = float(latitude)
    longitude = float(longitude)

    if name not in core.teams:
        return STATUS_CODES.S00004
    
    if longitude > 180 or longitude < -180 or latitude > 90 or latitude < -90:
        return STATUS_CODES.S00006
    
    log.debug(f"Team {name} is at {longitude}, {latitude}")
    
    return jsonify(core.check_pos(name, pgh.encode(latitude, longitude)))