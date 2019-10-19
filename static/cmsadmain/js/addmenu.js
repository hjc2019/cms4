init();
function init() {
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


