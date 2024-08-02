// ready
document.addEventListener("DOMContentLoaded", () => {
    showMap();
    showCollapse_time();
    showPoint();
    showLocate();
    showImprisoned();
    showPointchart();
    showDistance();
    resizeMap();
    window.addEventListener('resize', resizeMap);
    window.addEventListener('load', resizeMap);
});


// repeat
setInterval(showMap, 10000);
setInterval(showCollapse_time, 10000);
setInterval(showPoint, 10000);
setInterval(showLocate, 10000);
setInterval(showImprisoned, 10000);
setInterval(showDistance,10000);

function resizeMap() {
    const img = document.querySelector('.MRT_map img[style*="display: block"]');
    if (!img) return;  // No visible image
    const map = document.querySelector('map[name="image-map"]');
    const areas = map.getElementsByTagName('area');
    const imgWidth = img.naturalWidth;
    const imgHeight = img.naturalHeight;
    const widthRatio = img.width / imgWidth;
    const heightRatio = img.height / imgHeight;

    for (let i = 0; i < areas.length; i++) {
        const originalCoords = areas[i].getAttribute('data-original-coords').split(',').map(Number);
        const newCoords = originalCoords.map((coord, index) => {
            return index % 2 === 0 ? coord * widthRatio : coord * heightRatio;
        });
        areas[i].setAttribute('coords', newCoords.join(','));
    }
    mapReady = true;
    document.querySelector('.MRT_map').style.pointerEvents = 'auto'; // 啟用點擊事件
}


let lastStatus = null;
let lastWarning = null;

async function showMap() {
    try {
        const response = await fetch(`/api/collapse_status`);
        const data = await response.json();

        if (data.status !== lastStatus || data.warning !== lastWarning) {
            lastStatus = data.status;
            lastWarning = data.warning;
            let images = document.querySelectorAll('.MRT_map img');
            images.forEach(img => img.style.display = 'none');

            if (data.warning === false) {
                if (data.status === 0) {
                    document.getElementById('Map0').style.display = 'block';
                } else if (data.status === 1) {
                    document.getElementById('Map2').style.display = 'block';
                } else if (data.status === 2) {
                    document.getElementById('Map4').style.display = 'block';
                } else if (data.status === 3) {
                    document.getElementById('Map6').style.display = 'block';
                }
            } else {
                if (data.status === 0) {
                    document.getElementById('Map1').style.display = 'block';
                } else if (data.status === 1) {
                    document.getElementById('Map3').style.display = 'block';
                } else if (data.status === 2) {
                    document.getElementById('Map5').style.display = 'block';
                }
            }
        }
    }
    catch (error){
        console.error('Error fetching data:', error);
    }
}


