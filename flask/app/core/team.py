from datetime import datetime
from typing import Optional

from ..game_config import START_STATION

class Team:
    def __init__(self, name: str, players: Optional[list[str]]=None, admins: Optional[list[str]]=None, location: Optional[str]=None) -> None:
        self.name: str = name
        self.location: str = location or START_STATION
        self.target_location: Optional[str] = location or START_STATION
        self.players = players if players is not None else []
        self.admins = admins if admins is not None else []
        
        self.point_log: list[dict] = []
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
    
    
    def add_point_log(self, point: int, reason: str) -> None:
        data = {
            "point": point,
            "reason": reason,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.point_log.append(data)