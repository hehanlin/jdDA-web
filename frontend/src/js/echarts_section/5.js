var echarts = require("echarts");

module.exports = function(data) {
    //购买属性分析
    var s5 = echarts.init(document.getElementById("section5"));
    s5.setOption({
        title: {
            text: "用户购买属性分析图",
            subtitle: "颜色，材质等"
        },
        tooltip: {
            trigger: 'axis'
        },
        toolbox: {
            show: true,
            feature: {
                dataView: {show: true, readOnly: false},
                magicType: {show: true, type: ['line', 'bar']},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        xAxis: [
            {
                type: 'category',
                data: Object.keys(data.buy_color)
            },
        ],
        yAxis: [
            {
                type: 'value'
            }
        ],
        series: [
            {
                name: '配置',
                type: 'bar',
                data: Object.values(data.buy_color),
            }
        ]
    })
}