async function checkImageExists(imageUrl) {
    try {
        const response = await fetch(imageUrl, { method: 'HEAD' });
        return response.ok;
    } catch (error) {
        return false;
    }
}
async function station_info(station_name) {
    const team = document.querySelector('#team').innerHTML;
    station_name = station_name.replace("/", "_");

    const swalInstance = Swal.fire({
        title: `${station_name.replace("_", "/")} 站點資訊`,
        html: '<div class="loading-container"><span>載入中</span><div class="chaotic-orbit"></div></div>',
        showConfirmButton: false,
        showCancelButton: false,
        customClass: { cancelButton: 'swal-button-yellow' },
        allowOutsideClick: false
    });

    try {
        const [data, team_data] = await Promise.all([
            fetch(`/api/station/${station_name}`).then(response => response.json()),
            fetch(`/api/team/${team}`).then(response => response.json())
        ]);

        const imageUrl = `../static/img/stations/${station_name}.jpg`;
        const exists = await checkImageExists(imageUrl);
        const imageHtml = exists ? `<img src="${imageUrl}" alt="${station_name} 圖片" style="width:60%; height:auto;">` : '';

        const lebel_image = (!data.is_special || station_name === team_data.location) ? imageHtml : "";
        let lebel_is_special = data.is_special ? "是" : "否";
        lebel_is_special = data.is_prison ? "是" : "否";
        const label_team = data.team ? data.team : "無人佔領";
        const label_depiction = (!data.is_special || station_name === team_data.location) ? data.mission : "隱藏";
        const label_exit = (!data.is_special || station_name === team_data.location) ? data.exit : "隱藏";
        const lebel_difficult = data.difficult === 1 ? "簡單" : data.difficult === 2 ? "普通" : data.difficult === 3 ? "困難" : null;

        station_name = station_name.replace("_", "/");

        const result = await Swal.fire({
            title: `${station_name} 站點資訊`,
            html: `
                <p>特殊站 : ${lebel_is_special}</p>
                <p>佔領的小隊 : ${label_team}</p>
                <p>任務敘述 : ${label_depiction}</p>
                <p>任務出口 : ${label_exit}</p>
                <p>任務難度: ${lebel_difficult}</p>
                ${lebel_image}
            `,
            showConfirmButton: true,
            confirmButtonText: "關閉",
            showCancelButton: true,
            cancelButtonText: "提示",
            customClass: { cancelButton: 'swal-button-yellow' }
        });

        // Handle the result of the Swal.fire
        if (result.dismiss === Swal.DismissReason.cancel) {
            Swal.fire({
                title: '提示',
                text: `${data.tips}`,
                confirmButtonText: "關閉"
            });
        }
    } catch (error) {
        console.error('Error fetching station or team data:', error);
        // Show error message
        Swal.fire({
            title: '錯誤',
            html: '無法載入站點資訊',
            showConfirmButton: true,
            confirmButtonText: "關閉"
        });
    }
}


const chineseNumerals = { '零': 0, '一': 1, '二': 2, '三': 3, '四': 4, };

