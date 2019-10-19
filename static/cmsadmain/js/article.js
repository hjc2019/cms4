init();
var checkedlist;
function init() {
    checkedlist = [];

}

function del() {
    $('gridSystemModal').modal(options)
}

//点击跳转到添加文章页面
function addarticle() {
    $(location).attr("href","/cmsadmain/addarticle/");
}

//点击把id传到模态框
function saveid(id) {
    console.log(id);
    $(".modal-body span").html(id)
}

//确认删除
function delarticle() {
    id = $(".modal-body span").html();
    $.ajax({
        type:"post",
        dataType:"json",
        url:"http://127.0.0.1:8000/cmsadmain/delarticle/",
        data:{id:id},
        success:function(data){
            $(location).attr("href","/cmsadmain/article/");
        }
    });
    $('#gridSystemModal').modal('hide')
}


//添加推送
function addpush() {
    var positionid =$(".push select").val();
    var str = JSON.stringify(checkedlist);
    $.ajax({
        type: "post",
        dataType: "json",
        url: "/cmsadmain/addpositioncontent/",
        data: {positionid: positionid,newsid:str},
        success: function (data) {
            if (data.code == 0){
                alert(data.msg);
                $(location).attr("href","/cmsadmain/article/")
            }else{
                alert(data.msg)
            }
        }
    })
}

//选中复选框
function onClickHander(obj){
    if(obj.checked){
        checkedlist.push($(obj).val());
    }else{
        for (i=0;i<checkedlist.length;i++){
            if (checkedlist[i] == $(obj).val()) {
                checkedlist.splice(i,1);
            }
        }
    }
}

//搜索
function search() {
    var catid = $("select[name='menu']").val();
    var title = $("input[name='titlename']").val();
    $(location).attr("href","/cmsadmain/article?catid="+catid+"&title="+title)
}