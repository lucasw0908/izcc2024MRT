import random
import logging
from setuptools import find_namespace_packages

from .metro import Metro
from .team import Team
from .card import Card


log = logging.getLogger(__name__)


class TestCore:
    def __init__(self) -> None:
        self.metro = Metro()
        self.teams: dict[str: Team] = None
        self.current_round = 0
        self.cards: list[Card] = []
        self._load_cards()
        
        
    def _load_cards(self) -> None:
        """Load all the cards."""
        
        for card_path in find_namespace_packages(include=["app.cards.*"]):
            
            try:
                card: Card = __import__(card_path).NewCard
                self.cards.append(card)
                log.info(f"Loaded card {card.name}")
            except Exception:
                log.error(f"Failed to load card {card.name}!", exc_info=True)
                
        
    def get_metro(self) -> Metro:
        """
        Get the metro object.
        
        Returns
        -------
        metro: :class:`Metro`
            The metro object.
        """
        return self.metro
    
        
    def create_team(self, name: str, location: str, players: list[str]) -> Team | None:
        """
        Create a new team.
        
        Parameters
        ----------
        name: :type:`str`
            The name of the team.
            
        location: :type:`str`
            The id of the station.
            
        players: :type:`list[str]`
            The list of player names.
            
        Returns
        -------
        team: :class:`Team`
            The team object.
        """
        if name in [team.name for team in self.teams.values()]:
            log.warning(f"team {name} already exists.")
            return None
            
        self.teams[name] = team(name, location, players)
        return self.teams[name]
    
        
    def get_team(self, name: str) -> Team | None:
        """
        Get the team object.
        
        Parameters
        ----------
        name: :type:`str`
            The name of the team.
        """
        
        for team in self.teams:
            if team.name == name:
                return team
            
        return None
    
    
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
        
        sqeuence = self.teams[name].sqeuence
        choice = []
        if self.metro.find(sqeuence[:-2] + str(int(sqeuence[-2:]) + step)) is not None: choice.append(sqeuence[:-2] + str(int(sqeuence[-2:]) + step))
        if self.metro.find(sqeuence[:-2] + str(int(sqeuence[-2:]) - step)) is not None: choice.append(sqeuence[:-2] + str(int(sqeuence[-2:]) - step))
        
        return choice
    
    
    def move_to_location(self, name: str, location: str) -> None:
        """
        Move the team to the location.
        
        Parameters
        ----------
        name: :type:`str`
            The name of the team.

        location: :type:`str`
            The id of the station to move to.
        """
        self.teams[name].point += self.metro.find(location).point
        self.teams[name].location = location
        
        
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