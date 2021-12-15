// var domain = "https://proj6893.herokuapp.com";
var domain = "http://127.0.0.1:5000";
var pieChart = echarts.init(document.getElementById('pieChart'), null, {
    height: 450,
    width: 700
});

window.onload = function () {
    drawPieChart([]);
}

function drawPieChart(dataSet) {
    let option = {
        title: {
            left: 90,
            text: 'Most Popular Live Rooms in Different Language'
        },
        legend: {
            right: 'left',
            orient: 'vertical',
            top: 'center',
            icon: 'square',
            textStyle: {
                fontSize: '12',
            },
        },
        label: {
            show: true,
            position: 'top',
            fontSize: 13,
        },
        icon: 'rect',
        series: [
            {
                name: 'Pie Chart',
                type: 'pie',
                radius: '70%',
                center: ['50%', '50%'],
                // roseType: 'angle',
                data: dataSet,
            }
        ]
    };
    pieChart.setOption(option);
}

// ajax for pie chart
var pieDataSet;
$.ajax({
    url: domain + "/getLanguageCount/" + 500,
    type: 'GET',
    cache: false,
    processData: false,
    contentType: 'application/json',
    success: function (r) {
        console.log(r)
        pieDataSet = JSON.parse(r);
        console.log(pieDataSet);
        drawPieChart(pieDataSet);
    }
})