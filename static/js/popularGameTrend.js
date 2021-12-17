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
    width: 2000
});

window.onload = function () {
    drawLineChartForGameTrend([]);
}


function drawLineChartForGameTrend(dataSet) {
    // let minStartTime = covertToDatetimeFormat(dataSet);
    option = {
        title: {
            text: 'Stacked Line'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: dataSet.label
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
            data: dataSet.time
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                name: 'True',
                type: 'line',
                stack: 'Total',
                data: dataSet.true
            },
            {
                name: 'Prediction',
                type: 'line',
                stack: 'Total',
                data: dataSet.pred
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
        data: $('#gameList').val(),
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

//
// setInterval(function () {
//     console.log($('#gameList').val())
// }, 1000)