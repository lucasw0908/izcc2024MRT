import logging
from logging import INFO
from flask import abort, Blueprint, session, request
from zenora import APIClient

from ..core import core
from ..modules.checker import is_admin, is_game_admin
from ..status_codes import STATUS_CODES


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
           
    if not is_admin():
        abort(403)
        
    if name in core.teams:
        return STATUS_CODES.S20003
        
    if core.metro.find_station(station) is None:
        return STATUS_CODES.S00003
        
    core.create_team(name=name, station=station)
    return STATUS_CODES.S00000
    
    
@admin_api.route("/delete_team/<name>")
def delete_team(name: str):
        
    if not is_admin():
        abort(403)
        
    team = core.teams.pop(name, None)
    if team is None:
        return STATUS_CODES.S00004
    
    return STATUS_CODES.S00000


@admin_api.route("/join_team/<name>/<player_name>")
def join_team(name: str, player_name: str):
    
    if not is_admin():
        abort(403)
        
    if name not in core.teams:
        return STATUS_CODES.S00004

    core.teams[name].admins.append(player_name)
    
    return STATUS_CODES.S00000


@admin_api.route("/set_location/<name>/<location>")
def set_location(name: str, location: str):
    
    if not is_admin():
        abort(403)
        
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
        
    if name not in core.teams:
        return STATUS_CODES.S00004
        
    core.teams[name].is_imprisoned = True
    core.teams[name].imprisoned_time = time
    
    log.debug(f"Team {name} is imprisoned by admin.")
    
    return STATUS_CODES.S00000


@admin_api.route("/release_team/<name>")
def release_team(name: str):
    
    if not is_admin():
        abort(403)
        
    if name not in core.teams:
        return STATUS_CODES.S00004
        
    core.teams[name].is_imprisoned = False
    
    log.debug(f"Team {name} is released by admin.")
    
    return STATUS_CODES.S00000


@admin_api.route("/finish_mission/<name>")
def finish_mission(name: str):
    
    if not is_admin():
        abort(403)
    
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


@admin_api.route("/reset_team/<name>")
def reset_team(name: str):
        
    if not is_admin():
        abort(403)
        
    if name not in core.teams:
        return STATUS_CODES.S00004
        
    core.reset_team(name)
    
    return STATUS_CODES.S00000


@admin_api.route("/end_game")
def end_game():
    
    if not is_game_admin():
        abort(403)
        
    core.end_game()
    
    return STATUS_CODES.S00000