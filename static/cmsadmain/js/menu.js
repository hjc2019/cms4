init();
function init() {


}

//点击删除的时候把id值传到模态框里面
function del(id) {
    $(".modal-body span").html(id);
}
//点击确认删除
function save() {
    var id = $(".modal-body span").html();
    $.ajax({
        type:"post",
        dataType:"json",
        url:"/cmsadmain/delmenu/",
        data:{id:id},
        success:function(data){
            if (data.code == 0){
                $(".table tr[index='"+id+"']").remove()
            }
        }
    });
    $('#gridSystemModal').modal('hide')
}

//编辑菜单
function updatamenu(id) {
    $(location).attr("href","/cmsadmain/updatemenu/?id="+id)
}

function addmenu() {
    $(location).attr("href","/cmsadmain/addmenu/")
}