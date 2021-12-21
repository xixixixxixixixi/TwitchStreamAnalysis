let barDynamicHistory = echarts.init(document.getElementById('barDynamicHistory'), null, {
    height: 500,
    width: 700
});

window.onload = function () {
    drawBarDynamicHistory([]);
}

function drawBarDynamicHistory(dataSet) {
    if (dataSet == null || dataSet.length === 0) {
        return;
    }
    const dataToShow = [];
    // const data2 = dataSet.data;
    let viewerCount = dataSet["viewerCount"];
    let label = dataSet["gameLabel"];
    for (let i = 0; i < viewerCount.length; ++i) {
        dataToShow.push(100);
    }
    let option = {
        // title: {
        //     text: 'Recent Growing Trend of Most Popular Games'
        // },
        title: {
            left: 'left',
            text: 'Recent History Trend of Popular game viewer count'
        },
        xAxis: {
            max: 'dataMax'
        },
        yAxis: {
            type: 'category',
            data: label,
            inverse: true,
            animationDuration: 300,
            animationDurationUpdate: 300,
            max: 9 // only the largest 3 bars will be displayed
        },
        series: [
            {
                realtimeSort: true,
                name: 'Viewer Count',
                type: 'bar',
                data: dataToShow,
                label: {
                    show: true,
                    position: 'right',
                    valueAnimation: true
                }
            }
        ],
        legend: {
            show: true
        },
        animationDuration: 0,
        animationDurationUpdate: 3000,
        animationEasing: 'linear',
        animationEasingUpdate: 'linear'
    };

    function run() {
        for (var i = 0; i < viewerCount.length; ++i) {
            for (var j = 0; j < 5; ++j) {
                dataToShow[i] = viewerCount[i][j];
                barDynamicHistory.setOption(option);
            }

        }
    }

    setInterval(function () {
        run();
    }, 3000);
}


let dataSetForHistoryDynamicChart;
$.ajax({
    url: domain + "/getDynamicPopularGamesBarChart",
    type: 'POST',
    data: JSON.stringify(['Chatting', 'GrandTheftAutoV', 'LeagueofLegends',
        'ApexLegends', 'Valorant', 'CallofDuty', 'Fortnite',
        'TeamfightTactics', 'Minecraft', 'Pokemon']),
    cache: false,
    processData: false,
    contentType: 'application/json',
    success: function (r) {
        console.log(r)
        dataSetForHistoryDynamicChart = JSON.parse(r);
        console.log(dataSetForHistoryDynamicChart);
        drawBarDynamicHistory(dataSetForHistoryDynamicChart);
    }
})