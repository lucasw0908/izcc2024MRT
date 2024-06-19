import random
import logging

from .metro import Metro
from .team import Team


log = logging.getLogger(__name__)


class Core:
    def __init__(self) -> None:
        self.metro = Metro()
        self.teams: dict[str: Team] = None
        self.current_round = 0
        
    def get_metro(self) -> Metro:
        return self.metro
        
    def set_team(self, name: str, location: str, players: list[str]) -> None:
        """
        Parameters
        ----------
        
        name: :type:`str`
            The name of the team.
            
        location: :type:`str`
            The id of the station.
        """
        if name in [team.name for team in self.teams.values()]:
            log.warning(f"team {name} already exists.")
            return None
            
        self.teams[name] = team(name, location, players)
        
    def get_team(self, name: str) -> Team | None:
        
        for team in self.teams:
            if team.name == name:
                return team
            
        return None
    
    def move_step(self, name: str, step: int) -> None:
        sqeuence = self.teams[name].sqeuence
        choice = []
        if self.metro.find(sqeuence[:-2] + str(int(sqeuence[-2:]) + step)) is not None: choice.append(sqeuence[:-2] + str(int(sqeuence[-2:]) + step))
        if self.metro.find(sqeuence[:-2] + str(int(sqeuence[-2:]) - step)) is not None: choice.append(sqeuence[:-2] + str(int(sqeuence[-2:]) - step))
    
    def move_location(self, name: str, location: str) -> None:
        """
        Parameters
        ----------
        
        name: :type:`str`
            The name of the team.

        location: :type:`str`
            The id of the station to move to.
        """
        self.teams[name].point += self.metro.find(location).point
        self.teams[name].location = location
        
    def dice(self) -> int:
        return random.randint(1, 6)
        
        