from typing import Any, overload


class Card:
    def __init__(self) -> None:
        self.point = 0
    
    @overload
    def run(self) -> Any: ...