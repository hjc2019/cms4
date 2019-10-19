init();
function init() {
    // 获取当前编辑菜单id
    var id = window.location.search.split('=')[1];
    $.ajax({
        type: "post",
        dataType: "json",
        url: "http://127.0.0.1:8000/cmsadmain/updatemenu/",
        data:{id:id},
        success: function (data) {
            // 得到数据之后给前端赋值
            $(".menuname input:eq(0)").val(data.menuname);
            $(".menuname input:eq(1)").val(id);
            var admainmenu = $(".menutype input:eq(0)").val();
            var openmenu = $(".menustate input:eq(0)").val();
            if (data.menutype == admainmenu){
                $(".menutype input:eq(0)").attr("checked","on")
            }else {
                $(".menutype input:eq(1)").attr("checked","on")
            }
            if (data.menustate == openmenu){
                $(".menustate input:eq(0)").attr("checked","on")
            }else {
                $(".menustate input:eq(1)").attr("checked","on")
            }
        }
    });

    // 表单验证
     var validator = $("form").validate({
        rules:{
            menuname:{
                required:true
            },
            menutype:{
                required:true
            },
            menustate:{
                required:true
            }
        },
        messages:{
          menuname: {
              required:"菜单名不能为空!"
          },
          menutype:{
              required:"请选择菜单类型!"
          },
          menustate:{
              required:"请选择菜单状态!"
          }
        },
        submitHandler: function (form) {
            $("form").ajaxSubmit(function(data){
                var data1 = JSON.parse(data);
                $(".modal-body").html(data1.msg);
                $(".modal-body").attr("index",data1.code);
                $('#bs-example-modal-sm').modal();
            })
        }
    });
}

function save() {
    var index = $(".modal-body").attr("index");
    if (index == 0){
        $('#bs-example-modal-sm').modal('hide');
        $(location).attr("href","/cmsadmain/menus/");
    }else{
        $('#bs-example-modal-sm').modal('hide');
    }

}










