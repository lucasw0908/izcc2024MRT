document.addEventListener('DOMContentLoaded', (event) => {
    if (location.href === "https://mrt.ckcsc.net"){
        const socket = io.connect("wss://mrt.ckcsc.net")
    }
    else{
    const socket = io.connect(location.href);
    }
    socket.emit('Connect', {message: "Connected from client"});

    socket.on('Connected', (data) => {
        // console.log(data["message"]);
    });


    socket.on('collapse_damage', (team_name) => {
        if(team_name === document.querySelector('#team').innerHTML){
            Swal.fire({
                title: '崩塌傷害',
                icon: 'warning',
                text: '你們受到了崩塌的傷害',
                confirmButtonText: '關閉'
            });
        }
    });

    socket.on('collapse_warning', () => {
        Swal.fire({
            title: '崩塌通知',
            icon: 'info',
            text: '5 分鐘後將崩塌 請注意你們的位置',
            confirmButtonText: '關閉'
        });
    });

});