async function showLocate() {
    try {
        const response = await fetch(`/api/teams`);
        const data = await response.json();

        data.forEach(team => {
            // 提取隊名中的數字部分，例如 "零小" -> "0"
            const chineseNumeral = team.name.charAt(0); // 假設隊名的第一個字符是中文數字
            const teamNumber = chineseNumerals[chineseNumeral];

            if (teamNumber !== undefined) {
                const locationElement = document.getElementById(`team${teamNumber}_location`);
                if (locationElement) {
                    locationElement.textContent = team.is_imprisoned ? `監獄⛓️` : `${team.location}`;
                }
            }
        });
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

async function showPoint() {
    try {
        const response = await fetch(`/api/teams`);
        const data = await response.json();
        const teams = document.querySelectorAll(".team");
        const maxScore = 3000;

        data.forEach(teamData => {
            const chineseNumeral = teamData.name.charAt(0); // 假設隊名的第一個字符是中文數字
            const teamNumber = chineseNumerals[chineseNumeral];

            if (teamNumber !== undefined && teams[teamNumber]) {
                const teamElement = teams[teamNumber];
                const score = teamData.point;
                const progressBar = teamElement.querySelector(".progress");
                const scoreElement = teamElement.querySelector(".score");

                teamElement.setAttribute("data-score", score);

                const widthPercent = (score / maxScore) * 100;
                progressBar.style.width = widthPercent + "%";

                scoreElement.textContent = `${score} 分`;
            }
        });
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}


async function showCollapse_time() {
    try {
        const response = await fetch(`/api/next_collapse_time`);
        const data = await response.json();
        const targetTime = parseTime(data);
        const interval = setInterval(() => {
            const now = new Date();
            const timeDiff = targetTime - now;

            if (timeDiff <= 0) {
                clearInterval(interval);
                document.getElementById('next_collapse_time_label').textContent = '載入中...';
            } else {
                const countdown = formatTimeDiff(timeDiff);
                document.getElementById('next_collapse_time_label').textContent = `崩塌倒數 : ${countdown}`;
            }
        }, 1000);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function parseTime(timeString) {
    // 假設 data 格式為 'HH:MM'
    const [hours, minutes] = timeString.split(':').map(Number);
    const now = new Date();
    const targetTime = new Date(now);
    targetTime.setHours(hours, minutes, 0, 0);
    
    // 如果目標時間已過，設定為下一天的目標時間
    if (targetTime <= now) {
        targetTime.setDate(targetTime.getDate() + 1);
    }
    return targetTime;
}

function formatTimeDiff(timeDiff) {
    const hours = Math.floor(timeDiff / (1000 * 60 * 60));
    const minutes = Math.floor((timeDiff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((timeDiff % (1000 * 60)) / 1000);

    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}


async function showImprisoned() {
    const team = document.querySelector('#team').innerHTML;
    try {
        const response = await fetch(`/api/team/${team}`);
        const data = await response.json();
        if (data.is_imprisoned) {
            document.getElementById('is_imprisoned_label').textContent = `監獄剩餘時間 : ${data.imprisoned_time} 分鐘`;
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}


function getCurrentLocation() {
    return new Promise((resolve, reject) => {
        const team = document.querySelector('#team').innerHTML;
        if (navigator.geolocation) {
            // 使用高精度模式
            const options = {
                enableHighAccuracy: true,
                timeout: 10000, // 10 秒超時
                maximumAge: 0 // 不使用緩存位置
            };
            
            navigator.geolocation.getCurrentPosition(async (position) => {
                try {
                    const { latitude, longitude } = position.coords;
                    const response = await fetch(`/api/gps_location/${team}/${latitude}/${longitude}`);
                    if (!response.ok) {
                        throw new Error(`HTTP 錯誤！狀態: ${response.status}`);
                    }
                    const data = await response.json();
                    resolve({ distance: data.distance, location: data.location });
                } catch (error) {
                    console.error('獲取數據時出錯:', error);
                    reject(error);
                }
            }, (error) => {
                // 處理定位錯誤
                switch(error.code) {
                    case error.PERMISSION_DENIED:
                        alert('使用者拒絕了地理位置請求。');
                        break;
                    case error.POSITION_UNAVAILABLE:
                        alert('位置信息不可用。');
                        break;
                    case error.TIMEOUT:
                        alert('請求地理位置超時。');
                        break;
                    case error.UNKNOWN_ERROR:
                        alert('發生未知錯誤。');
                        break;
                }
                reject(error);
            }, options);
        } else {
            alert('對不起，您的裝置不支援地理位置功能。');
            reject(new Error('Geolocation not supported'));
        }
    });
}


async function showDistance() {
    const team = document.querySelector('#team').innerHTML;
    const { distance, location } = await getCurrentLocation();
    const distanceInKm = (distance / 1000).toFixed(1);
    try {
        const response = await fetch(`/api/team/${team}`);
        const data = await response.json();
        if (data.target_location) {
            if (location) {
                document.getElementById('distance_label').textContent = `( 你們已到${data.target_location}站 )`;
            } else {
                document.getElementById('distance_label').textContent = `( 你們距離${data.target_location}站 ${distanceInKm} km )`;
            }
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}


document.addEventListener("DOMContentLoaded", async function() {
    let teamsData = [];

    try {
        const response = await fetch('/api/teams');
        const data = await response.json();
        teamsData = data;
        setupEventListeners();
    } catch (error) {
        console.error('Error fetching teams data:', error);
    }

    function setupEventListeners() {
        for (let i = 0; i <= 4; i++) {
            document.getElementById(`team${i}_location_lebel`).addEventListener("click", function() {
                owned_stations_alert(this.textContent);
            });
            document.getElementById(`team${i}_point_lebel`).addEventListener("click", function() {
                point_log_alert(this.textContent);
            });
        }
    }
    
    function owned_stations_alert(team) {
        const team_name = team.replace(':', '').trim();
        const teamData = teamsData.find(t => t.name === team_name);

        if (teamData) {
            const stationsList = teamData.owned_stations.length > 0 ? teamData.stations.join(', ') : '無';
            Swal.fire({
                title: `${team_name} 土地佔領`,
                html: `佔領站: ${stationsList}`,
                confirmButtonText: '關閉'
            });
        } else {
            Swal.fire({
                title: `錯誤`,
                html: `找不到隊伍: ${team_name}`,
                confirmButtonText: '關閉'
            });
        }
    }


    function point_log_alert(team) {
        const team_name = team.replace(':', '').trim();
        const teamData = teamsData.find(t => t.name === team_name);

        if (teamData) {
            const point_log = teamData.point_log.length > 0 ? teamData.point_log.map(log => `${log.point} 分 - ${log.reason} (${log.time})`).join('<br>') : '無';

            Swal.fire({
                title: `${team_name} 分數紀錄`,
                html: `${point_log}<canvas id="scoreChart" width="1000" height="500"></canvas>`,
                confirmButtonText: '關閉',
            });
        } else {
            Swal.fire({
                title: `錯誤`,
                html: `找不到隊伍: ${team_name}`,
                confirmButtonText: '關閉'
            });
        }
    }
});


async function showPointchart() {
    try {
        const response = await fetch('/api/teams');
        const teamsData = await response.json();
        const allTimes = Array.from(new Set(teamsData.flatMap(teamData => teamData.point_log.map(log => log.time)))).sort();
        const datasets = teamsData
        .filter(teamData => teamData.name !== 'admins')  // 跳過隊伍名為 'admins' 的數據
        .map((teamData, index) => {
            let cumulativeScore = 0;
            const data = allTimes.map(time => {
                const log = teamData.point_log.find(log => log.time === time);
                if (log) {
                    cumulativeScore += log.point;
                }
                return cumulativeScore;
            });
            return {
                label: teamData.name,
                data: data,
                borderColor: getColor(index,0.7),
                backgroundColor: getColor(index, 0.2),
                fill: false,
                tension: 0,  
                pointStyle: 'circle',
                pointRadius: 5,
                pointBackgroundColor: getColor(index),
            };
        });

        const maxTime = moment(allTimes[allTimes.length - 1]).add(1, 'hour').toISOString();
        const rangeMaxTime = moment(allTimes[0]).add(2 / 3 * (moment(maxTime).diff(moment(allTimes[0]))), 'milliseconds').toISOString();
        const minTime = moment(rangeMaxTime).subtract(1, 'hour').toISOString();
        const ctx = document.getElementById('scoreChart').getContext('2d');

        const scoreChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: allTimes,
                datasets: datasets
            },
            options: {
                scales: {
                    x: {
                        title: { display: true, text: '時間' ,font: { size: 28 ,weight: 'bold'} },
                        type: 'time',
                        time: {
                            unit: 'hour',
                            tooltipFormat:'HH:mm',
                            displayFormats: {
                                hour: 'HH:mm'
                            }
                        },
                        ticks: {
                            font: { size: 14 ,weight: 'bold'}
                        },
                        max: maxTime,
                        min: minTime,
                    },
                    y: {
                        title: { display: true, text: '分數' ,font: { size: 28 ,weight: 'bold'}},
                        ticks: {
                            font: { size: 14 ,weight: 'bold'}
                        },
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            font: { size: 28 ,weight: 'bold' }
                        }
                    },
                    tooltip: {
                        bodyFont: { size: 40 ,weight: 'bold'}
                    }
                },
                elements: {
                    line: {
                        borderWidth: 7
                    },
                    point: {
                        radius: 10,
                        hoverRadius: 12
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error fetching teams data:', error);
    }
}


function getColor(index, alpha = 1) {
    const colors = [
        'rgba(75, 192, 192, ALPHA)',
        'rgba(255, 99, 132, ALPHA)',
        'rgba(54, 162, 235, ALPHA)',
        'rgba(255, 206, 86, ALPHA)',
        'rgba(153, 102, 255, ALPHA)',
        'rgba(255, 159, 64, ALPHA)'
    ];
    return colors[index % colors.length].replace('ALPHA', alpha);
}