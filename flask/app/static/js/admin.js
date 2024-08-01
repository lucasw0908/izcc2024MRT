function add_point() {
    const team = document.getElementById("add_point_team_name").value;
    const points = document.getElementById("add_points").value;

    if (team === "" || points === "") {
        alert("請填入隊伍名稱和分數");
        return;
    }

    fetch(`/api/add_point/${team}/${points}`)
        .then(response => response.text())
        .then(response => { alert(response); });
}

function set_point() {
    const team = document.getElementById("set_point_team-name").value;
    const points = document.getElementById("set_points").value;

    if (team === "" || points === "") {
        alert("請填入隊伍名稱和分數");
        return;
    }

    fetch(`/api/set_point/${team}/${points}`)
        .then(response => response.text())
        .then(response => { alert(response); });
}

function finish_misson() {
    const team = document.getElementById("finish_misson_team-name").value;

    if (team === "") {
        alert("請填入隊伍名稱");
        return;
    }

    fetch(`/api/admin/finish_mission/${team}`)
        .then(response => response.text())
        .then(response => { alert(response); });
}

function create_team() {
    const team = document.getElementById("create_team_team-name").value;
    const position = document.getElementById("create_team_team-position").value;

    if (team === "" || position === "") {
        alert("請填入隊伍名稱和位置");
        return;
    }

    fetch(`/api/admin/create_team/${team}/${position}`)
        .then(response => response.text())
        .then(response => { alert(response); });
}

function delete_team() {
    const team = document.getElementById("delete_team_team-name").value;

    if (team === "") {
        alert("請填入隊伍名稱");
        return;
    }

    fetch(`/api/admin/delete_team/${team}`)
        .then(response => response.text())
        .then(response => { alert(response); });
}

function join_team() {
    const team = document.getElementById("join_team_team-name").value;
    const player_name = document.getElementById("join_team_user-name").value;
    const admin = document.getElementById("join_team_team-admin").checked;

    if (team === "" || player_name === "") {
        alert("請填入隊伍名稱和玩家名稱");
        return;
    }

    if (admin) {
        fetch(`/api/admin/join_team/${team}/${player_name}`)
        .then(response => response.text())
        .then(response => { alert(response); });
    }
    else {
        fetch(`/api/join_team/${team}/${player_name}`)
        .then(response => response.text())
        .then(response => { alert(response); });
    }
}

function leave_team() {
    const player_name = document.getElementById("leave_team_user-name").value;

    if (player_name === "") {
        alert("請填入玩家名稱");
        return;
    }

    fetch(`/api/leave_team/${player_name}`)
        .then(response => response.text())
        .then(response => { alert(response); });
}

function set_location() {
    const team = document.getElementById("move_team_team-name").value;
    const location = document.getElementById("move_location").value;

    if (team === "" || location === "") {
        alert("請填入隊伍名稱和位置");
        return;
    }
    
    fetch(`/api/admin/set_location/${team}/${location}`)
        .then(response => response.text())
        .then(response => { alert(response); });
}

function release_team() {
    const team = document.getElementById("release_team-name").value;

    if (team === "") {
        alert("請填入隊伍名稱");
        return
    }

    fetch(`/api/admin/release_team/${team}`)
        .then(response => response.text())
        .then(response => { alert(response); });
}

function reset_team() {
    const team = document.getElementById("reset_team").value;
    
    fetch(`/api/admin/reset_team/${team}`)
        .then(response => response.text())
        .then(response => { alert(response); });
}