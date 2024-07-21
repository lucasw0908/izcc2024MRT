import json
import random
import requests
import logging
import os
from typing import Any

from ..config import BASEDIR
from ..game_config import DELETE_STATIONS, IS_SPECIAL, API_URL_TP, API_URL_NTP, LOCATION_API_URL_TP, LOCATION_API_URL_NTP
from ..data import load_data


log = logging.getLogger(__name__)
headers = {
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

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
        
    difficult: :type:`int`
        The difficult of the station.
    
    exit: :type:`str`
        The exit of the station.
        
    mission: :type:`str`
        The mission description of the station.
        
    tips: :type:`str`
        The tips of the mission.
        
    is_special: :type:`bool`
        If the station is a special station.
        
    is_prison: :type:`bool`
        If the station is a prison station.
        
    geohash: :type:`str`
        The geohash of the station.
        
    team: :type:`str`
        which team owns the station.
              
    point: :type:`int`
        The point of the station.
    """
        
    def __init__(self, station: dict) -> None:
        self.sequence: int
        self.id: str
        self.name: str
        self.english_name: str
        self.distance: float
        self.difficult: int
        self.exit: str
        self.mission: str
        self.tips: str
        self.is_special: bool
        self.is_prison: bool
        self.point: int
        self.geohash: str
        self.hidden: bool
        
        self.team: str = None
        
        self.__dict__.update({
            "sequence": int(station["Sequence"]),
            "id": str(station["StationID"]),
            "name": str(station["StationName"]["Zh_tw"]),
            "english_name": str(station["StationName"]["En"]),
            "distance": float(station["CumulativeDistance"]),
            "difficult": int(station["Difficult"]),
            "exit": str(station["Exit"]),
            "mission": str(station["Mission"]),
            "tips": str(station["Tips"]),
            "is_special": random.random() <= IS_SPECIAL,
            "is_prison": station["Mission"] == "監獄",
            "point": {1: 20, 2: 35, 3: 50}.get(station["Difficult"], 0),
            "geohash": str(station["geohash"]),
        })
        
        self.hidden = self.is_special or self.is_prison
    
    
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
        self.graph: dict[str, list] = {}
        self.station_info: dict[str, dict] = load_data("station_info")
        self.station_location: dict[str, str] = {}
        self.is_loaded: bool = False
        self._load_location(LOCATION_API_URL_TP)
        self._load_location(LOCATION_API_URL_NTP)
        self._load(API_URL_TP)
        self._load(API_URL_NTP)
        self.is_loaded = True
            
            
    def _load_location(self, url: str, save: bool=False) -> None:
        
        if self.station_location:
            return None
        
        response: list[dict] = requests.get(url, headers=headers).json()
        
        if "message" in response:
            log.error(response["message"])
            response = load_data("station_location")
                
        if save:
            with open(os.path.join(BASEDIR, "data", "station_location.json"), "r+", encoding="utf-8") as file:
                data: list = json.load(file)
                for station in response:
                    if station not in data:
                        data.append(station)
                json.dump(data, file, ensure_ascii=False, indent=4)
                
        self.station_location = {sl["StationName"]["Zh_tw"]: sl["StationPosition"]["GeoHash"] for sl in response}
        
        
    def _load(self, url: str, save: bool=False) -> None:
        
        if self.is_loaded:
            return None
        
        response: list[dict] = requests.get(url, headers=headers).json()
        
        if "message" in response:
            log.error(response["message"])
            response = load_data("api_data")
            self.is_loaded = True
                
        if save:
            with open(os.path.join(BASEDIR, "data", "api_data.json"), "r+", encoding="utf-8") as file:
                data: list = json.load(file)
                for line in response:
                    if line not in data:
                        data.append(line)
                json.dump(data, file, ensure_ascii=False, indent=4)
        
        for line in response:
            for station in line["Stations"]:
                station: dict[str, Any]
                
                current_station_name: str = station["StationName"]["Zh_tw"]
                
                if current_station_name in self.station_info:
                    station.update(self.station_info[current_station_name])
                else:
                    station.update({"Mission": "無", "Exit": "不限", "Difficult": 0, "Tips": "無"})
                    
                station["geohash"] = self.station_location.get(current_station_name, None)
                
                setattr(self, station["StationName"]["Zh_tw"], Station(station))
                
        for line in response:
            for index, station in enumerate(line["Stations"]):
                
                current_station_name: str = station["StationName"]["Zh_tw"]
                current_station_id: str = station["StationID"]
                
                if current_station_name not in self.graph:
                    self.graph[current_station_name] = []
                    
                if current_station_id.endswith("A"):
                    for station in line["Stations"]:
                        if station["StationID"] == current_station_id[:-1]:
                            station_name = station["StationName"]["Zh_tw"]
                            if station_name not in DELETE_STATIONS:
                                self.graph[current_station_name].append(station_name)
                                self.graph[station_name].append(current_station_name)
                    
                else:
                    if index != 0:
                        station_name = line["Stations"][index - 1]["StationName"]["Zh_tw"]
                        if station_name not in DELETE_STATIONS:
                            self.graph[current_station_name].append(station_name)
                            
                    if index != len(line["Stations"]) - 1:
                        station_name = line["Stations"][index + 1]["StationName"]["Zh_tw"]
                        if station_name not in DELETE_STATIONS:
                            self.graph[current_station_name].append(station_name)
                
        
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
            if station_name in self.__dict__:
                delattr(self, station_name)
            
        for current_station_name in self.graph:
            for station_name in self.graph[current_station_name]:
                if station_name in DELETE_STATIONS:
                    self.graph[station_name].remove(station_name)