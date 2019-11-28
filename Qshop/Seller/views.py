from django.shortcuts import render
from django.http import HttpResponseRedirect
import hashlib
from .models import *
from django.core.paginator import Paginator
import logging
from Buyer.models import OrderInfo, PayOrder

collect = logging.getLogger("django")


# Create your views here.
## 加密
def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


## 登录装饰器
def LoginValid(func):
    def inner(request, *args, **kwargs):
        ## 获取cookie 和session  进行校验
        email = request.COOKIES.get("email")
        email_session = request.session.get("email")
        username = request.COOKIES.get("username")
        if email and email_session and email == email_session:
            flag = LoginUser.objects.filter(email=email_session, username=username, user_type=0).exists()
            if flag:
                return func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect("/seller/login/")
        else:
            return HttpResponseRedirect("/seller/login/")

    return inner


import datetime


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
        code = request.POST.get("code")
        ## 判空
        if email and password and repassword and code:
            ## 不为空
            if password != repassword:
                result = "密码不一致"
            else:
                ## 查库
                flag = LoginUser.objects.filter(email=email).exists()
                if flag:
                    result = "邮箱已经注册，去登录"
                else:
                    ## 获取验证码   然后比较验证码是否一致    从数据库中查询到验证码
                    validcode = ValidCode.objects.filter(user=email, code=code).order_by("-id").first()
                    if validcode:
                        ## 判断有效时间
                        ## 当前时间 - 创建的时间  》 2min  失效
                        now_time = datetime.datetime.now()
                        db_time = validcode.date  ## 创建时间
                        # print(now_time,db_time)
                        # t = (now_time - db_time).seconds   ## 当天
                        t = (now_time - db_time).total_seconds()
                        if t > 120:
                            result = "验证码失效，请重新获取！"
                        else:
                            LoginUser.objects.create(email=email, username=email,
                                                     password=setPassword(password), user_type=0)
                            result = "注册成功"
                    else:
                        result = "验证码不正确"
        else:
            result = "不能为空"
    return render(request, "seller/register.html", locals())


## 登录
def login(request):
    if request.method == "POST":
        password = request.POST.get("password")
        email = request.POST.get("email")
        if password and email:
            user = LoginUser.objects.filter(email=email, password=setPassword(password), user_type=0).first()
            if user:
                ## 存在  登录成功    跳转到 index页面  同时 设置 cookie 和session
                response = HttpResponseRedirect("/seller/index/")
                response.set_cookie("email", email)
                response.set_cookie("username", user.username)
                response.set_cookie("user_id", user.id)
                request.session["email"] = email
                ## 代表用户登录成功
                ## 日志：  xxx用户在xxxx时间登录成功
                collect.debug("%s is login" % user.username)

                return response
            else:
                result = "账号或者密码不正确"
        else:
            result = "参数为空"

    return render(request, "seller/login.html", locals())


from CeleryTask.tasks import Test, add, sendDingDing
from django.db.models import Sum

## 首页
@LoginValid
def index(request):
    user_id = request.COOKIES.get("user_id")
    user = LoginUser.objects.get(id = user_id)
    month = datetime.datetime.now().month


    #  1. 当月成交订单量
    #  当月成交了多少订单   订单详情多少条
    #  条件： 状态 -》  2 3 4 5
    count_order = OrderInfo.objects.filter(store=user,order_status__in=[2,3,4,5],order_id__order_date__month=month).count()

    ## 2. 当月的成交额
    ##当月的销售金额总和
    ## 状态为    2 3 4 5
    ## 卖家 -》 订单详情表 -》  小计之和
    ## 方法 计算当月的开始和结束的日期
    # start,end = getDay()    ### start 开始日期   end  结束日期
    # total_mount_money = OrderInfo.objects.filter(store=user,order_status__in=[2,3,4,5]).aggregate(Sum("goods_total_price")).get("goods_total_price__sum")
    total_mount_money = 0

    total_mount_money = OrderInfo.objects.filter(store=user,order_status__in=[2,3,4,5],order_id__order_date__month=month).aggregate(Sum("goods_total_price")).get("goods_total_price__sum")






    # 3. 销量最高的商品
    # 按照销售数量
    # 最多的商品
    ## 按照商品进行 分组   ->  sum(商品的数量)  goods_id
    ## 查询 数量最多的商品
    data = OrderInfo.objects.values("goods").annotate(Sum("goods_count")).order_by("-goods_count__sum").first().get("goods")
    goods_name = Goods.objects.get(id=data).goods_name
    print (data)
    ## annotate 分组  前面的  values  是一个分组条件
    # print(data)
    # max_data = {}
    # for one in data:
    #     print (one.get("goods_count__sum"))
    #     print (max_data.get("goods_count__sum"))
    #     if "goods" not in max_data:
    #         max_data["goods"] = one["goods"]
    #         max_data["goods_count__sum"] = one["goods_count__sum"]
    #     else:
    #         if one["goods_count__sum"] > max_data["goods_count__sum"]:
    #             max_data["goods"] = one["goods"]
    #             max_data["goods_count__sum"] = one["goods_count__sum"]
    #
    # print (max_data)
    # goods_name = Goods.objects.get(id = max_data["goods"]).goods_name


    # 4. 当月成交商品的总量
    # 成交单品数量的总和
    total_goods = OrderInfo.objects.filter(store=user,order_status__in=[2,3,4,5],order_id__order_date__month=month).aggregate(Sum("goods_count")).get("goods_count__sum")

    # print (total_goods)

    return render(request, "seller/index.html",locals())

