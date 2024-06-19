from typing import Any, overload


class Card:
    def __init__(self) -> None:
        self.name: str = None
        self.description: str = None
        self.point: int = 0
    
    @overload
    def run(self) -> Any: ...