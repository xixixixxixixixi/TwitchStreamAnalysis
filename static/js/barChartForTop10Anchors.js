var barChartForTop10Anchors = echarts.init(document.getElementById('barChartForTop10Anchors'), null, {
    height: 500,
    width: 850
});
var barChartForTop10Anchors1 = echarts.init(document.getElementById('barChartForTop10Anchors1'), null, {
    height: 500,
    width: 850
});

window.onload = function () {
    drawBarChartForTop10Anchors([]);
}

function covertToDatetimeFormat(dataSet) {
    if (dataSet == null || dataSet.length === 0) {
        return;
    }
    let length = dataSet.starttime.length;
    let minStartTime = new Date(dataSet.starttime[0]).getTime();
    for (let i = 0; i < length; i++) {
        let st = new Date(dataSet.starttime[i]).getTime();
        if (st < minStartTime) {
            minStartTime = st;
        }
    }
    for (let i = 0; i < length; i++) {
        dataSet.starttime[i] = new Date(dataSet.starttime[i]).getTime() - minStartTime;
        dataSet.endtime[i] = new Date(dataSet.endtime[i]).getTime() - minStartTime;
        dataSet.duration[i] = dataSet.endtime[i] - dataSet.starttime[i];
        // dataSet.starttime[i] = echarts.format.formatTime('yyyy-MM-dd hh:mm:ss', dataSet.starttime[i], false);
        // dataSet.duration[i] = echarts.format.formatTime('hh:mm:ss', dataSet.duration[i], false);
    }
    console.log(dataSet.starttime);
    console.log(dataSet.endtime);
    console.log(dataSet.duration);
    return minStartTime;
}

function drawBarChartForTop10Anchors(dataSet) {
    console.log(dataSet)
    let minStartTime = covertToDatetimeFormat(dataSet);

    let option = {
        title: {
            // text: 'Streaming Schedule for popular channels'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            },
            formatter: function (params) {
                var tar = params[1];
                // https://www.tutorialspoint.com/How-to-get-time-difference-between-two-timestamps-in-seconds
                let value = tar.value / 1000;
                let days = Math.floor(value / 86400);
                let hours = Math.floor(value / 3600) % 24;
                let minutes = Math.floor(value / 60) % 60;
                let seconds = tar.value % 60;
                return days + "days " + hours + "hours " + minutes + "minutes " +seconds + "seconds"
                // return tar.name + '<br/>' + tar.seriesName + ' : ' + tar.value;
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            axisLabel: {
                interval: 0,
                rotate: 15,
                textStyle: {fontSize: 12}
            },
            // splitLine: {show: false},
            data: dataSet.name
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
                name: 'Placeholder',
                type: 'bar',
                stack: 'Total',
                itemStyle: {
                    borderColor: 'transparent',
                    color: 'transparent'
                },
                emphasis: {
                    itemStyle: {
                        borderColor: 'transparent',
                        color: 'transparent'
                    }
                },
                data: dataSet.starttime
            },
            {
                name: 'Life Cost',
                type: 'bar',
                stack: 'Total',
                data: dataSet.duration
            }
        ]
    };
    barChartForTop10Anchors.setOption(option);
    barChartForTop10Anchors1.setOption(option);
}

var barDataSetForTop10Anchors;
$.ajax({
    url: domain + "/getChannelStreamSchedule/" + 10,
    type: 'GET',
    cache: false,
    processData: false,
    contentType: 'application/json',
    success: function (r) {
        console.log(r)
        barDataSetForTop10Anchors = JSON.parse(r);
        console.log(barDataSetForTop10Anchors);
        drawBarChartForTop10Anchors(barDataSetForTop10Anchors);
    }
})