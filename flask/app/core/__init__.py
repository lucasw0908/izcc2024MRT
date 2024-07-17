import random
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from flask_socketio import SocketIO

from ..game_config import ADMINS, CARD, COLLAPSE, COLLAPSE_LIST, DELETE_STATIONS, END_STATION
from ..data import load_data
from .metro import MetroSystem, Station
from .team import Team
from .collapse import Collapse


log = logging.getLogger(__name__)
scheduler = BlockingScheduler()


class Core:
    def __init__(self) -> None:
        self.metro = MetroSystem()
        self.socketio = None
        self.teams: dict[str, Team] = {}
        self.collapse = Collapse()
        
        self.create_team("admins", admins=ADMINS)
        
        for collapse in COLLAPSE:
            hour, minute = collapse["time"].split(":")
            scheduler.add_job(self._collapse, "cron", hour=hour, minute=minute)
    
    
    def _collapse(self) -> None:
        for index, collapse in enumerate(COLLAPSE):
            if collapse["status"] == self.collapse_status:
                if collapse["final"]:
                    for station in self.metro.graph.keys():
                        if station == END_STATION:
                            continue
                        COLLAPSE_LIST.append(station)
                    self.collapse_status = 0
                    return None
                
                for station in collapse["stations"]:
                    COLLAPSE_LIST.append(station)
                    
                self.collapse.status += 1
                self.collapse.next_time = COLLAPSE[index + 1]["time"]
                
                
    def _collapse_warning(self) -> None:
        self.collapse.warning = True
        self.socketio.emit("collapse_warning", self.collapse.next_time)
                
                
    def init_socketio(self, socketio: SocketIO) -> None:
        self.socketio = socketio

    
    def create_team(self, name: str, players: list[str]=[], admins: list[str]=[], location: str=None) -> None:
        """
        Create a new team.
        
        Parameters
        ----------
        name: :type:`str`
            The name of the team.
            
        location: :type:`str`
            The name of the station.
            
        players: :type:`list[str]`
            The list of player discord usernames.
            
        Returns
        -------
        team: :class:`Team`
            The team object.
        """
        
        if name in self.teams.keys():
            log.error(f"Team {name} already exists.")
            return None
            
        self.teams[name] = Team(name, players, admins, location)
        
        
    def check_player(self, player: str) -> tuple[Team | None, bool]:
        """
        Check if the player is in the team.
        
        Parameters
        ----------
        player: :type:`str`
            The discord username of the player.
            
        Returns
        -------
        team: :class:`Team`
            The team object.
            
        is_admin: :type:`bool`
            If the player is an admin.
        """
        
        for team in self.teams:
            if player in self.teams[team].admins:
                return self.teams[team], True
            if player in self.teams[team].players:
                return self.teams[team], False
            
        return None, False
    
    
    def move(self, name: str, step: int) -> list[str] | None:
        """
        Calculate the possible stations to move.
        
        Parameters
        ----------
        name: :type:`str`
            The name of the team.
            
        step: :type:`int`
            The number of steps to move.
            
        Returns
        -------
        choice: :type:`list[str]`
            The list of possible station ids to move.
        """

        if name not in self.teams.keys():
            log.warning(f"Team {name} does not exist.")
            return None
        
        choice = []
        current_station = self.teams[name].location
        for index in range(step):
            log.debug(self.metro.move(current_station))
            for station in self.metro.move(current_station):
                if index + 1 == step:
                    choice.append(station)
                else:
                    current_station = station
                    
        self.teams[name].choice = choice
        
        return choice
    
    
    def move_to_location(self, name: str, location: str) -> tuple[list[str], int]:
        """
        Move the team to the location.
        
        Parameters
        ----------
        name: :type:`str`
            The name of the team.

        location: :type:`str`
            The name of the station to move to.
            
        Returns
        -------
        combos: :type:`list[str]`
            The list of new combo.
            
        point: :type:`int`
            The point to add.
        """
        
        point = 0
        combos = []
        station = self.metro.find_station(location)
        self.teams[name].location = station.name
        self.teams[name].stations.append(station.name)
        
        for combo in load_data("combo"):
            if combo["name"] in self.teams[name].combos:
                continue
            
            if combo["stations"] == set(combo["stations"]).intersection(set(self.teams[name].stations)):
                self.teams[name].point += combo["point"]
                point += combo["point"]
                self.teams[name].combos.append(combo["name"])
                combos.append(combo["name"])
        
        if station.team != name:
            self.teams[name].point -= station.point
            self.teams[station.team].point += station.point
        
        self.teams[name].current_mission_finished = False
        
        return combos, point
        
        
    def finish_mission(self, name: str) -> str | None:
        """
        Finish the mission.
        
        Parameters
        ----------
        name: :type:`str`
            The name of the team.
                        
        Returns
        -------
        card: :type:`str`
            The card to draw.
        """
        
        if self.teams[name].current_mission_finished:
            return None
        
        station = self.metro.find_station(self.teams[name].location)
        
        if station.team is None:
            self.teams[name].point += 30
            self.metro.__dict__[station].team = name
            
        elif station.team != name:
            match station.point:
                case 20: self.teams[name].point += 10
                case 35: self.teams[name].point += 15
                case 50: self.teams[name].point += 20
                
        self.teams[name].current_mission_finished = True
        
        if station.is_special:
            return f"card{self.dice(CARD)}"
            
        
    def dice(self, faces: int=6) -> int:
        """
        Just a dice.
        
        Parameters
        ----------
        faces: :type:`int`
            The number of faces of the dice.
            
        Returns
        -------
        result: :type:`int`
            The result of the dice.
        """
        
        return random.randint(1, faces)
    
    
core = Core()