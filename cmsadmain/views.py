import math
import os
from datetime import datetime,date
from django.shortcuts import render
from cmsadmain.models import *
from django.http import HttpResponse
from common import returnResult
from django.forms import forms
from DjangoUeditor.forms import  UEditorField
import json
from cms import settings
from common import utils
# Create your views here.
class TestUEditorForm(forms.Form):
    content = UEditorField('', width=700, height=400, toolbars="full", imagePath="static/images/", filePath="static/files/", upload_settings={"imageMaxSize":1204000},settings={})

######################主页
def home(request):
    # 获取文章最大阅读数量
    list = news.objects.values("num").order_by('-num')
    # 文章数
    count = list.count()
    # 今日登录用户
    todayuser = admain.objects.filter(lasttime=date.today()).count()
    # 推荐位数
    positioncount = position.objects.all().count()

    context = {"newscount": count, "maxread": list[0]["num"], "todayuser": todayuser,"positioncount": positioncount}
    return render(request, "../templates/cmsadmain/home/home.html", context)


def admainheader(request):
    request.session.flush()
    return HttpResponse(returnResult.returnResult(0, "已退出，欢迎下次登录!"))

def admainheaderHandler(request):
    # 获取session当前登录用户
    user = request.session.get("user")
    return HttpResponse(user)



######################菜单管理
def menus(request):
    # 获取数据，分页显示
    count = settings.PAGES["everypages"]
    current_page = request.GET.get("p")  # 当前页码
    if current_page == None:
        current_page = 1
    allcount = menu.objects.all().count()  # 数据总条数
    pageRange = utils.viewpage(current_page,allcount)#显示的按钮
    list = menu.objects.all().order_by("-id")[((int(current_page) - 1) * count):int(current_page) * count]  # 得到的数据
    pagecount = math.ceil(allcount / count)  #按每页五条所分的总页数
    context = {"menulist": list, "pageRange": pageRange,"current_page": int(current_page),"pagecount":pagecount}
    return  render(request, "../templates/cmsadmain/menu/menu.html", context)

def menusHandler(request):
    list = menu.objects.values("id","menuname","menutype","menustate")
    menulist = []
    if list.count()>0:
        for item in list:
            menulist.append(item)
        rs = json.dumps(menulist)
        return HttpResponse(rs)
    return HttpResponse(0)

#添加菜单
def addmenu(request):
    context = {}
    return render(request, "../templates/cmsadmain/menu/addmenu.html", context)

def addmenuHandler(request):
    if request.method == "POST":
        # 获取前端发送的数据
        name = request.POST.get("menuname")
        type = request.POST.get("menutype")
        state = request.POST.get("menustate")
        print(name, type, state)
        #获取数据库判断添加的数据是否存在
        list = menu.objects.values("menuname","menutype").filter(menuname=name)
        for item in list:
           if item["menuname"] == name and item["menutype"] == type:
               rs = returnResult.returnResult(1, "该栏目已存在!")
               return HttpResponse(rs)

        #将数据存储到数据库
        obj = menu(menuname=name,menustate=state,menutype=type)
        obj.save()
        #向前端返回数据
        rs = returnResult.returnResult(0,"添加成功!")
        return HttpResponse(rs)

#编辑菜单
def updatemenu(request):
    if request.method == "POST":
        id = request.POST.get("id")
        list = menu.objects.values("menuname","menutype","menustate").filter(id=id)
        dic = {}
        for item in list:
            dic = {"menuname":item["menuname"],"menutype":item["menutype"],"menustate":item["menustate"]}
        str = json.dumps(dic)
        return HttpResponse(str)
    context = {}
    return render(request, "../templates/cmsadmain/menu/updatemenu.html", context)

def updatemenuHandler(request):
    if request.method == "POST":
        # 获取前端发送的数据
        id = request.POST.get("menuid")
        name = request.POST.get("menuname")
        type = request.POST.get("menutype")
        state = request.POST.get("menustate")
        print(id,name, type, state)
        # 获取数据库判断添加的数据是否存在
        list = menu.objects.values("menuname", "menutype","menustate").filter(menuname=name)
        for item in list:
            if item["menuname"] == name and item["menutype"] == type and item["menustate"] == state:
                rs = returnResult.returnResult(1, "该栏目已存在!")
                return HttpResponse(rs)

        # 将数据修改后存储到数据库
        menu.objects.filter(id = id).update(menuname=name,menutype=type,menustate=state)
        # 向前端返回数据
        rs = returnResult.returnResult(0, "修改成功!")
        return HttpResponse(rs)

