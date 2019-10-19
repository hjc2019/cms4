import math
from django.shortcuts import render
from cmsadmain.models import *
from django.http import HttpResponse
from  common import returnResult
from  cms import settings
from  common import utils
import string
import json
from django.template.defaultfilters import striptags
# Create your views here.

def index(request):
    nav=menu.objects.filter(menustate="开启",menutype="前台栏目").values()
    count = settings.PAGES["everypages"]
    current_page = request.GET.get("page")
    if current_page == None:
        current_page = 1
    newsList = news.objects.all()
    List = news.objects.all()[((int(current_page)-1)*count):int(current_page)*count]
    #分页显示新闻信息
    allcount = newsList.count()       #数据总条数
    pagecount = math.ceil(allcount / count)      #总页数
    pageRange = utils.viewpage(current_page,allcount)     #调用函数得到显示的按钮数
    ranklist = news.objects.values("id","title").order_by('-num')[0:5]              #查找阅读量前五的新闻
    #遍历ranklist给每一个新闻加上rankid
    i = 1
    for item in ranklist:
        item["rankid"] = i
        i+=1
    #获取信息显示的部分内容
    for i in List:
        newscontent = news_content.objects.values("content").filter(newsid=i.id)
        i.content = striptags(newscontent[0]["content"])
    # 获取右侧广告栏的新闻
    rightList = positionNews("右侧广告位",3)
    #获取首页大图的广告新闻
    bigImg = positionNews("首页大图",5)
    # 遍历bigImg给每一个新闻加上index
    index = 1
    for item in bigImg:
        item["index"] = index
        index += 1
    #获取小图推荐的广告新闻
    smallImg = positionNews("小图推荐",3)
    # 遍历bigImg给每一个新闻加上index
    n = 1
    for item in smallImg:
        item["index"] = n
        n += 1
    context={
        "ranklist": ranklist,
        "pageRange":pageRange,
        "nav":nav,
        "newslist":List,
        "current_page":int(current_page),
        "pagecount":pagecount,
        "rightposition":rightList,
        "bigImg":bigImg,
        "smallImg":smallImg,
    }
    return render(request, 'cmsindex/index.html',context)

# 文章详情
def articleContent(request):
    nav = menu.objects.filter(menustate="开启", menutype="前台栏目").values()
    articleId=request.GET.get("articleId")  #获取传过来的文章id
    articleList=news.objects.values("title","time","num").get(id=articleId)    #通过文章id查询文章信息
    #每次点击进来的时候阅读量+1
    addnum=articleList["num"]
    save=news.objects.filter(id=articleId).update(num=addnum+1)
    content=news_content.objects.values("content").filter(newsid=articleId)    #获取文章内容
    ranklist = news.objects.values("id", "title").order_by('-num')[0:5]  # 查找阅读量前五的新闻
    # 遍历ranklist给每一个新闻加上rankid
    i = 1
    for item in ranklist:
        item["rankid"] = i
        i += 1
    # 获取右侧广告栏的新闻
    rightList = positionNews("右侧广告位", 3)
    context={
        "ranklist":ranklist,
        "save":save,
        "articleList":articleList,
        "content":content[0],
        "nav":nav,
        "rightposition":rightList
    }
    return render(request, 'cmsindex/articleContent.html', context)

# 分类文章
def articleClassifiedList(request):
    nav = menu.objects.filter(menustate="开启", menutype="前台栏目").values()
    navid=request.GET.get("navid")
    classifiedArticle=news.objects.filter(catid=navid).all()
    ranklist = news.objects.values("id", "title").order_by('-num')[0:5]  # 查找阅读量前五的新闻
    # 遍历ranklist给每一个新闻加上rankid
    i = 1
    for item in ranklist:
        item["rankid"] = i
        i += 1
    # 获取右侧广告栏的新闻
    rightList = positionNews("右侧广告位", 3)
    # 获取信息显示的部分内容
    for i in classifiedArticle:
        newscontent = news_content.objects.values("content").filter(newsid=i.id)
        i.content = i.content = striptags(newscontent[0]["content"])
    context={
        "classifiedArticle":classifiedArticle,
        "ranklist": ranklist,
        "nav":nav,
        "rightposition": rightList
    }
    return render(request, 'cmsindex/articleClassfiedList.html', context)


# 获取广告栏的新闻
def positionNews(str,count):
    # 广告位的id
    PositionId = position.objects.values("id").filter(name=str)
    # 倒序查询该id下的3条新闻
    newsIdList = position_content.objects.values("newsid").order_by("-id").filter(positionid=PositionId[0]["id"])[0:count]
    List = []
    for item in newsIdList:
        obj = news.objects.values("id", "title", "thumb").filter(id=item["newsid"])
        List.append(obj[0])
    return List

