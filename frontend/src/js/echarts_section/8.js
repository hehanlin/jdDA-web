var echarts = require("echarts");

module.exports = function(data) {
    var s8 = echarts.init(document.getElementById("section8"));
    s8.setOption({
        "title": {
            "text": "销量与评论月份分布图",
            x: "4%",

            textStyle: {
                color: '#fff',
                fontSize: '22'
            }
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "shadow",
                textStyle: {
                    color: "#fff"
                }

            },
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
        "grid": {
            "borderWidth": 0,
            "top": 110,
            "bottom": 95,
            textStyle: {
                color: "#fff"
            }
        },
        "legend": {
            x: '4%',
            top: '11%',
            textStyle: {
                color: '#90979c',
            },
            "data": ['评论月份', '购买月份']
        },
        "xAxis": [{
            "type": "category",
            "axisLine": {
                lineStyle: {
                    color: '#90979c'
                }
            },
            "splitLine": {
                "show": false
            },
            "axisTick": {
                "show": false
            },
            "splitArea": {
                "show": false
            },
            "axisLabel": {
                "interval": 0,

            },
            textStyle: {
                color: '#fff'
            },
            "data": Object.keys(data.sell_buy_month)
        }],
        "yAxis": [{
            "type": "value",
            textStyle: {
                color: '#fff'
            },
            "splitLine": {
                "show": false
            },
            "axisLine": {
                lineStyle: {
                    color: '#90979c'
                }
            },
            "axisTick": {
                "show": false
            },
            "axisLabel": {
                "interval": 0,

            },
            "splitArea": {
                "show": false
            },

        }],
        "dataZoom": [{
            "show": true,
            "height": 30,
            "xAxisIndex": [
                0
            ],
            bottom: 30,
            "start": 10,
            "end": 80,
            handleIcon: 'path://M306.1,413c0,2.2-1.8,4-4,4h-59.8c-2.2,0-4-1.8-4-4V200.8c0-2.2,1.8-4,4-4h59.8c2.2,0,4,1.8,4,4V413z',
            handleSize: '110%',
            handleStyle: {
                color: "#d3dee5"
            },
            textStyle: {
                color: "#fff"
            },
            borderColor: "#90979c"


        }, {
            "type": "inside",
            "show": true,
            "height": 15,
            "start": 1,
            "end": 35
        }],
        "series": [
            {
                "name": "购买月份",
                "type": "bar",
                "barMaxWidth": 35,
                "barGap": "10%",
                "itemStyle": {
                    "normal": {
                        "color": "rgba(255,144,128,1)",
                        "label": {
                            "show": true,
                            "textStyle": {
                                "color": "#fff"
                            },
                            "position": "insideTop",
                            formatter: function (p) {
                                return p.value > 0 ? (p.value) : '';
                            }
                        }
                    }
                },
                "data": Object.values(data.sell_buy_month),
                markPoint: {
                    data: [
                        {type: 'max', name: '最大值'},
                        {type: 'min', name: '最小值'}
                    ]
                },
                markLine: {
                    data: [
                        {type: 'average', name: '平均值'}
                    ]
                }
            },
            {
                "name": "评论月份",
                "type": "line",
                symbolSize: 20,
                symbol: 'circle',
                "itemStyle": {
                    "normal": {
                        "color": "rgba(252,230,48,1)",
                        "barBorderRadius": 0,
                        "label": {
                            "show": true,
                            "position": "top",
                            formatter: function (p) {
                                return p.value > 0 ? (p.value) : '';
                            }
                        }
                    }
                },
                "data": Object.values(data.sell_comment_month),
                markPoint: {
                    data: [
                        {type: 'max', name: '最大值'},
                        {type: 'min', name: '最小值'}
                    ]
                }
            },
        ]
    });
}