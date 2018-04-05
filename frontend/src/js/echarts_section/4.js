var echarts = require("echarts");

module.exports = function (data) {
    //购买配置分析
    var s4 = echarts.init(document.getElementById("section4"));
    s4.setOption({
        title: {
            text: '用户购买配置分析图',
            subtext: '如大小，尺码等'
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
        calculable: true,
        xAxis: [
            {
                type: 'category',
                data: Object.keys(data.buy_size)
            },
        ],
        yAxis: [
            {
                type: 'value'
            }
        ],
        series: [
            {
                name: '属性',
                type: 'bar',
                data: Object.values(data.buy_size),
                markPoint: {
                    data: [
                        {type: 'max', name: '最大值'},
                        {type: 'min', name: '最小值'}
                    ]
                }
            }
        ]
    })
}