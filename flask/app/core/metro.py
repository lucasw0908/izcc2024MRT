import json
import random
import requests
import logging
import os
from typing import overload
from ..game_config import DELETE_STATIONS, API_URL, IS_SPECIAL


log = logging.getLogger(__name__)

class Station:
    """
    Properties
    ----------
    sequence: :type:`int`
        The sequence of the station.
        e.g. 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...
        
    id: :type:`str`
        The id of the station.
        e.g. "BL01", "BL02", "BL03", "BL04", "BL05", "BL06", "BL07", "BL08", "BL09", "BL10", ...
        
    name: :type:`str`
        The name of the station in Chinese.
        
    english_name: :type:`str`
        The name of the station in English.
        
    distance: :type:`float`
        The distance of the station from the starting point of the line.
        
    point: :type:`int`
        The point of the station.
        
    is_special: :type:`bool`
        If the station is a special station.
        
    team: :type:`str`
        which team owns the station.
    """
    
    @overload
    def __init__(self, station: dict) -> None:
        self.sequence = None
        self.id = None
        self.name = None
        self.english_name = None
        self.distance = None
        self.point = None
        self.is_special = False
        self.team = None
        
        
    def __init__(self, station: dict) -> None:
        self.__dict__.update({
            "sequence": int(station["Sequence"]),
            "id": str(station["StationID"]),
            "name": str(station["StationName"]["Zh_tw"]),
            "english_name": str(station["StationName"]["En"]),
            "distance": float(station["CumulativeDistance"]),
            "point": random.choice([20, 35, 50]),
            "is_special": random.random() <= IS_SPECIAL,
        })
    
    
    def __str__(self) -> str:
        return self.name
    
    
    def __repr__(self) -> str:
        return self.name


class MetroSystem:
    """
    Properties
    ----------
    `station_name`: :class:`Station`
        The station object.
    """
    
    def __init__(self) -> None:
        self.graph = {}
        headers = {
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Accept": "application/json",
        }
        
        response = requests.get(API_URL, headers=headers).json()
        
        if response is None:
            raise ConnectionError()
        
        if "message" in response:
            log.error(response["message"])
            with open(os.path.join(os.path.dirname(__file__), "api_data.json"), "r", encoding="utf-8") as file:
                response = json.load(file)
        
        for line in response:
            for station in line["Stations"]:
                setattr(self, station["StationName"]["Zh_tw"], Station(station))
                
        for line in response:
            for index, station in enumerate(line["Stations"]):
                current_station_name = station["StationName"]["Zh_tw"]
                if current_station_name not in self.graph:
                    self.graph[current_station_name] = []
                    
                if index != 0:
                    station_name = line["Stations"][index - 1]["StationName"]["Zh_tw"]
                    if station_name not in DELETE_STATIONS:
                        self.graph[current_station_name].append(station_name)
                        
                if index != len(line["Stations"]) - 1:
                    station_name = line["Stations"][index + 1]["StationName"]["Zh_tw"]
                    if station_name not in DELETE_STATIONS:
                        self.graph[current_station_name].append(station_name)
                    
        self.graph["七張"].append("小碧潭")
        self.graph["小碧潭"].append("七張")
        
        self.delete_stations()
            
    
    def find_station(self, name: str) -> Station | None:
        """
        Find the station object by station name.
        
        Parameters
        ----------
        name: :type:`str`
            The name of the station.
            
        Returns
        -------
        station: :class:`Station`
            The station object.
        """
                
        return self.__dict__.get(name, None)
    
    
    def move(self, name: str) -> list[str] | None:
        """
        Calculate the possible stations to move.
        
        Parameters
        ----------
        name: :type:`str`
            The name of the current station.
            
        Returns
        -------
        choice: :type:`list[str]`
            The list of possible station ids to move.
        """
        
        return self.graph.get(name, None)
    
    
    def delete_stations(self) -> None:
        for station_name in DELETE_STATIONS:
            self.graph.pop(station_name, None)
            delattr(self, station_name)
            
        for current_station_name in self.graph:
            for station_name in self.graph[current_station_name]:
                if station_name in DELETE_STATIONS:
                    self.graph[station_name].remove(station_name)