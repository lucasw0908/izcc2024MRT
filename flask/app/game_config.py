import json

from .config import BASEDIR


GAME_CONFIG = json.load(open(BASEDIR + "/game_config.json", "r", encoding="utf-8"))
STATION_POINTS = GAME_CONFIG["station_points"]
SPECIAL_STATIONS = GAME_CONFIG["special_stations"]
API_URL = r"https://tdx.transportdata.tw/api/basic/v2/Rail/Metro/StationOfLine/TRTC?%24top=10000&%24format=JSON"