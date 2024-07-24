import re
import os
import json

from ..game_config import LANGUAGE


class StatusCodes:
    S00000 = "Success"
    
    S00001 = "Invalid Request."
    S00002 = "Invalid Name."
    S00003 = "Invalid Station."
    S00004 = "Invalid Team."
    S00005 = "Invalid Player."
    S00006 = "Invalid Location."
    S00007 = "Invalid Mission."
    S00008 = "Invalid Language."
    S00010 = "Invalid Type."

    S10001 = "Station Error"
    
    S20001 = "Team Error"
    S20002 = "Team is imprisoned."
    S20003 = "Team is already exist."
    
    S30001 = "Player Error"
    S30002 = "Player is not in any team."
    
    S40001 = "Location Error"
    S40002 = "Location not reached."
    
    S50001 = "Mission Error"
    S50002 = "Mission not finished."
    S50003 = "Mission already finished."
    
    S90001 = "Localization file not found."
    
    
    def __init__(self, language: str=None) -> None:
        self.codes = []
        if language is not None:
            self.localization(language)
            
        for code, message in self.__dict__.items():
            if callable(message): continue
            self.codes.append(code)
    
    def localization(self, language: str, is_return: bool=False) -> None:
        
        if re.match(r"^[A-Za-z0-9-_]+$", language) is None:
            raise ValueError(self.S00008)
        
        filename = language + ".json"
        if not os.path.exists(os.path.join(os.path.dirname(__file__), filename)):
            raise FileNotFoundError(self.S90001)
        
        with open(os.path.join(os.path.dirname(__file__), filename), "r", encoding="utf-8") as f:
            data: dict[str, str] = json.load(f)
            
            if is_return:
                return data
            else:
                for code, message in data.items():
                    setattr(self, code, message)
                
                
STATUS_CODES = StatusCodes(LANGUAGE)