import calendar
import datetime

def getDay():
    ## 计算当月的  开始 和 结束日期
    now_time = datetime.datetime.now()   ## 获取当前时间
    year = now_time.year    ## 当前的年
    month = now_time.month   ## 当前的月
    first_day = 1     ### 当前月的第一天
    last_day = calendar.monthrange(year,month)[1]
    first_day = datetime.date(year,month,first_day)
    last_day = datetime.date(year,month,last_day)

    return first_day,last_day




## 登出
def logout(request):
    response = HttpResponseRedirect("/seller/login/")
    response.delete_cookie("email")
    response.delete_cookie("username")
    response.delete_cookie("user_id")
    del request.session["email"]
    return response


## 商品列表
from django.core.cache import cache


@LoginValid
def goods_list(request, type, page=1):
    # user_id = request.COOKIES.get("user_id")
    # ##
    # user = LoginUser.objects.get(id =int(user_id))
    #
    # goods = Goods.objects.filter(goods_status = int(type),goods_store = user).order_by("-goods_number")
    # goods_obj = Paginator(goods,10)
    # goods_list = goods_obj.page(page)
    #
    ### 从缓存中获取数据
    data = cache.get("goods_list_data")
    goods_obj = cache.get("goods_obj")
    print(data)
    if data and goods_obj:
        goods_list = data

        ## 如果存在   直接获取
    else:
        ## 如果不存在 需要查询数据库 将查询结果增加到缓存中
        user_id = request.COOKIES.get("user_id")
        print(user_id)
        ##
        user = LoginUser.objects.get(id=int(user_id))

        goods = Goods.objects.filter(goods_status=int(type), goods_store=user).order_by("-goods_number")
        goods_obj = Paginator(goods, 10)
        goods_list = goods_obj.page(page)
        cache.set("goods_list_data", goods_list, 600)
        cache.set("goods_obj", goods_obj, 600)
        ####   设置缓存  缓存的名字（key)   缓存的value   缓存的有效时间

    return render(request, 'seller/goods_list.html', locals())


### 个人中心
@LoginValid
def PersonInfo(request):
    ## 查询用户的信息
    ## 登录的时候获取用户名  邮箱
    ## 查询
    user_id = request.COOKIES.get("user_id")
    user = LoginUser.objects.get(id=user_id)
    if request.method == "POST":
        print(request.POST)
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

    return render(request, "seller/personal_info.html", locals())


# 修改商品的状态
def goods_status(request, type, id):
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
    print(type)
    goods = Goods.objects.filter(id=int(id)).first()

    if type == "down":
        ##  将商品下架   修改  status= 0
        goods.goods_status = 0
        goods.save()

    else:
        ## 修改status = 1
        goods.goods_status = 1
        goods.save()

    # return HttpResponseRedirect("/goods_list/1/1/")
    url = request.META.get("HTTP_REFERER")  ## 获取请求的来源
    # print (url)
    return HttpResponseRedirect(url)


@LoginValid
def goods_add(request):
    # 获取商品信息
    # 保存商品信息
    goods_type = GoodsType.objects.all()  # 所有的类型
    if request.method == "POST":
        ##
        user_id = request.COOKIES.get("user_id")
        data = request.POST
        # print (data)
        goods = Goods()
        goods.goods_number = data.get("goods_number")
        goods.goods_name = data.get("goods_name")
        goods.goods_price = data.get("goods_price")
        goods.goods_count = data.get("goods_count")
        goods.goods_location = data.get("goods_location")
        goods.goods_safe_data = data.get("goods_safe_data")
        goods.goods_status = 1
        goods.goods_type_id = int(data.get("goods_type"))  ###获取到商品类型的id
        goods.goods_store_id = user_id  ## 店铺相关
        ## 图片
        goods.goods_picture = request.FILES.get("goodsfile")
        goods.save()

    return render(request, "seller/goodsadd.html", locals())


