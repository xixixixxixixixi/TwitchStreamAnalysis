
let pieChart = echarts.init(document.getElementById('pieChart'), null, {
    height: 450,
    width: 1248
});

let pieChart1 = echarts.init(document.getElementById('pieChart1'), null, {
    height: 450,
    width: 850
});

window.onload = function () {
    drawPieChart([]);
}

function drawPieChart(dataSet) {
    let option = {
        title: {
            left: 90,
            // text: 'Most Popular Live Rooms in Different Language'
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
    pieChart1.setOption(option);
}

// ajax for pie chart
let pieDataSet;
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