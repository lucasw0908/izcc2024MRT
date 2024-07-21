from . import db


class Teams(db.Model):
    __tablename__ = "teams"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    players = db.Column(db.PickleType(), nullable=False)
    admins = db.Column(db.PickleType(), nullable=False)
    point = db.Column(db.Integer, default=10)
    
    def __init__(self, name: str, players: list[str]=[], admins: list[str]=[], point: int=10) -> None:
        self.name = name
        self.players = players
        self.admins = admins
        self.point = point
    
    def __repr__(self):
        return f"<Team {self.name}>"