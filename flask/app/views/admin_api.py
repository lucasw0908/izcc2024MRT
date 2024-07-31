import logging
from flask import abort, Blueprint

from ..core import core
from ..modules.checker import is_admin
from ..status_codes import STATUS_CODES


log = logging.getLogger(__name__)
admin_api = Blueprint("admin_api", __name__, url_prefix="/api/admin")


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


@admin_api.route("/release_team/<name>")
def release_team(name: str):
    
    if not is_admin():
        abort(403)
        
    if name not in core.teams:
        return STATUS_CODES.S00004
        
    core.teams[name].is_imprisoned = False
    
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