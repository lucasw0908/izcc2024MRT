import random
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

from ..game_config import CARD, COLLAPSE, DELETE_STATIONS
from .metro import MetroSystem, Station
from .team import Team


log = logging.getLogger(__name__)
scheduler = BlockingScheduler()


class Core:
    def __init__(self) -> None:
        self.metro = MetroSystem()
        self.teams: dict[str: Team] = {}
        self.current_round = 0
        self.collapse_status = 0
        
        for collapse in COLLAPSE:
            hour, minute = collapse["time"].split(":")
            scheduler.add_job(self._collapse, "cron", hour=hour, minute=minute)
    
    
    def _collapse(self) -> None:
        for collapse in COLLAPSE:
            if collapse["status"] == self.collapse_status:
                for station in collapse["stations"]:
                    DELETE_STATIONS.append(station)
                    self.metro.delete_stations()
                self.collapse_status += 1

    
    def create_team(self, name: str, players: list[str], admins: list[str], location: str=None) -> None:
        """
        Create a new team.
        
        Parameters
        ----------
        name: :type:`str`
            The name of the team.
            
        location: :type:`str`
            The name of the station.
            
        players: :type:`list[str]`
            The list of player discord ids.
            
        Returns
        -------
        team: :class:`Team`
            The team object.
        """
        
        if name in self.teams.keys():
            log.error(f"Team {name} already exists.")
            return None
            
        self.teams[name] = team(name, players, admins, location)
        
        
    def check_player(self, player: str) -> tuple[Team | None, bool]:
        """
        Check if the player is in the team.
        
        Parameters
        ----------
        player: :type:`str`
            The discord id of the player.
            
        Returns
        -------
        team: :class:`Team`
            The team object.
            
        is_admin: :type:`bool`
            If the player is an admin.
        """
        
        for team in self.teams:
            if player in team.players:
                return team.name, False
            if player in team.admins:
                return team.name, True
            
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
            for station in self.metro.move(current_station):
                if index == step:
                    choice.append(station)
                else:
                    current_station = station
        
        return choice
    
    
    def move_to_location(self, name: str, location: str) -> str | None:
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
        card: :type:`str`
            The card to draw.
        """
        
        station = self.metro.find_station(location)
        self.teams[name].location = station.name
        
        if station.team != name:
            self.teams[name].point -= station.point
            self.teams[station.team].point += station.point
        
        if station.is_special:
            return f"card{self.dice(CARD)}"
        
        
    def mission_finish(self, name: str) -> None:
        """
        Finish the mission.
        
        Parameters
        ----------
        name: :type:`str`
            The name of the team.
        """
        station = self.teams[name].location
        if station.team is None:
            self.teams[name].point += 30
            self.metro.__dict__[station].team = name
        elif station.team != name:
            match station.point:
                case 20: self.teams[name].point += 10
                case 35: self.teams[name].point += 15
                case 50: self.teams[name].point += 20
            
        
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