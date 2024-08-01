from typing import Optional

from ..game_config import START_STATION

class Team:
    def __init__(self, name: str, players: Optional[list[str]]=None, admins: Optional[list[str]]=None, location: Optional[str]=None) -> None:
        self.name: str = name
        self.location: str = location or START_STATION
        self.target_location: Optional[str] = None
        self.players = players or []
        self.admins = admins or []
        
        self.point: int = 10
        self.step: int = 0
        
        self.current_mission_finished: bool = True
        self.current_card: Optional[str] = None
        
        self.imprisoned_time: int = 0
        self.is_imprisoned: bool = False
        
        self.stations: list[str] = []
        self.owned_stations: list[str] = []
        self.combos: list[str] = []
        self.choice: list[str] = []
        
        
    def __str__(self) -> str:
        return self.name
    
    
    def __repr__(self) -> str:
        return self.name