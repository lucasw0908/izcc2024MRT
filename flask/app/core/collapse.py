from ..game_config import COLLAPSE

class Collapse:
    def __init__(self) -> None:
        self.status = 0
        self.warning = False
        self.next_time = COLLAPSE[0]["time"]