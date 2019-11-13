from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect

# Create your views here.

import hashlib
def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result

def LoginValid(func):
    def inner(request,*args,**kwargs):
        ## 获取cookie 和session  进行校验
        email = request.COOKIES.get("email")
        email_session = request.session.get("email")
        if email and email_session and email == email_session:
            return func(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/loginuser/login/")
    return inner


## 注册
def register(request):
    """
    完成注册功能
    :param request:  请求方式为  post
    :return:
    """
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        repassword = request.POST.get("repassword")
        ## 判空
        if email and password and repassword:
            ## 不为空
            if password != repassword:
                result = "密码不一致"
            else:
                ## 查库
                flag = LoginUser.objects.filter(email=email).exists()
                if flag:
                    result = "邮箱已经注册，去登录"
                else:
                    LoginUser.objects.create(email =email,username=email,password=setPassword(password))
                    result = "注册成功"
        else:
            result = "不能为空"
    return render(request,"register.html",locals())

## 登录
def login(request):

    if request.method == "POST":
        password = request.POST.get("password")
        email = request.POST.get("email")
        if password and email:
            user = LoginUser.objects.filter(email=email,password=setPassword(password)).first()
            if user:
                ## 存在  登录成功    跳转到 index页面  同时 设置 cookie 和session
                response = HttpResponseRedirect("/loginuser/index/")
                response.set_cookie("email",email)
                response.set_cookie("username",user.username)
                request.session["email"] = email
                return response
            else:
                result = "账号或者密码不正确"
        else:
            result = "参数为空"

    return render(request,"login.html",locals())


@LoginValid
def index(request):
    return render(request,"index.html")


def logout(request):

    response =  HttpResponseRedirect("/loginuser/login/")
    response.delete_cookie("email")
    del request.session["email"]
    return response