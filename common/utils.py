import math
import os
from cmsadmain import models
import re
from cms import settings

#判断文件大小
def getsize(size,format = 'kb'):
    p = 0
    if format == "kb":
        p = 1
    elif format == "mb":
        p = 2
    elif format == "gb":
        p = 3
    size /= math.pow(1024,p)
    return "%0.2f"%size

#判断指定的文件夹存不存在，不存在就创建
def creatDir(dir):
    '''
    判断指定的文件夹存不存在
    :param dir:
    :return:
    '''
    dirlist = dir.split("/")
    for i,name in enumerate(dirlist):
        itemdir = os.path.join(os.getcwd(),name)
        #判断当前文件夹是否存在
        if not os.path.exists(itemdir):
            os.mkdir(itemdir)
        #如果当前文件夹存在并且不是最后一层
        if i < len(dirlist)-1:
            dirlist[i+1] = os.path.join(itemdir,dirlist[i+1])


#清理工作，清理文章内容多余的图片
def clear():
    #获取数据库新闻内容表中的所有内容
    contentList = models.news_content.objects.values("content")
    resultList = []
    #定义正则匹配表达式
    pattern = '(images\/([^\"]*))+'
    #遍历内容匹配字符串,匹配成功存入列表resultList
    for item in contentList:
        result = re.findall(pattern,item["content"])
        if result != []:
            for i in result:
                resultList.append(i[1])
    print(resultList)

    #获取/static/images/下的所有图片
    path = os.path.join(os.getcwd(),"static/images")
    imgList = os.listdir(path)

    #遍历imgList,如果imgList中的图片包含在resulrList中则保留，不包含就删除
    for item1 in imgList:
        if item1 not in resultList:
            path1 = os.path.join(path,item1)
            os.remove(path1)
    return contentList

#分页
def viewpage(current_page,allcount):
    count = settings.PAGES["everypages"]  # 每页5条信息
    pagecount = math.ceil(allcount / count)   #按每页五条所分的总页数
    # 每页显示的按钮数
    btncount = settings.PAGES["everybtns"]
    if int(current_page) == 1:
        pageRange = range(int(current_page), int(current_page) + btncount)
    elif int(current_page) == pagecount:
        pageRange = range(int(current_page) - (btncount - 1), int(current_page) + 1)
    else:
        pageRange = range(int(current_page) - 1, int(current_page) + (btncount - 1))
    return pageRange