/* 广告
(function(win,doc){
  var ibody = doc.querySelector('body'), adbox = doc.querySelector('#_cqupt-adbox');
  function outerHeight(el) {
    var height = el.offsetHeight;
    var style = getComputedStyle(el);
    height += parseInt(style.marginTop) + parseInt(style.marginBottom);
    return height;
  }
  var wHeight = win.innerHeight, adHeight = outerHeight(doc.querySelector('#_cqupt-adbox')), maxHeight = 0;
  var bcs = ibody.children;
  for(var i = 0; i < bcs.length; i++){
    if(bcs[i].id.indexOf('_cqupt') === -1 && maxHeight < outerHeight(bcs[i])){
      maxHeight = outerHeight(bcs[i]);
    }
  }
  if(maxHeight){
    ibody.style.minHeight = maxHeight + 'px';
  }
  if(wHeight > adHeight + maxHeight) {
    adbox.style.top = (wHeight-adHeight) + 'px';
  }
  doc.querySelector('#_cqupt-adbox-close').onclick = function(){
    adbox.style.display = 'none';
  };
})(window,document);
 */

(function(){
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

    // 热门排行
    // (function(data){
    //     var html = '<tbody>';
    //     for(var i = 0; i < data.length; i++){
    //         html += '<tr>';
    //         html += '<td>' + data[i].user_id +'</td>';
    //         html += '<td>' + data[i].user_name +'</td>';
    //         html += '<td>' + data[i].time +'</td>';
    //         html += '<td>' + data[i].money +'</td>';
    //         html += '</tr>';
    //     }
    //     html += '</tbody>';
    //     document.querySelector("._cqupt-donate-list").insertAdjacentHTML("afterbegin", html);
    // })(require('../../json/donate'));
})();