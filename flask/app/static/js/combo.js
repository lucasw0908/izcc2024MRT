document.addEventListener('DOMContentLoaded', changeColor);

function changeColor() {
    const team = document.querySelector('#team').innerHTML;
    fetch(`http://localhost:8080/api/team/${team}`)
        .then(response => response.json())
        .then(data => {
            const items = document.querySelectorAll('.item');
            items.forEach(item => {
                const stationSpans = item.querySelector('.stations');
                const pointSpan = item.querySelector('.points');
                const stations = item.getAttribute('data-stations').split(',');
                const isInStations = stations.map(station => data.stations.includes(station.trim()));

                const colors = {
                    true: 'rgba(0, 128, 0, 0.5)', // 綠色
                    false: 'rgba(255, 0, 0, 0.5)' // 紅色
                };

                stationSpans.innerHTML = '';

                stations.forEach((station, index) => {
                    const span = document.createElement('span');
                    span.textContent = station;
                    span.style.color = colors[isInStations[index]]; // 根據狀態設置顏色
                    stationSpans.appendChild(span);
                    if (index < stations.length - 1) {
                        stationSpans.appendChild(document.createTextNode(', ')); // 添加逗號分隔
                    }
                });
            });
        })
        .catch(error => console.error('Error fetching data:', error));
}