#删除菜单
def delmenu(request):
    id = request.POST.get("id")
    try:
        menu.objects.filter(id = id).delete()
        return HttpResponse(returnResult.returnResult(0, "删除成功!"))
    except Exception as e:
        return HttpResponse(returnResult.returnResult(1, "删除失败!"))


######################文章管理页面
def article(request):
    #获取搜索条件
    menuid = request.GET.get("catid")
    titlename = request.GET.get("title")
    if menuid == None or titlename == None:
        menuid = "-1"
        titlename = ""
    count = settings.PAGES["everypages"]  # 每页5条信息
    #获取全部栏目以及推送位
    menulist = menu.objects.values("id","menuname")
    positionlist = position.objects.values("id","name")

    current_page = request.GET.get("p")     #当前页码
    if current_page == None:
        current_page = 1
    #每页获取的五条信息,获取数据总条数
    #根据搜素条件是否存在来获取信息
    if menuid == "-1" and titlename == "":
        allcount = news.objects.all().count()   #数据总条数
        list = news.objects.all().order_by("-id")[((int(current_page)-1)*count):int(current_page)*count]    #搜索得到的数据
    elif menuid == "-1" and titlename != "":
        allcount = news.objects.filter(title__contains=titlename).count()
        list = news.objects.filter(title__contains=titlename).order_by('-id')[((int(current_page)-1)*count):int(current_page)*count]
    elif menuid != "-1" and titlename == "":
        allcount = news.objects.filter(catid=menuid).count()
        list = news.objects.filter(catid=menuid).order_by('-id')[((int(current_page) - 1) * count):int(current_page) * count]
    else:
        allcount = news.objects.filter(catid=menuid,title__contains=titlename).count()
        list = news.objects.filter(catid=menuid,title__contains=titlename).order_by('-id')[((int(current_page) - 1) * count):int(current_page) * count]

    pagecount = math.ceil(allcount / count)  # 按每页五条所分的总页数
    #通过匿名函数筛选得到栏目名
    for item in list:
        name = filter(lambda x: x['id']==item.catid,menulist)
        for i in name:
            item.menuname = i['menuname']

    pageRange = utils.viewpage(current_page,allcount)
    print(pageRange)
    context = {"menulist": menulist, "position": positionlist,"newslist": list,"pageRange":pageRange,"current_page":int(current_page),"menuid":int(menuid),"titlename":titlename,"pagecount":pagecount}
    return render(request,"../templates/cmsadmain/article/article.html",context)

def articleHandler(request):
    return HttpResponse(0)

#添加文章
def addarticle(request):
    list = menu.objects.values("menuname","id").filter(menutype="前台栏目")
    menudic = {}
    menulist = []
    for item in list:
        menudic = {"id":item["id"],"menuname":item["menuname"]}
        menulist.append(menudic)
    form = TestUEditorForm()
    return render(request,"../templates/cmsadmain/article/addarticle.html",{"form":form,"list":menulist})

