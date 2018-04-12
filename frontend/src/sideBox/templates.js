(function(){
    var $ = require("../js/jquery.min");
    /* side-box */
    var title_btn = document.querySelector("#_cqupt-title"),
        side = document.querySelector("#_cqupt-side-box");
    var sideTabs = document.querySelectorAll("[data-toggle='sideTab']"),
        sideTabLen = sideTabs.length,
        contentList = document.querySelectorAll("._cqupt-content-item"),
        contentLen = contentList.length;
    side.addEventListener('click', function(e){
        if(!e.target){ return; }
        var eTarget = e.target.getAttribute('data-toggle') == 'sideTab' ? e.target : e.target.parentNode;
        if(eTarget.getAttribute('data-toggle') == 'sideTab'){
            for(var i = 0; i < sideTabLen; i++){
                sideTabs[i].classList.remove('_cqupt-active');
            }
            for(var j = 0; j < contentLen; j++){
                contentList[j].classList.add('_cqupt-hidden');
            }
            var tabTarget = eTarget.getAttribute('data-target');
            if(tabTarget != 'close'){
                eTarget.classList.add('_cqupt-active');
                side.classList.add('_cqupt-active');
                document.querySelector(tabTarget).classList.remove('_cqupt-hidden');
            }else{
                side.classList.remove('_cqupt-active');
            }
        }
    });
    title_btn.onclick = function(){
        document.body.classList.remove('_cqupt-body');
        side.classList.remove('_cqupt-active');
        side.classList.add('_cqupt-close');
    };

    $.ajax({
        'type': "GET",
        'url': "/top_ana_detail/",
        'dataType': 'json',
        'success': function(data) {
            for(var i=0; i<data.length; i++) {
                $("._cqupt-nav-list").append(
                    "<a class=\"_cqupt-nav-item-o\" href=\"/good_detail/?good_id="+ data[i]._id +"\" target=\"_blank\">"+ data[i].name +"</a>"
                )
            }
        }
    })
})();