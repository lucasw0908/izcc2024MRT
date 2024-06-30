import json

from .config import BASEDIR


GAME_CONFIG = json.load(open(BASEDIR + "/game_config.json", "r", encoding="utf-8"))
CARD = GAME_CONFIG["card"]
STATION_POINTS = GAME_CONFIG["station_points"]
SPECIAL_STATIONS = GAME_CONFIG["special_stations"]
DELETE_STATIONS = GAME_CONFIG["delete_stations"]
START_STATION = GAME_CONFIG["start_station"]
COLLAPSE = GAME_CONFIG["collapse"]
API_URL = r"https://tdx.transportdata.tw/api/basic/v2/Rail/Metro/StationOfLine/TRTC?%24top=10000&%24format=JSON"