def addarticleHandler(request):
    #接收前端提交的数据
    title = request.POST.get("title")
    titlecolor = request.POST.get("color")
    newsmenu = request.POST.get("menu")
    newsimg = request.FILES.get("newsimg")
    content = request.POST.get("content")
    print(title,titlecolor,newsmenu,newsimg,content)
    #缩略图不存在的情况
    if newsimg == None:
        #同时标题颜色不存在
        if titlecolor == None:
            obj = news.objects.create(catid=newsmenu,title=title,num=0,time=datetime.now())
        else:
            obj = news.objects.create(catid=newsmenu,title=title,titlt_font_color=titlecolor,num=0,time=datetime.now())
        #获取刚存进去的id
        newsid = obj.id
        #把文章内容存入内容表中
        obj2 = news_content.objects.create(newsid=newsid,content=content)
        return HttpResponse(returnResult.returnResult(0,"添加成功!"))
    #缩略图存在的情况
    if newsimg != None:
        #判断传过来的文件是否是项目需要的
        if newsimg.name.split('.')[-1] not  in ["jpg","jpeg","png"]:
            return HttpResponse(returnResult.returnResult(1,"添加失败，文件格式不正确!"))
        #判断文件是否过大
        size = utils.getsize(newsimg.size)
        if float(size)> 100:
            return HttpResponse(returnResult.returnResult(1,"添加失败，文件过大!"))
        #创建文件名以及指定文件保存的路径
        filename = "newsImg_" + str(int(datetime.now().timestamp() * 1000000)) + "." + newsimg.name.split('.')[-1]
        #需要判断指定的文件夹存不存在，不存在就创建
        dir = "static/newsimg"
        utils.creatDir(dir)
        savePath=dir+"/"+filename
        #写入文件中
        with open(savePath,'wb') as f:
            for file in newsimg.chunks():
                f.write(file)
                f.flush()

        #存入数据库
        #标题颜色不存在的情况
        if titlecolor == None:
            obj = news.objects.create(catid=newsmenu,title=title,thumb=filename, num=0,time=datetime.now())
        else:
            obj = news.objects.create(catid=newsmenu, title=title, titlt_font_color=titlecolor,thumb=filename, num=0, time=datetime.now())
        # 获取刚存进去的id
        newsid = obj.id
        # 把文章内容存入内容表中
        obj2 = news_content.objects.create(newsid=newsid, content=content)
        return HttpResponse(returnResult.returnResult(0, "添加成功!"))

#编辑文章
def updatearticle(request):
    #获取前端传过来的id
    newsid = request.GET.get("id")
    #查询数据库
    newlist = news.objects.values("title","titlt_font_color","catid","thumb").filter(id = newsid)
    content = news_content.objects.values("content").filter(newsid = newsid)
    #数据处理
    contentstr = ""
    dic = {}
    list = []
    for item in content:
         contentstr = item["content"]
         for item2 in newlist:
             list = menu.objects.values("menuname","id").filter(menutype="前台栏目")
             name = filter(lambda x: x['id'] == item2["catid"],list)
             for i in name:
                 dic = {"title":item2["title"],"titlecolor":item2["titlt_font_color"],"menu":i["menuname"],"catid":item2["catid"],"thumb":item2["thumb"],"content":contentstr}
    form = TestUEditorForm()
    return render(request,"../templates/cmsadmain/article/updatearticle.html",{"form":form,"news":dic,"menulist":list})

def updatearticleHandler(request):
    newsid = request.POST.get("newsid")
    title = request.POST.get("title")
    titlecolor = request.POST.get("color")
    newsmenu = request.POST.get("menu")
    newsimg = request.FILES.get("newsimg")
    oldnewsimg = request.POST.get("preImg")
    newcontent = request.POST.get("content")
    # 缩略图不存在
    if newsimg == None:
        # 如果标题颜色不存在
        if titlecolor == None:
            news.objects.filter(id = newsid).update(catid=newsmenu, title=title,time=datetime.now())
        else:
            news.objects.filter(id = newsid).update(catid=newsmenu, title=title, titlt_font_color=titlecolor, time=datetime.now())
        # 把修改的文章内容存到数据库中
        if newcontent != None:
            news_content.objects.filter(newsid=newsid).update(content=newcontent)
            return HttpResponse(returnResult.returnResult(0, "修改成功!"))
        else:
            return HttpResponse(returnResult.returnResult(1, "修改失败，内容不能为空!"))
    # 新的缩略图存在
    if newsimg != None:
        # 判断上传过来的文件类型是否是项目需要的
        if newsimg.name.split(".")[-1] not in ["jpg", "jpeg", "png"]:
            return HttpResponse(returnResult.returnResult(1, "修改失败，文件类型不正确"))
        # 判断文件是否过大
        size = utils.getsize(newsimg.size)
        if float(size) > 100:
            return HttpResponse(returnResult.returnResult(2, "修改失败，文件过大!"))

        # 创建文件名 以及指定到保存文件的路径
        filename = "newsImg_" + str(int(datetime.now().timestamp() * 1000000)) + "." + newsimg.name.split(".")[-1]
        # 需要判断指定的文件夹存不存在，不存在就创建
        dir = "static/newsimg"
        utils.creatDir(dir)
        savePath = dir + "/" + filename
        # 写入文件中
        with open(savePath, 'wb') as f:
            for file in newsimg.chunks():
                f.write(file)
                f.flush()
        #删除原来的图片
        path1 = "static/newsimg/"+oldnewsimg
        path = os.path.join(settings.BASE_DIR,path1)
        os.remove(path)
        # 存入数据库中
        # 如果标题颜色不存在
        if titlecolor == None:
            news.objects.filter(id = newsid).update(catid=newsmenu, title=title, thumb=filename, time=datetime.now())
        else:
            news.objects.filter(id = newsid).update(catid = newsmenu, title = title, titlt_font_color = titlecolor, thumb = filename, time = datetime.now())
        # 把文章内容存到数据库中
        if newcontent != None:
            news_content.objects.filter(newsid=newsid).update(content=newcontent)
            return HttpResponse(returnResult.returnResult(0, "修改成功!"))

