from django.http import HttpResponse
from django.shortcuts import render
from  Article.models import *
from django.core.paginator import Paginator


## 首页
def index(request):
    """
    返回 最新的 6条数据
    返回图文推荐   7条数据
    返回点击排行  12条数据

    :param request:
    :return:
    """
    ## 最新的 6条数据
    newarticle = Article.objects.order_by("-date")[:6]
    ## 返回图文推荐   7条数据
    recommendarticle = Article.objects.filter(recommend=1)[:7]
    ## 点击率
    clickarticle = Article.objects.order_by("-click")[:12]

    return render(request,"index.html",locals())

def about(request):
    return render(request,"about.html")

def listpic(request):
    return render(request,"listpic.html")

def newslistpic(request,page=1):
    page = int(page)
    ## 查询数据
    article = Article.objects.all()
    ## 返回数据
    paginator = Paginator(article,6)
    page_obj = paginator.page(page)

    ## 首先获取当前页数    start = num -2  end = num + 3      3 4 5 6 7
    ## range(3,8)  ->
    ##   range(start,end)

    ##   先返回5个
    # page_range = paginator.page_range[:5]
    ## 控制  start 和 end
    #  获取当前页
    number = page_obj.number
    start = number -3
    end = number + 2
    if number <=2:
        start = 0
        end = 5
    if number >= paginator.num_pages - 2:
        end = paginator.num_pages
        start = end - 5
    page_range = paginator.page_range[start:end]
    return render(request,"newslistpic.html",locals())
def base(request):
    return render(request,"base.html")

## 文章详情
def articleDetails(request,id):
    """
    查询数据 查询指定文章的详情
        获取  文章的id
    查询文章详情的数据
    :param request:
    :return:  返回文章  返回指定文章的详情
    """
    id = int(id)
    article = Article.objects.filter(id=id).first()
    article.click += 1
    article.save()

    return render(request,"articledetails.html",locals())


def fytest(request):
    ### 分页的方法
    article = Article.objects.all().order_by("id")
    # print (aricle)

    paginator = Paginator(article,5)   ## 设置每一页显示多少条数据  返回是一个 paginator对象
    # # print (paginator)
    # print (paginator.count)   ## 数据总条数
    # print (paginator.num_pages)  ## 总页数   102/5
    # print (paginator.page_range)    ### 页码的返回    range(start,end)

    page_obj = paginator.page(10)   ### 指定页码的一个对象  <Page 2 of 21>
    # print (page_obj)    ##
    # print (type(page_obj))
    # for one in page_obj:   ## one  是每一页的数据
    #     print (one)
    #     print (one.title)

    # print(page_obj.number)  ## 当前页码

    # print (page_obj.has_next())  ## 判断是否有下一页  返回 布尔
    # print (page_obj.has_previous())  ## 判断是否有 上一页
    # print (page_obj.has_other_pages())  ## 判断是否有其他页

    # print(page_obj.next_page_number())  ## 下一页的页码
    # print(page_obj.previous_page_number())  ## 上一页的页码

    return HttpResponse("fenye test")




