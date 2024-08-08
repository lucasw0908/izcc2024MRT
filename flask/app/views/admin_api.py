import logging
from logging import INFO
from flask import abort, Blueprint, session, request
from zenora import APIClient

from ..core import core
from ..modules.checker import is_admin, is_game_admin
from ..status_codes import STATUS_CODES
from ..models import db


log = logging.getLogger(__name__)
admin_api = Blueprint("admin_api", __name__, url_prefix="/api/admin")

yellow_text_color = "\33[33m"
reset_text_color = "\33[0m"


@admin_api.before_request
def log_user():
    if "token" in session:
        bearer_client = APIClient(session.get("token"), bearer=True)
        current_user = bearer_client.users.get_current_user()
        log.log(INFO, f"{yellow_text_color}User \"{current_user.username}\" is using an admin api: \"{request.endpoint}\"{reset_text_color}")


@admin_api.route("/create_team/<name>/<station>")
def create_team(name: str, station: str):
    """
    Create a team with the given name and station.
    
    Parameters
    ----------
    name: :type:`str`
        The name of the team.
        
    station: :type:`str`
        The station of the team.
        
    Returns
    -------
    result: :type:`str`
        The status code.
        
    Status Codes
    ------------
    - S00000: The team is created successfully.
    - S00003: The station is not found.
    - S20003: The team is already exists.
    - S99999: The game is not running.
    """
           
    if not is_admin():
        abort(403)
                
    if core.is_running is False:
        return STATUS_CODES.S99999
        
    if name in core.teams:
        return STATUS_CODES.S20003
        
    if core.metro.find_station(station) is None:
        return STATUS_CODES.S00003
        
    core.create_team(name=name, station=station)
    return STATUS_CODES.S00000
    
    
@admin_api.route("/delete_team/<name>")
def delete_team(name: str):
    """
    Parameters
    ----------
    name: :type:`str`
        The name of the team.
        
    Returns
    -------
    result: :type:`str`
        The status code.
        
    Status Code
    -----------
    - S00000: The team is deleted successfully
    - S00004: The team does not exist.
    - S99999: The game is not running
    """
        
    if not is_admin():
        abort(403)
                
    if core.is_running is False:
        return STATUS_CODES.S99999
        
    team = core.teams.pop(name, None)
    if team is None:
        return STATUS_CODES.S00004
    
    return STATUS_CODES.S00000


@admin_api.route("/join_team/<name>/<player_name>")
def join_team(name: str, player_name: str):
    
    if not is_admin():
        abort(403)
                
    if core.is_running is False:
        return STATUS_CODES.S99999
        
    if name not in core.teams:
        return STATUS_CODES.S00004

    core.teams[name].admins.append(player_name)
    
    return STATUS_CODES.S00000


@admin_api.route("/set_location/<name>/<location>")
def set_location(name: str, location: str):
    
    if not is_admin():
        abort(403)
                
    if core.is_running is False:
        return STATUS_CODES.S99999
        
    if name not in core.teams:
        return STATUS_CODES.S00004
        
    if core.teams[name].is_imprisoned:
        return STATUS_CODES.S20002
    
    core.teams[name].location = location
    
    return STATUS_CODES.S00000


@admin_api.route("/imprison/<name>/<time>")
def imprison(name: str, time: int):
    
    if not is_admin():
        abort(403)
            
    if core.is_running is False:
        return STATUS_CODES.S99999
        
    if name not in core.teams:
        return STATUS_CODES.S00004
        
    core.teams[name].is_imprisoned = True
    core.teams[name].imprisoned_time = time
    
    log.debug(f"Team {name} is imprisoned by admin.")
    
    return STATUS_CODES.S00000


@admin_api.route("/release_team/<name>")
def release_team(name: str):
    
    if core.is_running is False:
        return STATUS_CODES.S99999
    
    if not is_admin():
        abort(403)
        
    if name not in core.teams:
        return STATUS_CODES.S00004
        
    core.teams[name].is_imprisoned = False
    
    log.debug(f"Team {name} is released by admin.")
    
    return STATUS_CODES.S00000


@admin_api.route("/finish_mission/<name>")
def finish_mission(name: str):
    """
    Finish the current mission of the team but admin version. \\
    If the team is imprisoned, the team will be released. \\
    If the team is not in the target location, the team will be moved to the target location.
    
    
    Parameters
    ----------
    name: :type:`str`
        The name of the team.
        
    Returns
    -------
    result: :type:`str`
        The status code.
        
    Status Code
    -----------
    - S00000: The mission is finished successfully.
    - S00004: The team does not exist.
    - S50003: The current mission is already finished.
    - S99999: The game is not running.
    """
    
    if not is_admin():
        abort(403)
        
    if core.is_running is False:
        return STATUS_CODES.S99999
    
    if name not in core.teams:
        return STATUS_CODES.S00004
    
    if core.teams[name].current_mission_finished:
        return STATUS_CODES.S50003
    
    if core.teams[name].is_imprisoned:
        core.teams[name].is_imprisoned = False
    
    if core.teams[name].target_location != core.teams[name].location:
        core.teams[name].location = core.teams[name].target_location
    
    card = core.finish_mission(name=name)
    return STATUS_CODES.S00000 if card is None else card


@admin_api.route("/save_team")
def save_team():
    """
    Save the team to the database.
    
    Returns
    -------
    result: :type:`str`
        The status code.
        
    Status Code
    -----------
    - S00000: The game is ended successfully.
    """
    
    if not is_game_admin():
        abort(403)
        
    db.create_all()
        
    core.save_team()
    
    return STATUS_CODES.S00000


@admin_api.route("/load_team")
def load_team():
    """
    Load the team from the database.
    
    Returns
    -------
    result: :type:`str`
        The status code.
        
    Status Code
    -----------
    - S00000: The game is ended successfully.
    """
    
    if not is_game_admin():
        abort(403)
        
    db.create_all()
        
    core.load_team()
    
    return STATUS_CODES.S00000


@admin_api.route("/reset_team/<name>")
def reset_team(name: str):
    """
    Reset the team.
    
    Parameters
    ----------
    name: :type:`str`
        The name of the team.
        
    Returns
    -------
    result: :type:`str`
        The status code.
        
    Status Code
    -----------
    - S00000: The team is reset successfully.
    - S00004: The team does not exist
    """
        
    if not is_admin():
        abort(403)
        
    if name not in core.teams:
        return STATUS_CODES.S00004
        
    core.reset_team(name)
    
    return STATUS_CODES.S00000


@admin_api.route("/end_game")
def end_game():
    """
    End the game.
    
    Returns
    -------
    result: :type:`str`
        The status code.
        
    Status Code
    -----------
    - S00000: The game is ended successfully.
    """
    
    if not is_game_admin():
        abort(403)
        
    core.end_game()
    
    return STATUS_CODES.S00000


@admin_api.route("/start_game")
def start_game():
    """
    Start the game.
    
    Returns
    -------
    result: :type:`str`
        The status code.
        
    Status Code
    -----------
    - S00000: The game is started successfully.
    """
    
    if not is_game_admin():
        abort(403)
        
    core.start_game()
    
    return STATUS_CODES.S00000