import requests
from typing import overload
from ..game_config import STATION_POINTS, SPECIAL_STATIONS, API_URL


class MetroGraph:
    encode_table: dict[str, int] = {}
    decode_table: dict[int, str] = {}
    graph: list[list[str]] = []

class Station:
    """
    Properties
    ----------
    sqeuence: :type:`int`
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
    """
    @overload
    def __init__(self, station: dict) -> None:
        self.sqeuence = None
        self.id = None
        self.old_id = None
        self.name = None
        self.english_name = None
        self.distance = None
        self.point = None
        self.is_special = False
        
    def __init__(self, station: dict) -> None:
        self.__dict__.update({
            "sequence": int(station["Sequence"]),
            "id": str(station["StationID"]),
            "name": str(station["StationName"]["Zh_tw"]),
            "english_name": str(station["StationName"]["En"]),
            "distance": float(station["CumulativeDistance"]),
            "point": int(STATION_POINTS[station["StationName"]["Zh_tw"]]) if station["StationName"]["Zh_tw"] in STATION_POINTS else 0,
            "is_special": station["StationName"]["Zh_tw"] in SPECIAL_STATIONS,
        })
        
        
    def encode(self, station_id: str) -> int:
        return MetroGraph.encode_table[station_id[:-2]] * 100 + int(station_id[-2:])
    
    def decode(self, code: int) -> str:
        if code // 100 not in MetroGraph.decode_table:
            return None
        return MetroGraph.decode_table[code // 100] + str(code % 100).zfill(2)

        

class Line:
    """
    Properties
    ----------
    name: :type:`str`
        The name of the line.
    
    `station_id`: :class:`Station`
        The station object.
    """
    def __init__(self, line: dict) -> None:
        
        self.name = line["LineID"]
        
        for station in line["Stations"]:
            setattr(self, station["StationID"], Station(station))


class Metro:
    """
    Properties
    ----------
    `line_id`: :class:`Line`
        The line object.
    """
    def __init__(self) -> None:   
        index = 1
        headers = {
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Accept": "application/json",
        }
        
        response = requests.get(API_URL, headers=headers).json()
        if response is None:
            raise ConnectionError()
        
        for line in response:
            MetroGraph.encode_table[line["LineID"]] = index
            MetroGraph.decode_table[index] = line["LineID"]
            setattr(self, line["LineID"], Line(line))
            index += 1
            
            
    def find_line(self, station_id: str) -> Line | None:
        """
        Find the line object by station id.
        
        Parameters
        ----------
        station_id: :type:`str`
            The id of the station.
            
        Returns
        -------
        line: :class:`Line`
            The line object.
        """
        
        for line in self.__dict__.values():
            if station_id in line.__dict__.keys():
                return line
            
        return None
            
    def find_station(self, station_id: str) -> Station | None:
        """
        Find the station object by station id.
        
        Parameters
        ----------
        station_id: :type:`str`
            The id of the station.
            
        Returns
        -------
        station: :class:`Station`
            The station object.
        """
        
        for line in self.__dict__.values():
            for station in line.__dict__.values():
                if station.id == station_id:
                    return station
                
        return None
    
    def find_station_by_name(self, name: str) -> Station | None:
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
        
        for line in self.__dict__.values():
            for station in line.__dict__.values():
                if station.name == name:
                    return station
                
        return None