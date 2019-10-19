init();
function init() {
    //获取网址传过来的id
    var newsid = location.search.split('=')[1];
    $("input[name='newsid']").val(newsid);

    // 监听上传的图片文件并进行图片预览
   $("input[name='newsimg']").change(function () {
            //获取文件以及地址
            var imgFile = this.files.item(0);
            var _url = window.URL.createObjectURL(imgFile);
            var str = imgFile.name.split('.');
            var filename = str[str.length-1];
            //定义允许上传的文件格式
            var list = ["jpg","jpeg","png"];
            if (list.indexOf(filename) != -1){
                $(".preview").attr("src",_url);
            } else{
                $(".preview").attr("src","/static/newsimg/img.png");
                alert("上传的文件格式不正确!");
                return;
            }
    });

    //表单验证
    var validator = $("form").validate({
        rules:{
            title:{
                required:true
            },
            menu:{
                required:true
            }
        },
        messages:{
          title: {
              required:"标题不能为空!"
          },
          menu:{
              required:"请选择所属栏目!"
          }
        },
        submitHandler: function (form) {
            $("form").ajaxSubmit(function(data){
                data1 = JSON.parse(data);
                if (data1.code == 0){
                    alert(data1.msg);
                    $(location).attr("href","/cmsadmain/article/")
                }else {
                    alert(data1.msg)
                }
            })
        }
    });
}

function look() {
    var color = $(".titlecolor select").val();
    $(".newstitle input").css({"color":color})
}

function back() {
    $(location).attr("href","/cmsadmain/article/")
}















