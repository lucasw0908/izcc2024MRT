from ..game_config import START_STATION

class Team:
    def __init__(self, name: str, players: list[str], admins: list[str], location: str=None) -> None:
        self.name = name
        self.location = location if location is not None else START_STATION
        self.players: players
        self.admins = admins
        self.point = 0
        
        
    def __str__(self) -> str:
        return self.name
    
    
    def __repr__(self) -> str:
        return self.name