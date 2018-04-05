var echarts = require("echarts");
require('echarts-liquidfill');

module.exports = function (data) {
    var s_6_1 = echarts.init(document.getElementById("s-6-1"));
    s_6_1.setOption({
        title: {
            text: "用户购买渠道分析图",
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
                magicType: {show: true, type: ['line', 'bar']},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        legend: {
            bottom: 10,
            left: 'center',
            data: Object.keys(data.buy_channel)
        },
        series: {
            name: "购买渠道",
            type: 'pie',
            radius: '60%',
            center: ['50%', '50%'],
            selectedMode: 'single',
            data: (function (data) {
                var tmp = [];
                for (var key in data.buy_channel) {
                    tmp.push({
                        value: data.buy_channel[key],
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

    var s_6_2 = echarts.init(document.getElementById("s-6-2"));
    s_6_2.setOption({
        title: {
            text: "移动端占比图",
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
            data: Object.keys(data.buy_channel)
        },
        series: {
            name: "购买渠道",
            type: 'pie',
            radius: '60%',
            center: ['50%', '50%'],
            selectedMode: 'single',
            data: (function (data) {
                var tmp = [];
                for (var key in data.is_mobile) {
                    tmp.push({
                        value: data.is_mobile[key],
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
}