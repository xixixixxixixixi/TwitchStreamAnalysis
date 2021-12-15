var domain = "http://127.0.0.1:5000";
var BarChartForTopKTags = echarts.init(document.getElementById('barChartForTopKTags'), null, {
    height: 500,
    width: 700
});
window.onload = function () {
    drawBarChartForTopKTags([]);
}

