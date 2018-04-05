var echarts = require("echarts");
require("echarts-wordcloud");
var $ = require("../jquery.min");

module.exports = function (data) {
    var s_10_1 = echarts.init(document.getElementById("s-10-1"));
    s_10_1.setOption({
        title: {
            text: "前一千条关键字摘要",
            left: 'center',
            textStyle: {
                color: '#f2c967',
                fontSize: 20
            }
        },
        series: [{
            type: 'wordCloud',
            shape: 'circle',
            width: '70%',
            height: '80%',
            rotationStep: 45,
            gridSize: 8,
            drawOutOfBound: false,
            textStyle: {
                normal: {
                    fontFamily: 'sans-serif',
                    fontWeight: 'bold',
                    // Color can be a callback function or a color string
                    color: function () {
                        // Random color
                        return 'rgb(' + [
                            Math.round(Math.random() * 160),
                            Math.round(Math.random() * 160),
                            Math.round(Math.random() * 160)
                        ].join(',') + ')';
                    }
                },
                emphasis: {
                    shadowBlur: 10,
                    shadowColor: '#333'
                }
            },
            data: (function (data) {
                var tmp = [];
                for (var key in data.keyword_of_summary) {
                    tmp.push({
                        value: data.keyword_of_summary[key],
                        name: key,
                    })
                }
                return tmp;
            })(data)
        }]
    });

    $("#s-10-2-h1").html($("#s-10-2-h1").html() + " 共有 " + data.all_top_nice_comment.usefulVoteCount + " 人点赞");
    $("#s-10-2-1").html(data.all_top_nice_comment.content);
    $("#s-10-2-h2").html($("#s-10-2-h2").html() + " 共有 " + data.all_top_reply_comment.replyCount + " 人回复");
    $("#s-10-2-2").html(data.all_top_reply_comment.content);
};