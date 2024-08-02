//ready
document.addEventListener("DOMContentLoaded", () => {
    mission_label();
    showDistance();
});

function mission_label() {
    const team = document.querySelector("#team").innerHTML;
    fetch(`/api/team/${team}`)
        .then(response => response.json())
        .then(data => {
            now_status = data.current_mission_finished
            if (now_status) {
                document.getElementById("mission_label").textContent = "目前狀態 : 沒有進行中的任務 請按骰子";
            }
            else {
                document.getElementById("mission_label").textContent = "目前狀態 : 任務進行中 請按任務完成";
            }
        })
}

async function finish_mission() {
    const team = document.querySelector("#team").innerHTML;
    try {
        const response = await fetch(`/api/finish_mission/${team}`);
        const responseText = await response.text();

        if (responseText === "Success" || responseText === "成功") {
            await Swal.fire({
                title: "任務完成",
                icon: "success",
                confirmButtonText: "OK",
                willClose: () => {
                    mission_label();
                }
            });
        } else if (responseText.includes("card")) {
            const result = await Swal.fire({
                title: "抽卡時間",
                icon: "info",
                text: "Card time!",
                showConfirmButton: true,
                confirmButtonText: "關閉",
                showCancelButton: true,
                cancelButtonText: "前往",
                customClass: { cancelButton: 'swal-button-yellow' }
            });

            // Handle the result of the Swal.fire
            if (result.isDismissed && result.dismiss === Swal.DismissReason.cancel) {
                window.location.href = "/card";
            }
        } else {
            await Swal.fire({
                title: responseText,
                icon: "warning",
                confirmButtonText: "OK"
            });
        }
    } catch (error) {
        console.error('Error finishing mission:', error);
        await Swal.fire({
            title: "錯誤",
            text: "無法完成任務，請稍後再試。",
            icon: "error",
            confirmButtonText: "OK"
        });
    }
}


function skip_mission() {
    const team = document.querySelector("#team").innerHTML;
    fetch(`/api/skip_mission/${team}`).then(response => response.text())
        .then(response => {
            if (response === "Success" || response === "成功") {
                Swal.fire({
                    title: "成功放棄",
                    icon: "success",
                    confirmButtonText: "OK",
                    willClose: () => {
                        mission_label();
                    }
                });
            }
            else {
                Swal.fire({
                    title: response,
                    icon: "warning",
                    confirmButtonText: "OK"
                });
            }
        })
}

function missionAPI() {
    const team = document.querySelector("#team").innerHTML;
    fetch(`/api/team/${team}`)
        .then(response => response.json())
        .then(data => {
            if (data.current_mission_finished) {
                window.location.href = "/dice";
            }
            else {
                Swal.fire({
                    title: "請先完成任務",
                    icon: "warning",
                    text: "Please finish mission first.",
                    confirmButtonText: "Close"
                });
            }
        })
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
                document.getElementById('distance_label').textContent = `目前位置 : 你們已到${data.target_location}站 `;
            } else {
                document.getElementById('distance_label').textContent = `目前位置 : 你們距離${data.target_location}站 ${distanceInKm} km `;
            }
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
