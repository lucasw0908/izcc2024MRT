import json
import os

path = os.path.dirname(os.path.abspath(__file__))

GAME_CONFIG = json.load(open(path + "/game_config.json"))
STATION_POINTS = GAME_CONFIG["station_points"]
SPECIAL_STATIONS = GAME_CONFIG["special_stations"]
API_URL = r"https://tdx.transportdata.tw/api/basic/v2/Rail/Metro/StationOfLine/TRTC?%24top=10000&%24format=JSON"