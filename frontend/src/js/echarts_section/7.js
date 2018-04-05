var echarts = require("echarts");

module.exports = function (data) {
    var s7 = echarts.init(document.getElementById("section7"));
    if (data.buy_province.length > 1) {
        require("echarts/map/js/china");
        s7.setOption({
            title: {
                text: '各省份销量',
                left: 'center'
            },
            tooltip: {
                trigger: 'item'
            },
            legend: {
                orient: 'vertical',
                left: 'left',
                data: ['销量']
            },
            visualMap: {
                min: 0,
                max: 2500,
                left: 'left',
                top: 'bottom',
                text: ['高', '低'],           // 文本，默认为数值文本
                calculable: true
            },
            toolbox: {
                show: true,
                orient: 'vertical',
                left: 'right',
                top: 'center',
                feature: {
                    dataView: {readOnly: false},
                    restore: {},
                    saveAsImage: {}
                }
            },
            series: [
                {
                    name: '销量',
                    type: 'map',
                    mapType: 'china',
                    label: {
                        normal: {
                            show: true
                        },
                        emphasis: {
                            show: true
                        }
                    },
                    data: (function (data) {
                        var tmp = [];
                        for (var key in data.buy_province) {
                            tmp.push({
                                value: data.buy_province[key],
                                name: key
                            })
                        }
                        return tmp;
                    })(data)
                }
            ]
        });
    } else {
        s7.setOption({
            title: {
                text: '各省份销量占比',
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
                data: Object.keys(data.buy_province)
            },
            series: {
                name: "销量",
                type: 'pie',
                radius: '60%',
                center: ['50%', '50%'],
                selectedMode: 'single',
                data: (function (data) {
                    var tmp = [];
                    for (var key in data.buy_province) {
                        tmp.push({
                            value: data.buy_province[key],
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

}