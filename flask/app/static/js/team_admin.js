//ready
document.addEventListener("DOMContentLoaded", () => {
    mission_label();
    getCurrentLocation();
});

function mission_label() {
    const team = document.querySelector('#team').innerHTML;
    fetch(`http://localhost:8080/api/team/${team}`)
        .then(response => response.json())
        .then(data => {
            now_status = data.current_mission_finished
            if (now_status) {
                document.getElementById('mission_label').textContent = "目前狀態 : 任務已完成 請按骰子";
            }
            else {
                document.getElementById('mission_label').textContent = "目前狀態 : 任務進行中 請按任務完成";
            }
        })
}


function finish_misson() {
    const team = document.querySelector('#team').innerHTML;
    fetch(`http://localhost:8080/api/finish_mission/${team}`).then(response => response.text())
        .then(response => {
            if (response === "Mission finished.") {
                Swal.fire({
                    title: '任務完成',
                    icon: "success",
                    text: response,
                    confirmButtonText: 'OK',
                    willClose: () => {
                        mission_label();
                    }
                });
            }
            else if (response === "Mission already finished.") {
                Swal.fire({
                    title: '已完成任務',
                    icon: "warning",
                    text: response,
                    confirmButtonText: 'OK'
                });
            }
            else if (response === "Location not reached") {
                Swal.fire({
                    title: '還沒抵達',
                    icon: "warning",
                    text: response,
                    confirmButtonText: 'OK'
                });
            }
            else if (response === "Team is imprisoned") {
                Swal.fire({
                    title: '監獄時間',
                    icon: "warning",
                    text: response,
                    confirmButtonText: 'OK'
                });
            }
            else if (response === "Location not reached.") {
                Swal.fire({
                    title: '未達目的地',
                    icon: "warning",
                    text: response,
                    confirmButtonText: 'OK'
                });
            }
            else if (response.includes('card')) {
                Swal.fire({
                    title: '抽卡時間',
                    icon: "info",
                    text: "Card time!",
                    confirmButtonText: '前往',
                    willClose: () => {
                        window.location.href = '/card';
                    }
                });
            }
            else {
                Swal.fire({
                    title: '錯誤',
                    icon: "error",
                    text: response,
                    confirmButtonText: 'Close'
                });
            }
        })
}


function missionAPI() {
    const team = document.querySelector('#team').innerHTML;
    fetch(`http://localhost:8080/api/team/${team}`)
        .then(response => response.json())
        .then(data => {
            if (data.current_mission_finished) {
                window.location.href = '/dice';
            }
            else {
                Swal.fire({
                    title: '請先完成任務',
                    icon: "warning",
                    text: "Please finish mission first.",
                    confirmButtonText: 'Close'
                });
            }
        })
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