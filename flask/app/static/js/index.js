// ready
document.addEventListener("DOMContentLoaded", () => {
    resizeMap();
    showMap();
    showCollapse_time();
    showPoint();
    showLocate();
    showImprisoned();
    getCurrentLocation();
});


// repeat
setInterval(showMap, 10000);
setInterval(showCollapse_time, 10000);
setInterval(showPoint, 10000);
setInterval(showLocate, 10000);
setInterval(showImprisoned, 10000);

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
}
window.addEventListener('resize', resizeMap);
window.addEventListener('load', resizeMap);


function checkImageExists(imageUrl) {
    return fetch(imageUrl, { method: 'HEAD' })
        .then(response => response.ok)
        .catch(() => false);
}
function station_info(station_name) {
    const team = document.querySelector('#team').innerHTML;
    station_name = station_name.replace("/", "_")
    Promise.all([
        fetch(`http://localhost:8080/api/station/${station_name}`).then(response => response.json()),
        fetch(`http://localhost:8080/api/team/${team}`).then(response => response.json())
    ])
        .then(([data, team_data]) => {
            let imageUrl = `../static/img/stations/${station_name}.jpg`;
            checkImageExists(imageUrl).then(exists => {
                let imageHtml = exists ? `<img src="${imageUrl}" alt="${station_name} 圖片" style="width:60%; height:auto;">` : '';
                let lebel_image = (data.is_special === false || station_name === team_data.location) ? imageHtml : "";
                let lebel_is_special = (data.is_special) ? "是" : "否";
                let label_team = (data.team) ? data.team : "無人佔領";
                let label_depiction = (data.is_special === false || station_name === team_data.location) ? data.mission : "隱藏";
                let label_exit = (data.is_special === false || station_name === team_data.location) ? data.exit : "隱藏";
                let lebel_difficult = null;
                if (data.difficult == 1) { lebel_difficult = "簡單"; }
                else if (data.difficult == 2) { lebel_difficult = "普通"; }
                else if (data.difficult == 3) { lebel_difficult = "困難"; }
                station_name = station_name.replace("_", "/")

                Swal.fire({
                    title: `${station_name} 站點資訊`,
                    html: `
                        <p>特殊站 : ${lebel_is_special}</p>
                        <p>佔領的小隊 : ${label_team}</p>
                        <p>任務敘述 : ${label_depiction}</p>
                        <p>任務出口 : ${label_exit}</p>
                        <p>任務難度: ${lebel_difficult}</p>
                        ${lebel_image}
                    `,
                    confirmButtonText: "關閉",
                    showCancelButton: true,
                    cancelButtonText: "提示",
                    customClass: { cancelButton: 'swal-button-yellow' },
                }).then((result) => {
                    if (result.dismiss === Swal.DismissReason.cancel) {
                        Swal.fire({
                            title: '提示',
                            text: `${data.tips}`,
                            confirmButtonText: "關閉",
                        });
                    }
                });
            });
        })
}


const chineseNumerals = { '零': 0, '一': 1, '二': 2, '三': 3, '四': 4, };
function showLocate() {
    fetch('http://localhost:8080/api/teams')
        .then(response => response.json())
        .then(data => {
            data.forEach(team => {
                // 提取隊名中的數字部分，例如 "零小" -> "0"
                const chineseNumeral = team.name.charAt(0); // 假設隊名的第一個字符是中文數字
                const teamNumber = chineseNumerals[chineseNumeral];

                if (teamNumber !== undefined) {
                    const locationElement = document.getElementById(`team${teamNumber}_location`);
                    if (locationElement) {
                        locationElement.textContent = `${team.location}`;
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching data:', error));
}

function showPoint() {
    fetch('http://localhost:8080/api/teams')
        .then(response => response.json())
        .then(data => {
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
        })
        .catch(error => console.error('Error fetching data:', error));
}


let lastStatus = null;
let lastWarning = null;
function showMap() {
    fetch('http://localhost:8080/api/collapse_status')
        .then(response => response.json())
        .then(data => {
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
                    }
                } else {
                    if (data.status === 0) {
                        document.getElementById('Map1').style.display = 'block';
                    } else if (data.status === 1) {
                        document.getElementById('Map3').style.display = 'block';
                    }
                }
            }
        })
        .catch(error => console.error('Error fetching data:', error));
}


function showCollapse_time() {
    fetch('http://localhost:8080/api/next_collapse_time')
        .then(response => response.json())
        .then(data => {
            document.getElementById('next_collapse_time_label').textContent = `下次崩塌時間 : ${data}`;
        })
        .catch(error => console.error('Error fetching data:', error));
}


function showImprisoned() {
    const team = document.querySelector('#team').innerHTML;
    fetch(`http://localhost:8080/api/team/${team}`)
        .then(response => response.json())
        .then(data => {
            if (data.is_imprisoned) {
                document.getElementById('is_imprisoned_label').textContent = `監獄剩餘時間 : ${data.imprisoned_time} 分鐘`;
            }
        })
        .catch(error => console.error('Error fetching data:', error));
}


function getCurrentLocation() {
    const team = document.querySelector('#team').innerHTML;
    // 先確認使用者裝置能不能抓地點
    if (navigator.geolocation) {

        // 使用者不提供權限，或是發生其它錯誤
        function error() {
            alert('無法取得你的位置');
        }

        // 使用者允許抓目前位置，回傳經緯度
        function success(position) {
            fetch(`http://localhost:8080/api/gps_location/${team}/${position.coords.latitude}/${position.coords.longitude}`)
        }

        // 跟使用者拿所在位置的權限
        navigator.geolocation.getCurrentPosition(success, error);

    } else {
        alert('Sorry, 你的裝置不支援地理位置功能。')
    }
}