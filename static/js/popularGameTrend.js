






var lineDataSetForPopularGameTrend;
$.ajax({
    url: domain + "/getViewerPrediction",
    type: 'GET',
    cache: false,
    processData: false,
    contentType: 'application/json',
    success: function (r) {
        console.log(r)
        lineDataSetForPopularGameTrend = JSON.parse(r);
        console.log(lineDataSetForPopularGameTrend);
        drawBarChartForTop10Anchors(lineDataSetForPopularGameTrend);
        gameTrendInformationInjection(lineDataSetForPopularGameTrend);
    }
})

function gameTrendInformationInjection(popularChannelData) {

}