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