#删除文章
def delarticel(request):
    newsid = request.POST.get("id")
    print(newsid)
    news.objects.filter(id=newsid).delete()
    news_content.objects.filter(newsid=newsid).delete()
    return HttpResponse(0)

###################用户管理
def user(request):
    userlist = admain.objects.values("id", "username", "resume", "email", "headimg").all()
    context = {
        "userlist": userlist
    }
    return  render(request, "../templates/cmsadmain/user/user.html", context)

# 添加用户
def adduser(request):
    form=TestUEditorForm()
    return  render(request, "../templates/cmsadmain/user/adduser.html", {"form":form})

# 添加用户的操作
def adduserHandler(request):
    headImg = request.FILES.get("heading")
    username=request.POST.get("username")
    password=request.POST.get("pwd")
    email=request.POST.get("email")
    content = request.POST.get("content")
    # 判断用户名是否已经存在
    # 存在，提示该用户名已存在
    newusername = admain.objects.all()
    for item in newusername:
        if username == item.username:
            return HttpResponse(returnResult.returnResult(1, "该用户名已存在"))
    #判断用户是否上传了头像
    if headImg == None:
        #判断是否有用户简介
        if content == None:
            newuser = admain.objects.create(username=username, password=password, email=email)
        else:
            newuser = admain.objects.create(username=username, password=password, email=email,resume=content)
    else:
        # 判断文件是否过大
        size=utils.getsize(headImg.size)
        if float(size) > 100:
            print("文件过大")
            return
        # 判断上传过来的文件类型是否是项目需要的：
        if headImg.name.split(".")[-1] not in ["jpg", "jpeg", "png"]:
            print("文件类型不正确")
            return
        # 把文件保存到指定的路径中
        # 比方说static/headImg
        # 创建文件名 以及指定到保存文件的路径
        filename = "headImg_" + str(int(datetime.now().timestamp() * 1000000)) + "." + headImg.name.split(".")[-1]
        dir = "static/headImg"
        utils.creatDir(dir)
        savePath = dir + "/" + filename
        # 写入文件中
        with open(savePath, 'wb') as f:
            for file in headImg.chunks():
                f.write(file)
                f.flush()
        if content == None:
            newuser = admain.objects.create(username=username, password=password, email=email,headimg=filename)
        else:
            newuser = admain.objects.create(username=username, password=password, email=email,headimg=filename, resume=content)
    return HttpResponse(returnResult.returnResult(0,"添加成功"))

# 删除管理员信息
def deleteUser(request):
    deleteIndex=request.GET.get("deleteIndex")
    admain.objects.filter(id=deleteIndex).delete()
    return HttpResponse(returnResult.returnResult(0, "删除成功"))

