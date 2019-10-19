init();
function init() {
     $.ajax({
        type: "get",
        dataType: "json",
        url: "http://127.0.0.1:8000/cmsadmain/admainheaderHandler/",
        success: function (data) {
        }
    });
}

//点击编辑把推荐位内容id存到模态框,以及后台获取所有推荐位的数据
function update(id) {
    $(".modal-header .positioncontentid").val(id);
    $.ajax({
        type: "post",
        dataType: "json",
        url: "http://127.0.0.1:8000/cmsadmain/updatepositioncontent/",
        success: function (data) {
            console.log(data);
            str = "<select>";
            str+="<option disabled selected hidden>"+"请选择推荐位"+"</option>";
            for (i=0;i<data.length;i++){
                str+="<option value='"+data[i].id+"'>"+data[i].name+"</option>";
            }
            str+="</select>";
            $(".modal-body .form-group").html(str)
        }
    })
}

//点击删除把推荐位内容id存到模态框
function del(id) {
    $(".modal-body span").html(id)
}

//点击保存修改
function saveupdate() {
    //获取推荐位id以及当前推荐内容id
    var positionid = $(".modal-header .positioncontentid").val();
    var positioncontentid = $(".modal-body select").val();
    console.log(positionid,positioncontentid);
    if (positioncontentid == null){
        $(".hint").css({"display":"block"});
    }else{
        $(".hint").css({"display":"none"});
        $.ajax({
            type: "post",
            dataType: "json",
            url: "http://127.0.0.1:8000/cmsadmain/update_position_content_Handler/",
            data: {positionid : positionid ,positioncontentid:positioncontentid},
            success: function (data) {
                $('#exampleModal').modal('hide');
                $(location).attr("href","/cmsadmain/positioncontent/");
            }
        })
    }
}

//点击确认删除
function del_positioncontent() {
     var id = $(".modal-body span").html();
    $.ajax({
        type:"post",
        dataType:"json",
        url:"http://127.0.0.1:8000/cmsadmain/del_position_content/",
        data:{id:id},
        success:function(data){
            $(location).attr("href","/cmsadmain/positioncontent/");
        }
    });
    $('#gridSystemModal').modal('hide')
}