init();
function init() {
    // 实时监听浏览器文档高度并给侧边栏高度赋值
    var _allHeight = $(document).height();//总高度
    var _clientHeight = $(window).height();//浏览器可视页面的高度
    var beside = $(".backcolor");
    beside.css({"height": _clientHeight - 52});
    $(window).scroll(function () {
        var _scroolTop = $(window).scrollTop();//滚动条上方的高度
        if ((_scroolTop + _clientHeight) > (_allHeight - 10)) {
            beside.css({"height": _clientHeight - 52 + _scroolTop});
        }
    });

    $.ajax({
        type: "get",
        dataType: "json",
        url: "/cmsadmain/admainheaderHandler/",
        success: function (data) {
            $(".currentuser b").html(data.user)
        }
    });

    //获取当前网址url路径名
    var urlname = location.pathname;
    //先删除所有a标签的选中状态
    $(".menu a").parent().removeClass("active");
    //得到每个菜单的a标签的href属性值
   $(".menu a").each(function () {
       var href = $(this).attr("href");
       if (href == urlname){
            $(this).parent().addClass("active")
        }
   })
}

function exit() {
    $.ajax({
        type: "get",
        dataType: "json",
        url: "/cmsadmain/admainheader/",
        success: function (data) {
            if (data.code == 0) {
                alert(data.msg);
                $(location).attr("href","/cmsadmain/login/");
            }
        }
    });
}