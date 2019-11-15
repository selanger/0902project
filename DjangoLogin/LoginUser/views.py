from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.core.paginator import Paginator


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
                response.set_cookie("user_id",user.id)
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


def goods_list(request,type,page=1):
    """
    type  ->   0  获取  下架的商品
                1   获取上架的商品
    :param request:
    :param type:
    :param page:
    :return:
    """
    print (type)
    ## 查询   返回数据
    # goods = Goods.objects.all().order_by("-goods_number")
    goods = Goods.objects.filter(goods_status = int(type)).order_by("-goods_number")
    ##
    goods_obj = Paginator(goods,10)  ## 每页10条
    goods_list = goods_obj.page(page)
    return render(request,'goods_list.html',locals())
    # return render(request,"goods_ajax.html")
    # return render(request,"vuedemo.html")
    # return render(request,"gooslistvue.html")


def goods_list_api(request,type,page=1):
    """
    type  ->   0  获取  下架的商品
                1   获取上架的商品
    :param request:
    :param type:
    :param page:
    :return:
    """
    print (type)
    ## 查询   返回数据
    # goods = Goods.objects.all().order_by("-goods_number")
    goods = Goods.objects.filter(goods_status = int(type)).order_by("-goods_number")
    ##
    goods_obj = Paginator(goods,10)  ## 每页10条
    goods_list = goods_obj.page(page)
    # return render(request,'goods_list.html',locals())
    res = []
    for one in goods_list:
        res.append({
            "goods_number":one.goods_number,
            "goods_name":one.goods_name,
            "goods_price":one.goods_price,
            "goods_count":one.goods_count,
            "goods_location":one.goods_location,
            "goods_safe_data":one.goods_safe_data,
            "goods_pro_time":one.goods_pro_time,
            "goods_status":one.goods_status,
        })
    result = {
        "page_range":list(goods_obj.page_range),
        "data":res,
        "page":page,
    }
    return JsonResponse(result)

from django.views import View
import json
### 类视图
class GoodsView(View):

    def __init__(self):
        super(GoodsView, self).__init__()
        self.result = {
            "methods": "get请求",
            "data": "",
            "version": "v1",
            "msg":"请求成功"
        }
        self.goods_obj = Goods

    ##处理get请求
    def get(self,request):
        id = request.GET.get("id")
        if id:
            ## 查找指定id的数据
            goods = self.goods_obj.objects.get(id=id)
            data = {
                "goods_number": goods.goods_number,
                "goods_name": goods.goods_name,
                "goods_price": goods.goods_price,
                "goods_count": goods.goods_count,
                "goods_location": goods.goods_location,
                "goods_safe_data": goods.goods_safe_data,
                "goods_pro_time": goods.goods_pro_time,
                "goods_status": goods.goods_status,
            }


        else:
            goods = self.goods_obj.objects.all()
            data = []
            for one in goods:
                data.append({
                    "goods_number": one.goods_number,
                    "goods_name": one.goods_name,
                    "goods_price": one.goods_price,
                    "goods_count": one.goods_count,
                    "goods_location": one.goods_location,
                    "goods_safe_data": one.goods_safe_data,
                    "goods_pro_time": one.goods_pro_time,
                    "goods_status": one.goods_status,
                })

        self.result["data"] = data
        return JsonResponse(self.result)

    ##处理post请求
    def post(self,request):
        ## 获取数据，保存数据
        data = request.POST
        goods = Goods()
        goods.goods_number = data.get("goods_number")
        goods.goods_name = data.get("goods_name")
        goods.goods_price = data.get("goods_price")
        goods.goods_count = data.get("goods_count")
        goods.goods_location = data.get("goods_location")
        goods.goods_safe_data = data.get("goods_safe_data")
        goods.save()

        # result = {"methods": "post请求"}
        self.result["methods"] = "post"
        self.result["data"] = {"id":goods.id}
        self.result["msg"] ="数据添加成功"
        return JsonResponse(self.result)
    ## 处理put请求
    def put(self,request):
        ## 获取数据  进行更新
        # data = request.POST    put 请求的数据，不在request.GET或者POST中
        data = request.body     ## bytes 类型
        data = json.loads(data.decode())
        id = data.get("id")
        goods_name = data.get("goods_name")
        ## 更新  操作   将指定id的商品名字修改
        Goods.objects.filter(id=id).update(goods_name=goods_name)
        self.result = {"methods": "put请求"}
        self.result["data"]={"id":id}
        self.result["msg"] = "数据修改完成"

        return JsonResponse(self.result)
    ## 处理delete请求
    def delete(self,request):
        data = request.body
        data = json.loads(data.decode())
        id = data.get("id")
        ## 删除
        Goods.objects.filter(id = id).delete()
        self.result = {"methods": "delete请求"}
        self.result["data"]={"id":id}
        self.result["msg"] = "数据删除完成"
        return JsonResponse(self.result)

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

import random
def add_goods(request):
    ## 增加100 条
    goods_name = "芹菜、西芹、菠菜、香菜、茼蒿、茴香、生菜、苋菜、莴苣、葱、香葱、分葱、胡葱、楼子葱、蒜头、洋葱头、韭菜、韭葱、黄瓜、丝瓜、冬瓜、菜瓜、苦瓜、南瓜、栉瓜、西葫芦、葫芦、瓠瓜、节瓜、越瓜、笋瓜、佛手瓜"
    goods_name = goods_name.split("、")
    address = "北京市，天津市，上海市，重庆市，河北省，山西省，辽宁省，吉林省，黑龙江省，江苏省，浙江省，安徽省，福建省，江西省，山东省，河南省，湖北省，湖南省，广东省，海南省，四川省，贵州省，云南省，陕西省，甘肃省，青海省，台湾省"
    address = address.split("，")
    ##
    # for i in range(100):
    for i,j in enumerate(range(100),1):  ## i 是索引
        goods = Goods()
        goods.goods_number = str(i).zfill(5)  ## 返回指定长度的字符串   长度是5
        goods.goods_name = random.choice(address) + random.choice(goods_name)   ###从列表中随机取一个值
        goods.goods_price = random.random()*100    ## 0到1 的小数
        goods.goods_count = random.randint(1,100)
        goods.goods_location = random.choice(address)
        goods.goods_safe_data = random.randint(1,12)
        goods.save()

    return HttpResponse("增加数据")

from rest_framework import viewsets
from .serializer import GoodsSerializer,UserSerializer
class GoodsViewsSet(viewsets.ModelViewSet):
    queryset = Goods.objects.all()    ## 固定的写法
    serializer_class = GoodsSerializer          ##  过滤器



class UserViewsSet(viewsets.ModelViewSet):
    queryset = LoginUser.objects.all()    ## 固定的写法
    serializer_class = UserSerializer          ##  过滤器


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

    return render(request,"personal_info.html",locals())


