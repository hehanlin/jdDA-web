var echarts = require("echarts");
require('echarts-liquidfill');

module.exports = function(data) {
    var s_1_1 = echarts.init(document.getElementById("s-1-1"));
    s_1_1.setOption({
        title: {
            text: '官方好评比例图',
            subText: '三星以上为好评',
            left: 'center'
        },
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        toolbox: {
            show: true,
            feature: {
                dataView: {show: true, readOnly: false},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        legend: {
            bottom: 10,
            left: 'center',
            data: Object.keys(data.official_comment_rate)
        },
        series: {
            name: "评价比例",
            type: 'pie',
            radius: '60%',
            center: ['50%', '50%'],
            selectedMode: 'single',
            data: (function (data) {
                var tmp = [];
                for (var key in data.official_comment_rate) {
                    tmp.push({
                        value: data.official_comment_rate[key],
                        name: key,
                    })
                }
                return tmp;
            })(data),
            itemStyle: {
                emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    });

    var s_1_2 = echarts.init(document.getElementById("s-1-2"));
    s_1_2.setOption({
        title: {
            text: '不参与评价率（默认为好评）',
            left: 'center',
            textStyle: {
                color: '#f2c967',
                fontSize: 20
            }
        },
        toolbox: {
            show: true,
            feature: {
                dataView: {show: true, readOnly: false},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        series: [{
            type: 'liquidFill',
            data: [data.five_star_rate],
            radius: '60%'
        }]
    })

}