# 捷運大富翁

## 目錄

- [簡介](#簡介)
- [遊戲內容](#遊戲內容)
- [介面介紹](#介面介紹)
- [遊戲設定](#遊戲設定)
- [貢獻名單](#貢獻名單)
- [歷史版本](#歷史版本)

## 簡介

由IZCC共同開發，作為社團內具特色的一個活動，在社團內的暑訓、寒訓等活動皆可使用，遊戲結合了現實的團隊活動與資訊科技的應用，目標是希望能讓參與者藉由資訊社的活動體驗資訊科技帶來的娛樂與應用。

## 遊戲內容

### 遊玩方式

進行方式與普通大富翁大致相同，有擲骰子、佔領地盤、機會命運等等，而我們另外新增了任務系統，到達每站時，需要完成該站特定的任務（任務完成後即佔領該站），才可擲骰子，往下一站移動。(擲骰子->選下一站->過任務->特殊站進入抽卡階段)

### 計分方式

#### 加分

- 完成無人土地的任務 (根據設定內對應難度的分數進行扣分)
- 卡片 (卡片效果需手動加分)
- 組合

#### 扣分

- 縮圈
- 卡片 (卡片效果需手動扣分)

#### 備註

- 踩到自己的站：0
- 踩到別人的站：依照難易度扣分 (完成任務後：0)

### 起點

各小隊會抽籤分散到各顏色的線，等到所有小隊到達各自起點後統一開始。

- 台北車站往頂埔方向
- 台電大樓往松山方向
- 大安往南港展覽館方向
- 松江南京往迴龍/蘆洲方向
- 忠孝新生往南勢角方向

### 縮圈

指定時間後會開始往終點縮圈，需注意自己所在的位置，如果持續留在圈外則會被扣分

- 第一階段 15:00
- 第二階段 16:00
- 第三階段 17:00  

### 站點

可透過點擊獲得站點資訊，包含以下資訊

- 是否為特殊站
- 佔領隊伍
- 任務敘述
- 任務提示
- 任務難度
- 任務出口

### 一般站

包含一個任務，且點擊可獲得任務提示，完成任務後可佔領該站並獲得對應難度之分數，若是其他小隊行經我方佔領之站點，則須繳交相對應之分數

### 特殊站

- 存在任務
- 特殊站在小隊到達前皆為隱藏狀態

特殊站會顯示在地圖上，過完該站任務後可進行抽卡，有加分扣分以及額外任務。(目前有26張卡片)

### 監獄站

- 不存在任務
- 監獄站在小隊到達前皆為隱藏狀態

到達監獄站會進入隨機的囚禁時間，囚禁時間內無法進行擲骰子、完成任務等動作，時間上下限可在一般遊戲設定中進行設定

## 介面介紹

### 首頁

- 地圖 (點擊可獲得各站資訊)
- 各小隊資訊 (位置、分數)
- 點擊各小隊位置的標籤（零小：），可獲得各隊佔領過的站
- 分數變更歷史

### 組合

顯示有哪些組合可以額外加分，已造訪的站點會變成綠色，反之為紅色，完成後系統會自動加分

### 隊隨

- 骰子
- 抽卡
- 完成任務
- 跳過任務
- 常用設定
- 進階設定

### 常用設定

- 增減小隊員
- 加減分(抽完卡後需要)

### 進階設定

- 創建 / 刪除 / 重設隊伍
- 分數控制
- 遊戲開始 / 結束

## 遊戲設定

### 一般遊戲設定

所有設定皆在
[game_config.json](https://github.com/lucasw0908/izcc2024MRT/blob/main/flask/app/data/game_config.json)
中進行設定，且改變設定後須重新啟動程式以套用設定，
另外參數說明可在
[game_config.py](https://github.com/lucasw0908/izcc2024MRT/blob/main/flask/app/game_config.py)
亦或是參數說明文件中獲取更詳細的資訊

- [參數說明文件](https://github.com/lucasw0908/izcc2024MRT/blob/main/assets/Parameter.md)

### 站點資訊設定

所有設定皆在
[station_info.json](https://github.com/lucasw0908/izcc2024MRT/blob/main/flask/app/data/station_info.json)
中進行設定，且改變設定後須重新啟動程式以套用設定

範例格式如下

```json=
{
    "南勢角": {
        "Mission": "到興南夜市門口拍合照",
        "Tips": "出去後往左邊走",
        "Exit": "4號出口",
        "Difficult": 1
    },
    "景安": {
        "Mission": "跟中和四面佛合照",
        "Tips": "走到對面右轉",
        "Exit": "景平路",
        "Difficult": 1
    },
}
```

### 組合資訊設定

所有設定皆在
[combo.json](https://github.com/lucasw0908/izcc2024MRT/blob/main/flask/app/data/combo.json)
中進行設定，且改變設定後須重新啟動程式以套用設定

範例格式如下

```json=
[   
    {
        "name": "IZCC",
        "point": 100,
        "stations": ["中正紀念堂","松江南京","善導寺","七張"]
    },
    {
        "name": "山山山山",
        "point": 100,
        "stations": ["芝山","圓山","象山","松山"]
    },
]
```

## 開發說明

### API

若是需要改變前端的呈現，可參考此資料對API進行交互藉此控制遊戲核心

- [API文件](https://github.com/lucasw0908/izcc2024MRT/blob/main/assets/API.md)

文件內說明可能有遺漏或版本不符等問題，最新版本之API說明可參考

- [api.py](https://github.com/lucasw0908/izcc2024MRT/blob/main/flask/app/views/api.py)
- [admin_api.py](https://github.com/lucasw0908/izcc2024MRT/blob/main/flask/app/views/admin_api.py)

### 紀錄日誌

所有紀錄日誌皆儲存於
[logs](https://github.com/lucasw0908/izcc2024MRT/tree/main/flask/app/logs)
資料夾內，詳細可參閱資料夾內說明文件

### 狀態代碼

為了本地化支援，本專案使用狀態代碼作為後端回傳之說明訊息

如欲新增語言可至以下資料夾內新增對應語言之翻譯文件

- [status codes](https://github.com/lucasw0908/izcc2024MRT/tree/main/flask/app/status_codes)

詳細狀態代碼資訊可參考文件內容，預設為英文文件如下：

```=
{
    "S00000": "Success.",
    
    "S00001": "Invalid Request.",
    "S00002": "Invalid Name.",
    "S00003": "Invalid Station.",
    "S00004": "Invalid Team.",
    "S00005": "Invalid Player.",
    "S00006": "Invalid Location.",
    "S00007": "Invalid Mission.",
    "S00010": "Invalid Type.",

    "S10001": "Station Error",
    
    "S20001": "Team Error",
    "S20002": "Team is imprisoned.",
    "S20003": "Team is already exist.",
    
    "S30001": "Player Error",
    "S30002": "Player is not in any team.",
    
    "S40001": "Location Error",
    "S40002": "Location not reached.",
    
    "S50001": "Mission Error",
    "S50002": "Mission not finished.",
    "S50003": "Mission already finished.",

    "S90001": "Localization file not found.",
    
    "S99999": "Game Over"
}
```

## 貢獻名單

### 主要開發者

- [000](https://github.com/lucasw0908)：後端開發、遊戲核心設計、API設計、前端開發協助、文件撰寫
- [A1u](https://github.com/ayooooou)：前端開發、介面設計、捷運圖製作、串接API、文件撰寫
- [samuelhsieh0829](https://github.com/samuelhsieh0829)：前端開發、介面設計、串接API、伺服器維運與相關文件配置

### 其他開發者

- [FranzLee](https://github.com/FranzLee)：擲骰子介面撰寫
- [IanWen](https://github.com/IanWen103026)：優化擲骰子介面設計

## 歷史版本

- [2021](https://github.com/IZCC111/izcc-2021-winter-metro)
- [2022](https://github.com/Timothychen00/izcc2022MRT)
- [2023](https://github.com/ddd-dong/izcc2023MRT)
