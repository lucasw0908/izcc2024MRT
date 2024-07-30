function add_point() {
    const team = document.getElementById('add_point_team_name').value;
    const points = document.getElementById('add_points').value;
    fetch(`/api/add_point/${team}/${points}`)
        .then(response => response.text())
        .then(response => { alert(response); });
}

function set_point() {
    const team = document.getElementById('set_point_team-name').value;
    const points = document.getElementById('set_points').value;
    fetch(`/api/set_point/${team}/${points}`)
        .then(response => response.text())
        .then(response => { alert(response); });
}

function finish_misson() {
    const team = document.getElementById('finish_misson_team-name').value;
    fetch(`/api/finish_mission/${team}`)
        .then(response => response.text())
        .then(response => { alert(response); });
}

function create_team() {
    const team = document.getElementById('create_team_team-name').value;
    const position = document.getElementById('create_team_team-position').value;
    fetch(`/api/create_team/${team}/${position}`)
        .then(response => response.text())
        .then(response => { alert(response); });
}

function delete_team() {
    const team = document.getElementById('delete_team_team-name').value;
    fetch(`/api/delete_team/${team}`)
        .then(response => response.text())
        .then(response => { alert(response); });
}

function join_team() {
    const team = document.getElementById('join_team_team-name').value;
    const player_name = document.getElementById('join_team_user-name').value;
    const admin = document.getElementById('join_team_team-admin').checked;
    fetch(`/api/join_team/${team}/${player_name}/${admin}`)
        .then(response => response.text())
        .then(response => { alert(response); });
}

function leave_team() {
    const player_name = document.getElementById("leave_team_user-name").value;
    fetch(`/api/leave_team/${player_name}`)
        .then(response => response.text())
        .then(response => { alert(response); });
}

function move_to_location() {
    const team = document.getElementById('move_team_team-name').value;
    const location = document.getElementById('move_location').value;
    fetch(`/api/move_to_location/${team}/${location}`)
        .then(response => response.text())
        .then(response => { alert(response); });
}