require('../style.css');
var $ = require('./jquery.min');
require('./tagcloud.min');
// templates
var sideBoxTemplates = require('../templates/templates.html');
document.body.insertAdjacentHTML("beforeend", sideBoxTemplates);
require('../templates/templates');

$(function() {
    var main_input = $('.main_input'), enter = $("#enter"), more = $("#more"), $tagcloud = $(".tagcloud"), $status = $("#status");
    var more_text = more.find("p");
    //升起动画控制
    var iUp = (function() {
        var t = 0,
            d = 200,
            clean = function(){
                t = 0;
            },
            up = function(e) {
                setTimeout(function() {
                    $(e).removeClass("down")
                }, t);
                t += d;
            },
            down = function(e){
                $(e).addClass("down");
            },
            toggle = function(e){
                setTimeout(function() {
                    $(e).toggleClass("down")
                }, t);
                t += d;
            };
        return {
            clean: clean,
            up: up,
            down: down,
            toggle: toggle
        }
    })();
    $(".iUp").each(function(i, e) {
        iUp.up(e);
    });
    var status = {
        reset: function(){
            $status.find("i").attr("class", "reset");
            $status.find("span").text("正在查询中");
        },
        on: function(data, text){
            $status.find("i").attr("class", "on");
            if(!text){
                $status.find("span").text("爬虫集群在线 " + data + "ms");
            }else{
                $status.find("span").text(text);
            }
        },
        off: function(){
            $status.find("i").attr("class", "off");
            $status.find("span").text("服务器超时");
        },
        unknown: function(){
          $status.find("span").text("未知");
        }
    };
    //服务器状态
    var statusQuery = function(){
        status.reset();
        var start_time = new Date().getTime();
        var query = $.ajax({
            url: "/ping/?" + start_time,
            timeout : 10000,
            success: function(data){
                if(data == 1) {
                    var end_time = new Date().getTime();
                    status.on(end_time-start_time, null);
                }else {
                    status.unknown();
                }
            },
            complete: function(XMLHttpRequest){
                if(XMLHttpRequest.status !== 200){
                    query.abort();
                    status.unknown();
                }
            }
        });
    };
    statusQuery();
    $status.on("click", statusQuery);
    main_input.on({
        focus: function () {
            if (this.value == this.defaultValue) {
                this.value = "";
            }
            more.hide();
            enter.addClass("active");
        },
        blur: function () {
            if (this.value == "") {
                this.value = this.defaultValue;
            }
            more.hide();
            enter.removeClass("active");
        },
        keypress: function (event) {
            if (event.keyCode == "13") {
                enter.click();
            }
        }
    });
    //输入框确认点击
    enter.on("click", function () {
        more.show();
        var main_input_val = $.trim(main_input.val());
        if (main_input_val.indexOf("http://") != -1) {
            main_input_val = main_input_val.split("http://")[1];
            main_input.val(main_input_val);
        }
        if (main_input_val.indexOf("https://") != -1 ) {
            main_input_val = main_input_val.split("https://")[1];
            main_input.val(main_input_val);
        }
        if (url) {
            window.open(url);
        }
    });
    //读取json数据，顶部悬浮提醒框warn文本及tagList快捷链接
    $.ajax({
        url: "/category/",
        success: function (data) {
            data = JSON.parse(data)
            $.each(data, function (i, e) {
                $tagcloud.append("<a target='_blank' href='/analysis_category/?cat_id=" + e.cat_id + "'>" + e.name + "</a>");
            });
            tagcloud({
                radius: 175,
                fontsize: 18
            });
        }
    });
    //底部信息切换
    setTimeout(show_about, 10000);
    function show_about() {
        $(".about#tome").fadeToggle();
        $(".about#toblues").fadeToggle();
        setTimeout(show_about, 10000);
    }

//顶部悬浮提醒框
  var warn = $("#warn"), warn_text = $("#warn-text");
  var s = warn.get(0), si = warn_text.get(0);
  var s_scrollLeft, s_add = 1, tmar;
//文字滑动
  function mar() {
    if (s.offsetWidth <= si.offsetWidth) {
      s_scrollLeft = s.scrollLeft;
      s.scrollLeft += s_add;
      if (s_scrollLeft == s.scrollLeft) {
        s_add = -s_add;
      }
      tmar = setTimeout(mar, 20);
    }
  }
  //框体升降
  var warnBox = {
    up: function () {
      warn.animate({ "top": "-48px" }, "slow");
      clearTimeout(tmar);
    },
    down: function (text) {
      var t = {
        showTime: 500,
        moveTime: 4000,
        totalTime: 15000
      };
      $.each(text, function (i, e) {
        setTimeout(function () {
          s.scrollLeft = 0;
          warn_text.html(e);
          warn.animate({"top": "18px"}, "slow");
        }, t.totalTime * i + t.showTime);
        setTimeout(function () {
          mar();
        }, t.totalTime * i + t.moveTime);
        setTimeout(function () {
          warnBox.up();
        }, t.totalTime * i + t.totalTime);
      });
    }
  };
  var warn_text_array = ['暂无'];
  // warnBox.down(warn_text_array);
});