from django.http import JsonResponse
from sdk.sendDD import senddingding
import random


def get_code(request):
    result = {"code": 10000, "msg": ""}
    ### 发送请求  获取验证码
    """(content = "",isAtAll= True/False,"atMobiles":[])"""
    ### 随机4位数
    code = random.randint(1000, 9999)
    params = {
        "content": "您的验证码为%s,打死不要告诉别人!!!" % code,
        "atMobiles": [],
        "isAtAll": True
    }
    try:
        sendDingDing.delay(params)
        ### 保存验证码
        ValidCode.objects.create(code=code, user=request.GET.get("email"))

        result = {"code": 10000, "msg": "发送验证码成功"}
    except:
        result = {"code": 10001, "msg": "发送验证码失败"}
    return JsonResponse(result)


from django.http import HttpResponse, JsonResponse


def middletest(request, date):
    # print("我是 视图 ")
    # return HttpResponse("middletest")
    # def test():
    #     return HttpResponse("xxxxxxxxxxxx")
    # rep =  HttpResponse("middletest")
    # rep.render = test
    # return rep
    return JsonResponse({"name": "hello"})


def test(request):
    user = LoginUser.objects.create(email="hello@126.com", password=123123)
    return HttpResponse("sdss")


def cachetest(request, id):
    data = cache.get("name")
    if data:
        name = data
        print(name)
        cache.delete("name")
        data = cache.get("name")
        print(data)
    else:
        email = LoginUser.objects.filter(id=2).first()
        cache.set("name", email.email, 600)
        name = email.email
    return HttpResponse("name:%s" % name)


def get_goods(request):
    ## 获取商品的id
    goods_id = request.GET.get("id")
    data = cache.get(goods_id)
    if data:
        print("第一次")
        return HttpResponse(data)
    else:
        ## 查询商品
        print("第二次")
        goods = Goods.objects.filter(id=goods_id).first()
        if goods:
            cache.set(goods_id, goods.goods_name, 600)
        else:
            cache.set(goods_id, None, 600)
        return HttpResponse(goods.goods_name)


def update_goods(request):
    goods_id = request.GET.get("id")
    goods_name = request.GET.get("goods_name")
    goods = Goods.objects.get(id=goods_id)
    ## 修改数据
    ## 先判断数据是否在缓存中
    data = cache.get(goods_id)
    ## 如果在  删除缓存
    if data:
        print("第三次")
        cache.delete(goods_id)
    goods.goods_name = goods_name
    goods.save()
    return HttpResponse("保存数据完成")


### 后台订单页面
def order(request):
    ## 查询登录卖家用户所有订单
    user_id = request.COOKIES.get("user_id")
    ## 通过 user_id(卖家) -》  卖的商品（goods） -》 订单详情表
    ## 通过卖家id  -》 正向操作  -》 商品  ——》 订单
    # order_info = OrderInfo.objects.filter(store=LoginUser.objects.get(id = user_id)).all()

    ##
    ## 按照 订单状态，返回卖家所有的数据
    status = request.GET.get("status")  ## 获取订单状态   1  代表 获取未支付的订单
    order_info = OrderInfo.objects.filter(store=LoginUser.objects.get(id=user_id), order_status=status)

    return render(request, "seller/order.html", locals())


## 处理订单
def change_order(request):
    ## 修改状态
    ## 获取到   order_info 的id
    ## 操作的内容    确认发货  取消订单  修改
    order_id = request.GET.get("order_id")
    type = request.GET.get("type")
    ## 查询到订单详情
    order_info = OrderInfo.objects.get(id=order_id)
    if type == "tx":
        ### 提醒用户支付
        ## 发送邮件或者  发送短息
        ## 发钉钉
        params = {
            "content": "您的订单，请立即付款",
            "atMobiles": [],
            "isAtAll": True
        }

        sendDingDing.delay(params)
    elif type == "qx":
        ## 将订单详情状态  改为 取消
        ## 物理删除   逻辑删除
        ## 表中增加   on_delete int     0    未删除
        #                               1   删除
        pass
    elif type == "xg":
        ## 修改订单信息
        pass
    elif type == "fh":
        ## 确认发货
        order_info.order_status = 4
        order_info.save()

    url = request.META.get("HTTP_REFERER")  ## 获取请求的来源
    return HttpResponseRedirect(url)
