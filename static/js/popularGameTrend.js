// let dataForTopKGames;
// $.ajax({
//     url: domain + "/topKGames/" + 10,
//     type: 'GET',
//     cache: false,
//     processData: false,
//     contentType: 'application/json',
//     success: function (r) {
//         dataForTopKGames = JSON.parse(r);
//         console.log(dataForTopKGames);
//         gameTrendInformationInjection(dataForTopKGames);
//     }
// })
let LineChartForGameTrend = echarts.init(document.getElementById('lineChartForGameTrend'), null, {
    height: 500,
    width: 700
});

window.onload = function () {
    drawLineChartForGameTrend([]);
}

function drawLineChartForGameTrend(dataSet) {
    option = {
        title: {
            text: 'Stacked Line'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: dataset.label
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: dataset.time
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                formatter: function (value) {
                    return echarts.format.formatTime('yyyy-MM-dd hh:mm:ss', value + minStartTime);
                }
            }
        },
        series: [
            {
                name: 'True',
                type: 'line',
                stack: 'Total',
                data: dataset.true
            },
            {
                name: 'Prediction',
                type: 'line',
                stack: 'Total',
                data: dataset.predict
            }
        ]
    };
    LineChartForGameTrend.setOption(option);
}

// TODO: implement Custome Game Name
window.onload = function () {
    gameTrendInformationInjection();
}

function gameTrendInformationInjection() {
    let gameName = [
        "Chatting",
        "GrandTheftAutoV",
        "LeagueofLegends",
        "ApexLegends",
        "Valorant",
        "CallofDuty",
        "Fortnite",
        "TeamfightTactics",
        "Minecraft",
        "Pokemon",
        "Total",
    ];
    let gameListString = "";
    for (let i = 0; i < gameName.length; i++) {
        gameListString += "<option value=\"" + gameName[i] + "\">" + gameName[i] + "</option>";
    }
    document.getElementById("popularGameTrendSelection").innerHTML =
        "<select id=\"gameList\">" + gameListString + "</select>";
    document.getElementById("popularGameTrendSelection").innerHTML +=
        "<button id=\"gameList\" " +
        "onClick=\"submitRequestForGameTrend()\">change channel</button>";
}


let lineDataSetForPopularGameTrend;

function submitRequestForGameTrend() {
    $.ajax({
        url: domain + "/getViewerPrediction",
        type: 'POST',
        cache: false,
        data: JSON.stringify($('#gameList').val()),
        processData: false,
        contentType: 'application/json',
        success: function (r) {
            console.log(r)
            lineDataSetForPopularGameTrend = JSON.parse(r);
            console.log(lineDataSetForPopularGameTrend);
            drawLineChartForGameTrend(lineDataSetForPopularGameTrend);
        }
    })
}

setInterval(function () {
    console.log($('#gameList').val())
}, 1000)