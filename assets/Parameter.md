# Parameter

`LANGUAGE`：The response language of api. Default is "en".

`ADMINS`：The list of admin's discord username.

`CARD_COUNT`：The number of card in the game.

`DISTANCE`：
The minimum effective distance between the team and the station.
Default is 500.0.

`START_STATION`：The default start station of every team.

`END_STATION`：The goal station of every team.

`DELETE_STATIONS`：The stations that will not be used in the game.

`STATION_POINTS`：The points of every difficults of station.

`IS_SPECIAL`：
The probability of every station to be a special station.
Default is 0.3.

`IS_HIDDEN`：
The probability of every normal(not prison or special) station to be a hidden station.
Default is 0.1.

`IMPRISONED_TIME`：
The time of being imprisoned for every team.

- `min`: The minimum time (minute) of being imprisoned. Default is 5.
- `max`: The maximum time (minute) of being imprisoned. Default is 20.

`COLLAPSE`：
The collapse setting of the game.

- `status`: The status code of collapse.
- `time`: The time of this collapse. e.g. `"16:00"`
- `final`: is this the final collapse.
- `stations`: The stations that will collapse.
if `final` is `True`, this field will be ignored.

`COLLAPSE_DAMAGE_INTERVAL`：
The interval of collapse damage in minute.
Default is 10.

`COLLAPSE_DAMAGE`：
The damage of collapse.
Default is 10.

`COLLAPSE_LIST`：The list of stations that collapsed in the beginning.
