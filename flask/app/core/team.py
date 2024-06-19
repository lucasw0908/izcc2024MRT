

class Team:
    def __init__(self, name: str, location: str, players: list[str]) -> None:
        self.name = name
        self.location = location
        self.players: players
        self.point = 0
        
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.name