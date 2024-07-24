# API

All of api request are `get` method, and use `/api` as url prefix.

- `/status_codes/<language: str>` : Get the localization status codes data.

Returns : `json`

```json
{
    "S00001": "Invalid Request.",
    "S00002": "Invalid Name.",
    "S00003": "Invalid Station.",
    "S00004": "Invalid Team.",
    "S00005": "Invalid Player.",
    "S00006": "Invalid Location.",
    "S00007": "Invalid Mission.",
    "S00010": "Invalid Type.",
    ...
}
```

---

## Player Only API

- `/graph` : Get the graph linked-list data.

Returns : `json`

```json
{
    "Station1": [
        "Neighbor1",
        "Neighbor2",
        ...
    ],
    "Station2": [
        "Neighbor1",
        "Neighbor2",
        ...
    ],
    ...
}
```

---

- `/station/<station_name: str>` : Get the station data.

Returns : `json`

```json
{
    "difficult": 2,
    "distance": 7.45,
    "english_name": "Fuzhong",
    "exit": "1號出口",
    "geohash": "wsqq7beuy",
    "hidden": false,
    "id": "BL06",
    "is_prison": false,
    "is_special": false,
    "mission": "找到燒肉アニキ，請一位店員在店門旁的圖案與小隊合照",
    "name": "府中",
    "point": 35,
    "sequence": 6,
    "team": null,
    "tips": "店家如下圖，在全家那側，這一鍋附近"
}
```

---

- `/stations` : Get the `list` of all stations data.

Returns : `json`

---

- `/collapse_status` : Get the collapse status.

Returns : `json`

```json
{
  "status": 0,
  "warning": false
}
```

---

- `/next_collapse_time` : Get the time of next collapse.

Returns : `json`

```json
"15:00"
```

---

- `/combo` : Get the combos data from [`combo.json`](https://github.com/lucasw0908/izcc2024MRT/blob/main/flask/app/data/combo.json)

Returns : `json`

```json
{
    "name": "台北城",
    "point": 100,
    "stations": [
        "東門",
        "西門",
        "北門",
        "小南門"
    ]
},
{
    "name": "8+9",
    "point": 100,
    "stations": [
        "龍山寺",
        "善導寺",
        "先嗇宮",
        "行天宮"
    ]
},
...
```

---

- `/team/<team_name: str>` : Get the team data.

Returns : `json`

```json
{
    "admins": [
        "lucasw0",
        "a.uuu",
        "e04._.40e",
        "ianwen_is_a_sheep"
    ],
    "choice": [],
    "combos": [],
    "current_card": null,
    "current_mission_finished": true,
    "imprisoned_time": 0,
    "is_imprisoned": false,
    "location": "中正紀念堂",
    "name": "admins",
    "players": [],
    "point": 10,
    "stations": [],
    "step": 0,
    "target_location": null
}
```

---

- `/teams` : Get the `list` of all teams data.

Returns : `json`

---

## Admin Only API

- `/create_team/<team_name: str>/<station: str>` : Create a team with name and starting station.

Returns : `Success`, `Invalid Name`, `Invalid Station`, `Team is already exist`

---

- `/delete_team/<team_name: str>` : Delete a team with name.

Returns : `Success`, `Invalid Team`

---

- `/join_team/<team_name: str>/<player_name: str>/<is_admin: bool>` : Let the player join the team. You can input a undefined player name, that will allow the player join the team after first login.

Returns : `Success`, `Invalid Team`

---

- `/leave_team/<player_name: str>` : Let the player leave the team.

Returns : `Success`, `Player is not in any team`

---

- `/move/<team_name: str>` : The first stage of this round. Let the team dice and choose the station you can go next.

Returns: `json`, `Invalid Team`, `Team is imprisoned`, `Mission not finished`

```json
{
    "step": 2,
    "choice": ["七張", "景美"]
}
```

---

- `/move_to_location/<name: str>/<location: str>` : The second stage of this round. Set the target station of the team.

Returns: `json`, `Invalid Team`, `Invalid Location`, `Team is imprisoned`, `Mission not finished`

```json
{
    "combos": ["台北城", "8+9"],
    "point": 200
}
```

---

- `/finish_mission/<mission_name: str>` : The third stage of this round. Told system mission finished. If the station is special, you will get the `card` (filename) in response.

Returns: `card`, `Success`, `Invalid Team`, `Team is imprisoned`, `Location not reached`, `Mission already finished`

---

- `/add_point/<name: str>/<point: int>` : Add team point.

Returns: `Success`, `Invalid Team`

---

- `/set_point/<name: str>/<point: int>` : Set team point.

Returns: `Success`, `Invalid Team`

---

- `/gps_location/<name: str>/<latitude: float>/<longitude: float>` : Update the current location of the team.

Returns: `json`, `Invalid Team`, `Invalid Location`, `Team is imprisoned`

```json
{
    "location": "中山",
    "distance": 20.0
}
```

---
