var echarts = require("echarts");
module.exports = function(data) {
    var s2 = echarts.init(document.getElementById("section2"));
    s2.setOption({
        title: {
            text: '星级分布图',
            subText: '最近一千条评论',
            left: 'center',
            textStyle: {
                color: '#3398DB',
                fontSize: 20
            }
        },
        color: ['#3398DB'],
        tooltip: {
            trigger: 'axis',
            axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            }
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
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: [
            {
                type: 'category',
                data: Object.keys(data.histogram_score),
                axisTick: {
                    alignWithLabel: true
                }
            }
        ],
        yAxis: [
            {
                type: 'value'
            }
        ],
        series: [
            {
                name: '评论个数',
                type: 'bar',
                barWidth: '60%',
                data: Object.values(data.histogram_score)
            }
        ]
    });
}