# 编辑管理员信息
def reuser(request):
    editIndex = request.GET.get("editIndex")
    list = admain.objects.values("id","username", "password", "email", "headimg", "resume").get(id=editIndex)
    form=TestUEditorForm()
    return render(request, "../templates/cmsadmain/user/reuser.html", {"form":form,"user":list})

def resave(request):
    headImg = request.FILES.get("heading")
    oldheadimg =request.POST.get("preImg")
    username = request.POST.get("username")
    oldname = request.POST.get("oldname")
    print(username,oldname)
    password = request.POST.get("pwd")
    email = request.POST.get("email")
    uid=request.POST.get("id")
    content = request.POST.get("content")
    #判断用户名是否跟原来的一样
    if username != oldname:
        # 判断用户名是否已经存在
        # 存在，提示该用户名已存在
        newusername = admain.objects.all()
        for item in newusername:
            if username == item.username:
                return HttpResponse(returnResult.returnResult(1, "该用户名已存在"))
            elif username != item.username and item == newusername[len(newusername)-1]:
                #判断用户是否更新了头像
                if headImg == None:
                    admain.objects.filter(id=uid).update(username=username, password=password, email=email,resume = content)
                    return HttpResponse(returnResult.returnResult(0, "更改成功"))
                else:
                    # 判断文件是否过大
                    size = utils.getsize(headImg.size)
                    if float(size) > 100:
                        return HttpResponse(returnResult.returnResult(2, "文件过大!"))
                    # 判断上传过来的文件类型是否是项目需要的：
                    if headImg.name.split(".")[-1] not in ["jpg", "jpeg", "png"]:
                        return HttpResponse(returnResult.returnResult(3, "文件类型不正确!"))
                    # 把文件保存到指定的路径中
                    # 创建文件名 以及指定到保存文件的路径
                    filename = "headImg_" + str(int(datetime.now().timestamp() * 1000000)) + "." + headImg.name.split(".")[-1]
                    dir = "static/headImg"
                    utils.creatDir(dir)
                    savePath = dir + "/" + filename
                    # 写入文件中
                    with open(savePath, 'wb') as f:
                        for file in headImg.chunks():
                            f.write(file)
                            f.flush()
                    # 删除原来的图片
                    path1 = "static/headImg/" + oldheadimg
                    path = os.path.join(settings.BASE_DIR, path1)
                    os.remove(path)
                    admain.objects.filter(id=uid).update(username=username, password=password, email=email, headimg=filename,resume = content)
                    return HttpResponse(returnResult.returnResult(0, "更改成功"))
    else:
        # 判断用户是否更新了头像
        if headImg == None:
            admain.objects.filter(id=uid).update(username=username, password=password, email=email,resume = content)
            return HttpResponse(returnResult.returnResult(0, "更改成功"))
        else:
            # 判断文件是否过大
            size = utils.getsize(headImg.size)
            if float(size) > 100:
                return HttpResponse(returnResult.returnResult(2, "文件过大!"))
            # 判断上传过来的文件类型是否是项目需要的：
            if headImg.name.split(".")[-1] not in ["jpg", "jpeg", "png"]:
                return HttpResponse(returnResult.returnResult(3, "文件类型不正确!"))
            # 把文件保存到指定的路径中
            # 创建文件名 以及指定到保存文件的路径
            filename = "headImg_" + str(int(datetime.now().timestamp() * 1000000)) + "." + headImg.name.split(".")[-1]
            dir = "static/headImg"
            utils.creatDir(dir)
            savePath = dir + "/" + filename
            # 写入文件中
            with open(savePath, 'wb') as f:
                for file in headImg.chunks():
                    f.write(file)
                    f.flush()
            # 删除原来的图片
            path1 = "static/headImg/" + oldheadimg
            path = os.path.join(settings.BASE_DIR, path1)
            os.remove(path)
            admain.objects.filter(id=uid).update(username=username, password=password, email=email, headimg=filename,resume = content)
            return HttpResponse(returnResult.returnResult(0, "更改成功"))


#################推荐位管理
def positions(request):
    list = position.objects.all()
    dic = {}
    li = []
    for item in list:
        dic = {"id":item.id,"name":item.name}
        li.append(dic)
    return render(request, "../templates/cmsadmain/position/position.html", {"list":li})

