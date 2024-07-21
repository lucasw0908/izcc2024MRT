import pygeohash as pgh
import logging
import random
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from flask_socketio import SocketIO

from ..game_config import ADMINS, CARD, COLLAPSE, COLLAPSE_TIME, COLLAPSE_DAMAGE, COLLAPSE_LIST, END_STATION, DISTANCE, IMPRISONED_TIME
from ..data import load_data
from ..models import db
from ..models.teams import Teams
from .metro import MetroSystem
from .team import Team
from .collapse import Collapse


log = logging.getLogger(__name__)


class Core:
    def __init__(self) -> None:
        self.metro = MetroSystem()
        self.socketio = None
        self.teams: dict[str, Team] = {}
        self.visited = []
        self.choice: dict[int, list[str]] = {i: [] for i in range(1, 7)}
        self.collapse = Collapse()
        self.collapse_scheduler = BackgroundScheduler()
        self.prison_scheduler = BackgroundScheduler()
        
        self.create_team("admins", admins=ADMINS)
        
        for collapse in COLLAPSE:
            hour, minute = map(int, collapse["time"].split(":"))
            self.collapse_scheduler.add_job(self._collapse, "interval", minutes=COLLAPSE_TIME)
            self.collapse_scheduler.add_job(self._collapse, "date", run_date=datetime.now().replace(hour=hour, minute=minute))
            if minute >= 5: minute -= 5
            else: hour -= 1; minute += 55
            self.collapse_scheduler.add_job(self._collapse_warning, "date", run_date=datetime.now().replace(hour=hour, minute=minute))
        self.collapse_scheduler.start()
        
        self.prison_scheduler.add_job(self._release, "interval", minutes=1)
        self.prison_scheduler.start()
    
    
    def _collapse(self) -> None:
        self.collapse.warning = False
        for index, collapse in enumerate(COLLAPSE):
            if collapse["status"] == self.collapse.status:
                if collapse["final"]:
                    for station in self.metro.graph.keys():
                        if station == END_STATION:
                            continue
                        COLLAPSE_LIST.append(station)
                    self.collapse.status = 0
                    return None
                
                for station in collapse["stations"]:
                    COLLAPSE_LIST.append(station)
                    
                self.collapse.status += 1
                self.collapse.next_time = COLLAPSE[index + 1]["time"]
                
                log.info(f"Station {collapse['stations']} collapsed.")
                
                
    def _collapse_damage(self) -> None:
        for team in self.teams.values():
            if team.location in COLLAPSE_LIST:
                team.point -= COLLAPSE_DAMAGE
                self.socketio.emit("collapse_damage", team.name)
                
                
    def _collapse_warning(self) -> None:
        self.collapse.warning = True
        self.socketio.emit("collapse_warning", self.collapse.next_time)
        
        log.info(f"Station will collapse in 5 minutes.")
        
        
    def _release(self) -> None:
        for team in self.teams.values():
            if not team.is_imprisoned:
                continue
            team.imprisoned_time -= 1
            if team.imprisoned_time <= 0:
                team.is_imprisoned = False
                team.imprisoned_time = 0
                self.socketio.emit("release", team.name)
                
                
    def init_socketio(self, socketio: SocketIO) -> None:
        self.socketio = socketio
        
    
    def load_data(self) -> None:
        for team in Teams.query.all():
            team: Teams
            self.create_team(team.name, team.players, team.admins)
            
        
    def save_data(self) -> None:
        for team in self.teams.values():
            if team.name == "admins":
                continue
            if team.name not in Teams.query.all():
                db.session.add(Teams(team.name, team.players, team.admins, team.point))
            else:
                Teams.query.filter_by(name=team.name).update({"players": team.players, "admins": team.admins, "point": team.point})
        db.session.commit()

    
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
            log.warning(f"Team {name} already exists.")
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
    
    
    def _move(self, current_station: str, target_deep: int, deep: int=1) -> list[str]:
        choice = []
        
        if deep > target_deep or current_station in self.visited:
            return choice
        
        self.visited.append(current_station)
        
        for station in self.metro.move(current_station):
            if station not in self.visited: choice.append(station)
            choice.extend(self._move(station, target_deep, deep + 1))
            
        log.debug(f"Deep: {deep}, Station: {current_station}, Choice: {choice}")
        
        for s in choice:
            if s not in self.choice[deep]:
                self.choice[deep].append(s)
                
        return choice
    
    
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
        
        self.choice = {i: [] for i in range(1, 7)}
        self.visited = []
        current_station = self.teams[name].location
        self._move(current_station, step)
                    
        self.teams[name].choice = self.choice[step]
        
        return self.choice[step]
    
    
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
        
        if name not in self.teams.keys():
            log.warning(f"Team {name} does not exist.")
            return None
        
        point = 0
        combos = []
        station = self.metro.find_station(location)
        self.teams[name].target_location = station.name
        self.teams[name].stations.append(station.name)
        
        for combo in load_data("combo"):
            if combo["name"] in self.teams[name].combos:
                continue
            
            if combo["stations"] == set(combo["stations"]).intersection(set(self.teams[name].stations)):
                self.teams[name].point += combo["point"]
                point += combo["point"]
                self.teams[name].combos.append(combo["name"])
                combos.append(combo["name"])
        
        if station.team is not None and station.team != name:
            self.teams[name].point -= station.point
            self.teams[station.team].point += station.point
            
        if station.is_prison:
            self.teams[name].is_imprisoned = True
            self.teams[name].imprisoned_time = random.randint(IMPRISONED_TIME["min"], IMPRISONED_TIME["max"])
        else:
            self.teams[name].current_mission_finished = False
            
        self.teams[name].current_card = None
        self.metro.find_station(location).hidden = False
        
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
        
        if name not in self.teams.keys():
            log.warning(f"Team {name} does not exist.")
            return None
        
        if self.teams[name].current_mission_finished:
            return None
        
        station = self.metro.find_station(self.teams[name].target_location)
        
        if station.team is None:
            self.teams[name].point += 30
            self.metro.__dict__[station.name].team = name
            
        elif station.team != name:
            match station.point:
                case 20: self.teams[name].point += 10
                case 35: self.teams[name].point += 15
                case 50: self.teams[name].point += 20
                
        self.teams[name].current_mission_finished = True
        self.teams[name].location = self.teams[name].target_location
        
        if station.is_special:
            if self.teams[name].current_card is None:
                card = f"card{self.dice(CARD)}"
                self.teams[name].current_card = card
            return self.teams[name].current_card
            
        
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
    
    
    def check_pos(self, name: str, geohash: str) -> dict[str, str]:
        """
        Check the position of the team.
        
        Parameters
        ----------
        name: :type:`str`
            The name of the team.
            
        geohash: :type:`str`
            The geohash of the position.
        """
        
        if name not in self.teams.keys():
            log.warning(f"Team {name} does not exist.")
            return None
        
        if self.teams[name].is_imprisoned:
            return None
        
        data = {
            "location": None,
            "distance": None,
        }
        
        for station_name, station_geohash in self.metro.station_location.items():
            dis = pgh.geohash_approximate_distance(geohash, station_geohash)
            if dis <= DISTANCE:
                
                if data["location"] is None or dis < data["distance"]:
                    data["location"] = station_name
                    self.teams[name].location = station_name
                    
                    log.info(f"Team {name} moved to {station_name}.")
                    
            if station_name == self.teams[name].target_location:
                data["distance"] = dis
                
        log.debug(data)
        
        return data
    
    
core = Core()