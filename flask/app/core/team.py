from timedelta import Timedelta
from datetime import datetime

from ..game_config import START_STATION

class Team:
    def __init__(self, name: str, players: list[str]=[], admins: list[str]=[], location: str | None=None) -> None:
        self.name = name
        self.location = location if location is not None else START_STATION
        self.players = players
        self.admins = admins
        
        self.point: int = 10
        self.step: int = 0
        
        self.current_mission_finished = True
        self.current_card: str | None = None
        
        self.imprisoned_time: datetime = Timedelta(minutes=0)
        self.is_imprisoned = False
        
        self.stations = []
        self.combos = []
        self.choice = []
        
        
    def __str__(self) -> str:
        return self.name
    
    
    def __repr__(self) -> str:
        return self.name