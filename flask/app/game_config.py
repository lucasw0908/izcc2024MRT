import json

from .config import BASEDIR


GAME_CONFIG = json.load(open(BASEDIR + "/game_config.json", "r", encoding="utf-8"))
CARD = GAME_CONFIG["card"]
START_STATION = GAME_CONFIG["start_station"]
DELETE_STATIONS = GAME_CONFIG["delete_stations"]
IS_SPECIAL = GAME_CONFIG["is_special"]
COLLAPSE = GAME_CONFIG["collapse"]
API_URL_TP = r"https://tdx.transportdata.tw/api/basic/v2/Rail/Metro/StationOfLine/TRTC?%24top=10000&%24format=JSON"
API_URL_NTP = r"https://tdx.transportdata.tw/api/basic/v2/Rail/Metro/StationOfLine/NTMC?%24top=10000&%24format=JSON"