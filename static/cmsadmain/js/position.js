init();
function init() {

}

function del() {
    $('#gridSystemModal').modal('show')
}

function open() {
    $('#exampleModal').modal('show')
}
//添加推荐位
function addposition() {
    var content = $("#recipient-name").val();
     if (content == ""){
        $(".hint").css({"display":"block"});
    }else{
        $(".hint").css({"display":"none"});
        $.ajax({
            type: "post",
            dataType: "json",
            url: "http://127.0.0.1:8000/cmsadmain/addposition/",
            data: {name: content},
            success: function (data) {
                $('#exampleModal').modal('hide');
                $(location).attr("href","/cmsadmain/positions/");
            }
        })
    }
}

// 编辑推荐位
function updateposition(id) {
    $.ajax({
        type: "post",
        dataType: "json",
        url: "http://127.0.0.1:8000/cmsadmain/updateposition/",
        data: {id: id},
        success: function (data) {
            $('#exampleModalLabel').html(data.title);
            $('#recipient-name').val(data.name);
            $(".save").attr("onclick","saveposition("+data.id+")")
        }
    })
}
//保存编辑的推荐位
function saveposition(id) {
    var content = $("#recipient-name").val();
     if (content == ""){
        $('#exampleModal').modal('hide')
    }else{
        $.ajax({
            type: "post",
            dataType: "json",
            url: "http://127.0.0.1:8000/cmsadmain/updatepositionHandler/",
            data: {name: content,id:id},
            success: function (data) {
                if (data.code == 0){
                    $(location).attr("href","/cmsadmain/positions/");
                }
                $('#exampleModal').modal('hide');
            }
        })
    }
}

//删除推荐位
//点击删除的时候把id值传到模态框里面
function del(id) {
    $(".modal-body span").html(id);
}
//点击确认删除
function delposition() {
    var id = $(".modal-body span").html();
    $.ajax({
        type:"post",
        dataType:"json",
        url:"http://127.0.0.1:8000/cmsadmain/delposition/",
        data:{id:id},
        success:function(data){
            $(location).attr("href","/cmsadmain/positions/");
        }
    });
    $('#gridSystemModal').modal('hide')
}