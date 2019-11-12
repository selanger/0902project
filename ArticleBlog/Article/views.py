from django.shortcuts import render
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from .models import *
from ArticleBlog.views import setPassword

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
                return response
            # else:
            #     return HttpResponseRedirect("/login")

        else:
            return HttpResponse("参数为空")

    return render(request,"login.html")

def logout(request):

    response =  HttpResponseRedirect("/login")
    response.delete_cookie("username")
    return response

