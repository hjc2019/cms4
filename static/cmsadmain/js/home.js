init();
function init() {
    $.ajax({
        type: "get",
        dataType: "json",
        url: "http://127.0.0.1:8000/cmsadmain/home/",
        success: function (data) {
        }
    });
}