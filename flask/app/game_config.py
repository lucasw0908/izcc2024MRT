from .data import load_data


GAME_CONFIG = load_data("game_config")

LANGUAGE: str = GAME_CONFIG.get("language", "en")
"""The response language of api, default is "en". """

ADMINS: list[str] = GAME_CONFIG.get("admins", [])
"""The list of admin's discord username."""

CARD_COUNT: int = GAME_CONFIG.get("card_count")
"""The number of card in the game."""

DISTANCE: float = GAME_CONFIG.get("distance")
"""The minimum effective distance between the team and the station."""

START_STATION: str = GAME_CONFIG.get("start_station")
"""The default start station of every team."""

END_STATION: str = GAME_CONFIG.get("end_station")
"""The goal station of every team."""

DELETE_STATIONS: list[str] = GAME_CONFIG.get("delete_stations")
"""The stations that will not be used in the game."""

IS_SPECIAL: float = GAME_CONFIG.get("is_special")
"""The probability of every station to be a special station."""

IMPRISONED_TIME: dict[str, int] = GAME_CONFIG.get("imprisoned_time")
"""The time of being imprisoned for every team.
`min`(:type:`int`): The minimum time (minute) of being imprisoned.
`max`(:type:`int`): The maximum time (minute) of being imprisoned.
"""
COLLAPSE: list[dict] = GAME_CONFIG.get("collapse")
"""The collapse setting of the game.
`status`(:type:`int`): The status code of collapse.
`time`(:type:`str`): The time of this collapse. e.g. `"16:00"`
`final`(:type:`bool`): is this the final collapse.
`stations`(:type:`list[str]`): The stations that will collapse. if `final` is `True`, this field will be ignored.
"""

COLLAPSE_DAMAGE_INTERVAL: int = GAME_CONFIG.get("collapse_damage_interval")
"""The interval of collapse damage in minute."""

COLLAPSE_DAMAGE: int = GAME_CONFIG.get("collapse_damage")
"""The damage of collapse."""

COLLAPSE_LIST: list[str] = GAME_CONFIG.get("collapse_list")
"""The list of stations that collapsed in the beginning."""


API_URL_TP = r"https://tdx.transportdata.tw/api/basic/v2/Rail/Metro/StationOfLine/TRTC?%24top=10000&%24format=JSON"  # 北捷站點資料
LOCATION_API_URL_TP = r"https://tdx.transportdata.tw/api/basic/v2/Rail/Metro/Station/TRTC?%24top=10000&%24format=JSON"  # 北捷站點位置
API_URL_NTP = r"https://tdx.transportdata.tw/api/basic/v2/Rail/Metro/StationOfLine/NTMC?%24top=10000&%24format=JSON"  # 環狀線站點資料
LOCATION_API_URL_NTP = r"https://tdx.transportdata.tw/api/basic/v2/Rail/Metro/Station/NTMC?%24top=10000&%24format=JSON"  # 環狀線站點位置
