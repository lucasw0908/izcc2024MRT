import json

from .data import load_data


GAME_CONFIG = load_data("game_config")
ADMINS = GAME_CONFIG["admins"]
CARD = GAME_CONFIG["card"]
START_STATION = GAME_CONFIG["start_station"]
END_STATION = GAME_CONFIG["end_station"]
DELETE_STATIONS = GAME_CONFIG["delete_stations"]
IS_SPECIAL = GAME_CONFIG["is_special"]
COLLAPSE = GAME_CONFIG["collapse"]
COLLAPSE_LIST = []
API_URL_TP = r"https://tdx.transportdata.tw/api/basic/v2/Rail/Metro/StationOfLine/TRTC?%24top=10000&%24format=JSON"
API_URL_NTP = r"https://tdx.transportdata.tw/api/basic/v2/Rail/Metro/StationOfLine/NTMC?%24top=10000&%24format=JSON"