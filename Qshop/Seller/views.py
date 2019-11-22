from django.shortcuts import render
from django.http import HttpResponseRedirect
import hashlib
from .models import *
from django.core.paginator import Paginator
# Create your views here.
## 加密
def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result
## 登录装饰器
def LoginValid(func):
    def inner(request,*args,**kwargs):
        ## 获取cookie 和session  进行校验
        email = request.COOKIES.get("email")
        email_session = request.session.get("email")
        username = request.COOKIES.get("username")
        if email and email_session and email == email_session:
            flag = LoginUser.objects.filter(email=email_session,username=username,user_type=0).exists()
            if flag:
                return func(request,*args,**kwargs)
            else:
                return HttpResponseRedirect("/seller/login/")
        else:
            return HttpResponseRedirect("/seller/login/")
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
                    ## 获取验证码   然后比较验证码是否一致
                    ## 从数据库中查询到验证码
                    LoginUser.objects.create(email =email,username=email,
                                             password=setPassword(password),user_type=0)
                    result = "注册成功"
        else:
            result = "不能为空"
    return render(request,"seller/register.html",locals())
## 登录
def login(request):

    if request.method == "POST":
        password = request.POST.get("password")
        email = request.POST.get("email")
        if password and email:
            user = LoginUser.objects.filter(email=email,password=setPassword(password),user_type=0).first()
            if user:
                ## 存在  登录成功    跳转到 index页面  同时 设置 cookie 和session
                response = HttpResponseRedirect("/seller/index/")
                response.set_cookie("email",email)
                response.set_cookie("username",user.username)
                response.set_cookie("user_id",user.id)
                request.session["email"] = email
                return response
            else:
                result = "账号或者密码不正确"
        else:
            result = "参数为空"

    return render(request,"seller/login.html",locals())

## 首页
@LoginValid
def index(request):
    return render(request,"seller/index.html")
## 登出
def logout(request):

    response =  HttpResponseRedirect("/seller/login/")
    response.delete_cookie("email")
    response.delete_cookie("username")
    response.delete_cookie("user_id")
    del request.session["email"]
    return response
## 商品列表
@LoginValid
def goods_list(request,type,page=1):
    user_id = request.COOKIES.get("user_id")
    ##
    user = LoginUser.objects.get(id =int(user_id))

    goods = Goods.objects.filter(goods_status = int(type),goods_store = user).order_by("-goods_number")
    goods_obj = Paginator(goods,10)
    goods_list = goods_obj.page(page)
    return render(request,'seller/goods_list.html',locals())
### 个人中心
@LoginValid
def PersonInfo(request):
    ## 查询用户的信息
    ## 登录的时候获取用户名  邮箱
    ## 查询
    user_id = request.COOKIES.get("user_id")
    user = LoginUser.objects.get(id = user_id)
    if request.method == "POST":
        print (request.POST)
        data = request.POST
        ## 更新数据
        user.username = data.get("username")
        user.phone_number = data.get("phone_number")
        user.age = data.get("age")
        user.gender = data.get("gender")
        user.address = data.get("address")
        # user.photo = data.get("photo")

        if request.FILES.get("photo"):
            user.photo = request.FILES.get("photo")
        user.save()
        user = LoginUser.objects.get(id=user_id)

    return render(request,"seller/personal_info.html",locals())


# 修改商品的状态
def goods_status(request,type,id):
    """
    商品id
    操作： 内容  上架  下架
        获取  type  down   下架操作
                      up   上架操作
        修改商品的状态
    :param request:
    :return:
    """
    print(id)
    print (type)
    goods = Goods.objects.filter(id = int(id)).first()

    if type =="down":
        ##  将商品下架   修改  status= 0
        goods.goods_status = 0
        goods.save()

    else:
        ## 修改status = 1
        goods.goods_status = 1
        goods.save()

    # return HttpResponseRedirect("/goods_list/1/1/")
    url = request.META.get("HTTP_REFERER")  ## 获取请求的来源
    print (url)
    return HttpResponseRedirect(url)

@LoginValid
def goods_add(request):
    # 获取商品信息
    # 保存商品信息
    goods_type = GoodsType.objects.all()  #  所有的类型
    if request.method == "POST":
        ##
        user_id = request.COOKIES.get("user_id")
        data = request.POST
        print (data)
        goods = Goods()
        goods.goods_number = data.get("goods_number")
        goods.goods_name = data.get("goods_name")
        goods.goods_price = data.get("goods_price")
        goods.goods_count = data.get("goods_count")
        goods.goods_location = data.get("goods_location")
        goods.goods_safe_data = data.get("goods_safe_data")
        goods.goods_status = 1
        goods.goods_type_id = int(data.get("goods_type"))     ###获取到商品类型的id
        goods.goods_store_id = user_id     ## 店铺相关
        ## 图片
        goods.goods_picture = request.FILES.get("goodsfile")
        goods.save()

    return render(request,"seller/goodsadd.html",locals())

from django.http import JsonResponse
from sdk.sendDD import senddingding
import random
def get_code(request):
    result = {"code":10000,"msg":""}
    ### 发送请求  获取验证码
    """(content = "",isAtAll= True/False,"atMobiles":[])"""
    ### 随机4位数
    code = random.randint(1000,9999)
    params = {
        "content":"您的验证码为%s,打死不要告诉别人!!!" % code,
        "atMobiles":[],
        "isAtAll":True
    }
    try:
        senddingding(params)
        result = {"code": 10000, "msg": "发送验证码成功"}
    except:
        result = {"code": 10001, "msg": "发送验证码失败"}
    return JsonResponse(result)
