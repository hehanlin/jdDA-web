module.exports = function (data) {
    window.data = data;
    require("./echarts_section/1")(data);
    require("./echarts_section/2")(data);
    require("./echarts_section/3")(data);
    require("./echarts_section/4")(data);
    require("./echarts_section/5")(data);
    require("./echarts_section/6")(data);
    require("./echarts_section/7")(data);
    require("./echarts_section/8")(data);
    require("./echarts_section/9")(data);
    require("./echarts_section/10")(data);
    require("./echarts_section/11")(data);
};