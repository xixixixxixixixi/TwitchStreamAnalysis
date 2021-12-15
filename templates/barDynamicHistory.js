var barDynamicHistory = echarts.init(document.getElementById('barDynamicHistory'), null, {
    height: 500,
    width: 700
});

window.onload = function () {
    drawBarDynamicHistory([]);
}

var dataSetForHistoryDynamicChart;
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