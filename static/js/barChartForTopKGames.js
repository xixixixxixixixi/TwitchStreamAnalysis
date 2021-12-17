
let BarChartForTopKGames = echarts.init(document.getElementById('barChartForTopKGames'), null, {
    height: 500,
    width: 700
});

window.onload = function () {
    drawBarChartForTopKGames([]);
}

function drawBarChartForTopKGames(dataSet) {
    let option = {
        title: {
            left: 'left',
            text: 'TOP 10 Popular Live Games'
        },
        dataset: [
            {
                dimensions: ['game', 'viewer'],
                source: dataSet
            },
            {
                transform: {
                    type: 'sort',
                    config: {dimension: 'viewer', order: 'desc'}
                }
            }
        ],
        xAxis: {
            type: 'category',
            axisLabel: {
                interval: 0,
                rotate: 15,
                textStyle: {fontSize: 11}
            }
        },
        yAxis: {
            textStyle: {fontSize: 12}
        },
        series: {
            type: 'bar',
            encode: {x: 'name', y: 'score'},
            datasetIndex: 1
        }
    };
    BarChartForTopKGames.setOption(option);
}

let barDataSetForTopKGames;
$.ajax({
    url: domain + "/topKGames/" + 10,
    type: 'GET',
    cache: false,
    processData: false,
    contentType: 'application/json',
    success: function (r) {
        barDataSetForTopKGames = JSON.parse(r);
        drawBarChartForTopKGames(barDataSetForTopKGames);
    }
})