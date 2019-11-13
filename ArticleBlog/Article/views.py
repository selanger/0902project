from django.shortcuts import render
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from .models import *
from ArticleBlog.views import setPassword
from django.core.paginator import Paginator


# Create your views here.
def checkuser(request):
    result ={"code":10000,"msg":""}
    ##校验用户名是否存在
    username= request.GET.get("username")
    if username:
        ## 存在
        user = User.objects.filter(name=username).first()
        if user:
            # 有数据
            result = {"code": 10001, "msg": "账号不可用"}
        else:
            # 没有数据
            result = {"code": 10000, "msg": "账号可用"}
    else:
        result = {"code": 10001, "msg": "参数为空"}
    return JsonResponse(result)

def login(request):
    ##  登录
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            user = User.objects.filter(name = username,password = setPassword(password)).first()
            if user:
                ## 登录成功
                # return HttpResponse("登录成功")
                # return HttpResponseRedirect("/index")
                response = HttpResponseRedirect("/index")
                ##  设置cookie
                response.set_cookie("username",username,max_age=1200)
                response.set_cookie("password",password)
                request.session["username"] = username
                request.session["password"] = password
                return response
            # else:
            #     return HttpResponseRedirect("/login")

        else:
            return HttpResponse("参数为空")

    return render(request,"login.html")

def logout(request):

    response =  HttpResponseRedirect("/login")
    response.delete_cookie("username")
    ## 删除session
    ##  {“name" :dsfsfsfds}
    del request.session["username"]
    return response

def searchtitle(request):
    search_key = request.POST.get("keyboard")
    if search_key:
        article = Article.objects.filter(title__icontains=search_key).order_by("-date")

    paginator = Paginator(article,6)
    page_range = paginator.page_range
    page_obj = paginator.page(1)
    #
    # number = page_obj.number
    # start = number -3
    # end = number + 2
    # if number <=2:
    #     start = 0
    #     end = 5
    # if number >= paginator.num_pages - 2:
    #     end = paginator.num_pages
    #     start = end - 5
    # page_range = paginator.page_range[start:end]

    return render(request,"newslistpic.html",locals())