#添加推荐位
def addposition(request):
    name = request.POST.get("name")
    obj = position(name=name)
    obj.save()
    return HttpResponse(0)

#编辑推荐位
def updataposition(request):
    id = request.POST.get("id")
    list = position.objects.values("id","name").filter(id = id)
    dic = {}
    for item in list:
        dic = {"title":"编辑推荐位","name":item["name"],"id":item["id"]}
    str = json.dumps(dic)
    return HttpResponse(str)

def updatepositionHandler(request):
    id = request.POST.get("id")
    name = request.POST.get("name")
    list = position.objects.values("name").filter(id = id)
    for item in list:
        if name == item["name"]:
            return HttpResponse(returnResult.returnResult(1,"暂无修改!"))
        else:
            position.objects.filter(id = id).update(name=name)
            return HttpResponse(returnResult.returnResult(0, "修改成功!"))

#删除推荐位
def delposition(request):
    id = request.POST.get("id")
    position.objects.filter(id = id).delete()
    return HttpResponse(returnResult.returnResult(0, "删除成功!"))

#################推荐位内容管理
def positioncontent(request):
    # 查询推荐位内容表
    list1 = position_content.objects.values("positionid", "newsid", "id").order_by('-id')
    #查询推荐位表
    list2 = position.objects.values("name","id")
    # 查询新闻表
    list3 = news.objects.values("title", "thumb","id")

    # 数据处理
    dic = {}
    list = []
    for item1 in list1:
        for item2 in list2:
            if item1["positionid"] == item2["id"]:
                for item3 in list3:
                    if item1["newsid"] == item3["id"]:
                        dic = {"PositionContentId":item1["id"],"PositionName":item2["name"],"title":item3["title"],"thumb":item3["thumb"]}
                        list.append(dic)
    return render(request, "../templates/cmsadmain/positionContent/positioncontent.html", {"list":list})

#添加推荐内容
def addpositioncontent(request):
    positionid = request.POST.get("positionid")
    newsidlist = json.loads(request.POST.get("newsid"))
    for item in newsidlist:
        obj = position_content.objects.create(positionid=positionid,newsid=item)
    return HttpResponse(returnResult.returnResult(0, "添加成功!"))
#编辑推荐位内容
def updatepositioncontent(request):
    list = position.objects.values("id","name")
    dic = {}
    positionlist = []
    for item in list:
        dic = {"id":item["id"],"name":item["name"]}
        positionlist.append(dic)
    print(positionlist)
    str = json.dumps(positionlist)
    return HttpResponse(str)

def update_position_content_Handler(request):
    positionid = request.POST.get("positionid")
    position_content_id = request.POST.get("positioncontentid")
    print(positionid,position_content_id)
    #执行修改操作
    position_content.objects.filter(id=position_content_id).update(positionid=positionid)
    return HttpResponse(0)

#删除推荐位内容
def del_position_content(request):
    position_content_id = request.POST.get("id")
    print(position_content_id)
    position_content.objects.filter(id=position_content_id).delete()
    return HttpResponse(0)








###################后台登录
def login(request):
    return render(request, "../templates/cmsadmain/login/login.html")

def loginHandler(request):
    username = request.POST.get("username")
    pwd = request.POST.get("password")
    #查询数据库
    list = admain.objects.values("username","password").filter(username=username)
    if list.count != 0:
        for item in list:
            if pwd == item["password"]:
                #如果用户名密码通过验证,存入缓存中
                dic = {"user":username,"pwd":pwd}
                str = json.dumps(dic)
                request.session["user"] = str
                #同时更新用户登录时间
                admain.objects.filter(username=username).update(lasttime=datetime.now())
                return HttpResponse(returnResult.returnResult(0, "登录成功!"))
            else:
                return HttpResponse(returnResult.returnResult(1, "密码错误!"))
    else:
        return HttpResponse(returnResult.returnResult(2, "用户名不存在!"))

    return HttpResponse(0)


def clearImg(request):
    return render(request, "../templates/cmsadmain/clear/other.html")

def clearImgHandler(request):
    utils.clear()
    return render(request, "../templates/cmsadmain/clear/other.html")












