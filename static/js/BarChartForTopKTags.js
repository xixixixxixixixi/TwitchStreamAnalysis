
var BarChartForTopKTags = echarts.init(document.getElementById('barChartForTopKTags'), null, {
    height: 500,
    width: 700
});

window.onload = function () {
    drawBarChartForTopKTags([]);
}

function drawBarChartForTopKTags(dataSet) {
    let option = {
        title: {
            left: 'left',
            text: 'Most Popular Tags'
        },
        dataset: [
            {
                dimensions: ['tag', 'count'],
                source: dataSet
            },
            {
                transform: {
                    type: 'sort',
                    config: {dimension: 'count', order: 'desc'}
                }
            }
        ],
        xAxis: {
            type: 'category',
            axisLabel: {
                interval: 0,
                rotate: 15,
                textStyle: {fontSize: 12}
            }
        },
        yAxis: {
            textStyle: {fontSize: 13}
        },
        series: {
            type: 'bar',
            encode: {x: 'name', y: 'score'},
            datasetIndex: 1,
            itemStyle: {color: '#3BA272'}
        }
    };
    BarChartForTopKTags.setOption(option);
}

// ajax for top K Tags
var barDataSetForTopKTags;
$.ajax({
    url: domain + "/topKTags/" + 10,
    type: 'GET',
    cache: false,
    processData: false,
    contentType: 'application/json',
    success: function (r) {
        barDataSetForTopKGames = JSON.parse(r);
        drawBarChartForTopKTags(barDataSetForTopKGames);
    }
})

