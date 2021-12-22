let lineAndPie = echarts.init(document.getElementById('lineAndPie'), null, {
    height: 700,
    width: 1248
});

let lineAndPie1 = echarts.init(document.getElementById('lineAndPie1'), null, {
    height: 700,
    width: 850
});

window.onload = function () {
    drawLineAndPie([]);
}

function drawLineAndPie(dataSet) {
    console.log(dataSet)
    if (dataSet == null || dataSet.length === 0) {
        return;
    }
    setTimeout(function () {
        let option = {
            legend: {},
            tooltip: {
                trigger: 'axis',
                showContent: false
            },
            dataset: {
                source: dataSet
                // ['product', '12-14', '12-15', '12-16', '12-17', '12-18', '12-19'],
                // ['lol', 56.5, 82.1, 88.7, 70.1, 53.4, 85.1],
                // ['Matcha Latte', 51.1, 51.4, 55.1, 53.3, 73.8, 68.7],
                // ['Cheese Cocoa', 40.1, 62.2, 69.5, 36.4, 45.2, 32.5],
                // ['Walnut Brownie', 25.2, 37.1, 41.2, 18, 33.9, 49.1]
            },
            xAxis: {type: 'category'},
            yAxis: {gridIndex: 0},
            grid: {top: '55%'},
            series: [
                // TODO: implement changing length of series
                // {
                //     type: 'line',
                //     smooth: true,
                //     seriesLayoutBy: 'row',
                //     emphasis: {focus: 'series'}
                // },
                // {
                //     type: 'line',
                //     smooth: true,
                //     seriesLayoutBy: 'row',
                //     emphasis: {focus: 'series'}
                // },
                {
                    type: 'line',
                    smooth: true,
                    seriesLayoutBy: 'row',
                    emphasis: {focus: 'series'}
                },
                {
                    type: 'line',
                    smooth: true,
                    seriesLayoutBy: 'row',
                    emphasis: {focus: 'series'}
                },
                {
                    type: 'line',
                    smooth: true,
                    seriesLayoutBy: 'row',
                    emphasis: {focus: 'series'}
                },
                {
                    type: 'line',
                    smooth: true,
                    seriesLayoutBy: 'row',
                    emphasis: {focus: 'series'}
                },
                {
                    type: 'line',
                    smooth: true,
                    seriesLayoutBy: 'row',
                    emphasis: {focus: 'series'}
                },
                {
                    type: 'line',
                    smooth: true,
                    seriesLayoutBy: 'row',
                    emphasis: {focus: 'series'}
                },
                {
                    type: 'line',
                    smooth: true,
                    seriesLayoutBy: 'row',
                    emphasis: {focus: 'series'}
                },
                {
                    type: 'line',
                    smooth: true,
                    seriesLayoutBy: 'row',
                    emphasis: {focus: 'series'}
                },
                {
                    type: 'pie',
                    id: 'pie',
                    radius: '30%',
                    center: ['50%', '25%'],
                    emphasis: {
                        focus: 'self'
                    },
                    label: {
                        formatter: '{b}: {@2012} ({d}%)'
                    },
                    encode: {
                        itemName: 'product',
                        value: dataSet[0][1],
                        tooltip: dataSet[0][1]
                    }
                }
            ]
        };
        lineAndPie.on('updateAxisPointer', function (event) {
            const xAxisInfo = event.axesInfo[0];
            if (xAxisInfo) {
                const dimension = xAxisInfo.value + 1;
                lineAndPie.setOption({
                    series: {
                        id: 'pie',
                        label: {
                            formatter: '{b}: {@[' + dimension + ']} ({d}%)'
                        },
                        encode: {
                            value: dimension,
                            tooltip: dimension
                        }
                    }
                });
            }
        });
        lineAndPie1.on('updateAxisPointer', function (event) {
            const xAxisInfo = event.axesInfo[0];
            if (xAxisInfo) {
                const dimension = xAxisInfo.value + 1;
                lineAndPie.setOption({
                    series: {
                        id: 'pie',
                        label: {
                            formatter: '{b}: {@[' + dimension + ']} ({d}%)'
                        },
                        encode: {
                            value: dimension,
                            tooltip: dimension
                        }
                    }
                });
            }
        });
        lineAndPie.setOption(option);
        lineAndPie1.setOption(option);
    });
}

let LinePieData;
$.ajax({
    url: domain + "/getDailyMeanViewerCount",
    type: 'GET',
    cache: false,
    processData: false,
    contentType: 'application/json',
    success: function (r) {
        console.log(r)
        LinePieData = JSON.parse(r);
        console.log(LinePieData);
        drawLineAndPie(LinePieData);
    }
})

