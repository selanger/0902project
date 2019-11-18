from django.shortcuts import render
from Seller.models import *
from Seller.views import setPassword
from django.http import HttpResponseRedirect

# Create your views here.
def LoginValid(func):
    def inner(request,*args,**kwargs):
        ## 判断
        ## 获取cookie 和 session
        print (request.COOKIES)
        cookie_email = request.COOKIES.get("email")
        session_email = request.session.get("email")
        cookie_username = request.COOKIES.get("username")
        if cookie_email and session_email and cookie_email == session_email:
            flag = LoginUser.objects.filter(username=cookie_username,email=cookie_email,user_type=1).exists()
            if flag:
                return func(request,*args,**kwargs)
            else:
                return HttpResponseRedirect("/buyer/login/")
        else:
            return HttpResponseRedirect("/buyer/login/")
    return inner


# @LoginValid
def index(request):
    goods_type = GoodsType.objects.all()
    return render(request,"buyer/index.html",locals())
def login(request):
    if request.method == "POST":
        password = request.POST.get("pwd")
        username = request.POST.get("username")
        if password and username:
            user = LoginUser.objects.filter(username=username, password=setPassword(password),user_type=1).first()
            if user:
                ## 存在  登录成功    跳转到 index页面  同时 设置 cookie 和session
                response = HttpResponseRedirect("/buyer/index/")
                response.set_cookie("email", user.email)
                response.set_cookie("username", user.username)
                response.set_cookie("user_id", user.id)
                request.session["email"] = user.email
                return response
            else:
                result = "账号或者密码不正确"
        else:
            result = "参数为空"

    return render(request,"buyer/login.html",locals())
## 注册
def register(request):

    if request.method == "POST":
        email = request.POST.get("email")
        user_name = request.POST.get("user_name")
        password = request.POST.get("pwd")
        repassword = request.POST.get("cpwd")
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
                    LoginUser.objects.create(email =email,username=user_name,password=setPassword(password))
                    result = "注册成功"
        else:
            result = "不能为空"

    return render(request,"buyer/register.html",locals())

## 登出
def logout(request):

    response =  HttpResponseRedirect("/buyer/login/")
    response.delete_cookie("email")
    response.delete_cookie("username")
    response.delete_cookie("user_id")
    del request.session["email"]
    return response

def base(request):
    return render(request,"buyer/base.html")