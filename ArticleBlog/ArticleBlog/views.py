from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from  Article.models import *
from django.core.paginator import Paginator

## 登录验证装饰器
def LoginVaild(func):
    def inner(request,*args,**kwargs):
        ##  需要校验用户的 cookie
        username = request.COOKIES.get("username")
        username_session = request.session.get("username")
        password_session = request.session.get("password")
        # print(password_session)
        # print(username_session)
        if username == username_session:
            return func(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/login/")
    return inner




## 首页
@LoginVaild
def index(request):
    """
    返回 最新的 6条数据
    返回图文推荐   7条数据
    返回点击排行  12条数据

    :param request:
    :return:
    """
    # print (request.COOKIES.get("username"))
    # username = request.COOKIES.get("username")   ## 获取cookie
    ### 校验cookie 校验cookie中是否有 username就可以
    # if username:
    ## 最新的 6条数据
    newarticle = Article.objects.order_by("-date")[:6]
    ## 返回图文推荐   7条数据
    recommendarticle = Article.objects.filter(recommend=1)[:7]
    ## 点击率
    clickarticle = Article.objects.order_by("-click")[:12]

    return render(request,"index.html",locals())
    # else:
    #     return HttpResponseRedirect("/login/")
@LoginVaild
def about(request):

    return render(request,"about.html")

def listpic(request):

    return render(request,"listpic.html")

def newslistpic(request,type,page=1):

    """
    获取指定类型的文章
    :param request: 请求对象
    :param page:    页码
    :param type:    类型    个人日记    学习笔记   技术文章
    :return:
    """

    page = int(page)
    ## 查询数据
    # article = Article.objects.all()
    article = Type.objects.filter(name=type).first().article_set.all()
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

def requsttest(request):
    # print (dir(request))
    # print(request.COOKIES)  ## 用户的身份
    # print(request.FILES)  ## 请求携带的文件   比如：  图片，文档，压缩包
    # print(request.META)     ## 请求的具体数据，包含所有的http请求信息
    # print(request.GET)   ## 获取get请求传递的参数
    # print (request.GET.get("name"))  ## 获取get请求参数中指定key的value
    # print(request.POST)      ## 获取post请求传递的参数
    # print(request.POST.get("name"))   ## 获取post请求传递参数中指定key的value
    # print(request.scheme)    ##   http 或者是  https
    # print(request.method)      ## 获取请求方式   POST  GET
    # print(request.path)    ## 请求的路径
    # print(request.body)   ## 请求的主体，放请求的内容  bytes 类型
    # print(request.META.get("OS"))   ## 请求来源使用的操作系统
    # print(request.META.get("HTTP_USER_AGENT"))   ##  浏览器的版本
    # print(request.META.get("HTTP_HOST"))    ## 请求的主机
    print(request.META.get("HTTP_REFERER"))    ## 请求的来源
    # print(request.META)







    return HttpResponse("请求demo")

def reqtest(request):

    ## 获取get请求的参数
    data = request.GET
    print(data)
    username = request.GET.get("username")
    print (username)

    return render(request,"reqtest.html")


def search(requst):
    ## 获取数据
    search_key = requst.GET.get("searchkey")
    article = []
    ## 判断是否空值
    if search_key:
        ## 如果有数据   查询数据库
        article=Article.objects.filter(title__icontains=search_key).all().values("title")
    ## 如果没有数据   返回页面
    return render(requst,"search.html",locals())

def reqpost(request):
    ## 接受用户的请求
    if request.method == "POST":
        ## 处理页面
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username)
        print(password)
    return render(request,"reqpost.html")

import hashlib
## 加密
def setPassword(password):
    ## 将password 通过md5 加密
    md5 = hashlib.md5()
    md5.update(password.encode())   ## 要求，传递的是一个  bytes类型
    result = md5.hexdigest()
    return result




from Article.form import UserForm
def register(request):
    ## 获取数据   完成注册功能
    register_form = UserForm()  ## 实例化
    if request.method == "POST":
        print(request.POST)
        # username = request.POST.get("username")
        # username = request.POST.get("name")
        # password = request.POST.get("password")
        ## 将接收到的数据，进行校验， 数据是否合法
        ## 校验用户名 不能为  admin@126.com
        ## 将获取到的数据  给到form表单类
        data = UserForm(request.POST)
        if data.is_valid():   ##判断校验是否成功
            ## 获取数据
            clean_data = data.cleaned_data   ## 获取经过校验的数据
            # print (clean_data)
            username = clean_data.get("name")
            password = clean_data.get("password")
            if username and password:
                ## 校验用户是否重复
                flag = User.objects.filter(name = username).exists()  ## 布尔类型
                ## 重复
                if not flag:
                    user = User()
                    user.name = username
                    user.password = setPassword(password)
                    user.save()
                    result = "注册成功"
                else:
                    result = "用户已存在"
            else:
                result = "用户名或密码为空"
        else:
            ## 校验不通过的
            # result = "校验不通过"
            print (data.errors)
            result = data.errors
    return render(request,"register.html",locals())



def ajaxtest(request):
    username = request.GET.get("username")
    if username:
        flag = User.objects.filter(name = username).exists()
        if flag:
            ## 存在
            result = "存在"
        else:
            result = "不存在"


    return render(request,"ajaxtest.html",locals())

from django.http import JsonResponse




def ajaxdemo(request):
    return render(request,"ajaxdemo.html")
def ajaxreq(request):
    """
    接受用户的请求     校验用户名  密码
        参数：   username    password
    处理请求
        查询数据库   查看指定用户名密码的用户是否存在
    返回响应
        存在或者 不存在
    :param request:
    :return:
    """
    print (request.GET)
    username = request.GET.get("username")
    password = request.GET.get("password")
    result = {"code":10000,"msg":""}

    if username and password:
        flag = User.objects.filter(name=username,password= setPassword(password)).exists()
        if flag:
            ## 存在
            result["msg"]="存在"
        else:
            result["msg"] = "不存在"
            result["code"] = 10001
    else:
        result["msg"] = "密码或者用户名为空"
        result["code"] = 10002
    # return HttpResponse("xxxxxxx")
    return JsonResponse(result)

## 提供注册页面
def ajaxregister(request):
    return render(request,"ajaxregister.html")

## 处理ajax 请求
def ajaxpost(request):

    result = {"code":10000,"msg":""}
    print(request.POST)
    ## 处理注册
    username = request.POST.get("username")
    password = request.POST.get("password")
    if username and password:
        ## 数据存在
        ## 判断用户名是否存在
        flag = User.objects.filter(name = username).exists()
        if flag:
            ## 存在
            result = {"code": 10002, "msg": "该用户已存在"}
        else:
            try:
                User.objects.create(name=username,password = setPassword(password))
                result = {"code": 10000, "msg": "注册成功"}
            except:
                result = {"code": 10003, "msg": "操作失败，联系管理员"}
    else:
        result = {"code": 10001, "msg": "参数为空"}
    return JsonResponse(result)





