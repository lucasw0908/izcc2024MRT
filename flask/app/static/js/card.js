document.addEventListener('DOMContentLoaded', function () {
    var elementCard = document.querySelector('.element-card');
    var arrow = document.querySelector('.arrow');
    var startY, endY;

    function getCardName() {
        const team = document.querySelector('#team').innerHTML;
        return fetch(`/api/team/${team}`)
            .then(response => response.json())
            .then(data => {
                return data.current_card;
            });
    }

    getCardName().then(card => {
        if (card === null) {
            document.body.classList.add('modal-open');
            Swal.fire({
                title: `沒有卡片可以抽`,
                icon: 'warning',
                text: "You don't have card.",
                confirmButtonText: "關閉",
                didClose: () => {
                    document.body.classList.remove('modal-open');
                    window.location.href = '/team_admin';
                }
            });
        } else {
            document.getElementById("front-facing").style.backgroundImage = `url('../static/img/cards/${card}.jpg')`;
        }
    });

    document.addEventListener('touchstart', function (e) {
        startY = e.touches[0].clientY;
    });

    document.addEventListener('touchend', function (e) {
        endY = e.changedTouches[0].clientY;
        if (startY - endY > 50) { // 檢查滑動距離是否大於50px
            elementCard.classList.add('show');
            arrow.style.display = 'none'; // 隱藏箭頭
        }
    });

    elementCard.addEventListener('click', function () {
        elementCard.classList.toggle('stopped');
        if (elementCard.classList.contains('stopped')) {
            elementCard.style.transform = 'rotateY(0deg)'; // 停止在正面
        }
    });
});