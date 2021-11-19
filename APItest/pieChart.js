var myChart = echarts.init(document.getElementById('main'), null, {
  width: 4000,
  height: 1000
});
window.onload = function () {
  drawBarChart([]);
}
function drawBarChart(dataSet) {
  var option = {
    title: {
      text: 'Referer of a Website',
      subtext: 'Fake Data',
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
        {
          name: 'Access From',
          type: 'pie',
          radius: '50%',
          data: [
            { value: 1048, name: 'Search Engine' },
            { value: 735, name: 'Direct' },
            { value: 580, name: 'Email' },
            { value: 484, name: 'Union Ads' },
            { value: 300, name: 'Video Ads' }
          ],
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
        ]
  };
  myChart.setOption(option);
}
var dataSet;
$.ajax({
  url:"http://127.0.0.1:5000/getLanguageCount/" + 500,
  type: 'GET',
  headers:{'Content-type' : 'application/json'},
  cache: false,
  dataType : 'html',
  processData : false,
  contentType : 'application/json',
  success: function (r){
    console.log(r)
    dataSet = JSON.parse(r);
    drawBarChart(dataSet);
  }
})