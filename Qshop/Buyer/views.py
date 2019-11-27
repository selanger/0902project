from django.db.models import Q
from django.shortcuts import render
from Seller.models import *
from Seller.views import setPassword
from django.http import HttpResponseRedirect,JsonResponse
from .models import *

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


from django.views.decorators.cache import cache_page
# @LoginValid
# @cache_page(120)
def index(request):
    # goods_type = GoodsType.objects.all()
    # return render(request,"buyer/index.html",locals())
    """
    - 如果每个类型下面有多条数据	展示4条
    - 如果类型没有数据，不展示
    :param request:
    :return:
        返回只有商品的类型
        html中遍历 类型
        返回商品 指定条数的商品
    """
    goods_type = GoodsType.objects.all()
    types = []
    for one in goods_type:   ## one 每一个类型的对象
        goods = one.goods_set.order_by("-goods_price")   ## 排序
        ## goods 可以为空的queryset   也可能   大于四条 通过切片进行截取
        if len(goods) > 4:
            goods_all = goods[:4]
            types.append({"type":one,"goods":goods_all})
        elif len(goods) > 0 and len(goods) <= 4:
            goods_all = goods
            types.append({"type": one, "goods": goods_all})

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
def goodslist(request):
    ## 通过get请求 获取类型
    ## 通过get请求传值     key -》 keywords   value -》 goodsType 中id

    """
    keywords  查询条件
        查看更多中   代表  商品类型的id
        搜索中  代表 搜索的关键字
    req_type 代表  是查看更多    findall
                    搜索      search
    :param request:
    :return:
    """
    req_type = request.GET.get("req_type")
    keywords = request.GET.get("keywords")
    if req_type == "findall":  ##  查看指定类型的的商品
        goods_type = GoodsType.objects.get(id = int(keywords))
        ## 获取到类型下面的所有数据
        goods_all = goods_type.goods_set.all()
        print(goods_all)
    ## 搜索 进行模糊查询
    else:
        ## 从搜索进来
        ## 进行模糊查询
        goods_all = Goods.objects.filter(goods_name__icontains=keywords).all()

    goods_new = goods_all.order_by("-goods_pro_time")[:2]
    return render(request,"buyer/goods_list.html",locals())

def goodsdetail(request,goods_id):
    ## 获取商品的id
    ## 查询商品
    ## 返回商品数据
    goods = Goods.objects.get(id=int(goods_id))
    ## 当前使用的地址
    address = UserAddress.objects.filter(status = 1).first()




    return render(request,'buyer/detail.html',locals())

## 个人中心
@LoginValid
def person_info(request):
    return render(request,"buyer/person_info.html")

## 购物车
@LoginValid
def cart(request):
    ## 登录用户的购物车
    user_id = request.COOKIES.get("user_id")
    ## 查找用户的购物车内容，  按照时间逆序
    ## 查找用户的所有的待支付的购物车内容
    ## 查询到待支付的订单号
    order_numer = PayOrder.objects.filter(order_user=LoginUser.objects.get(id=user_id),
                                          order_status=1).values("order_number")

    # cart = Cart.objects.filter(cart_user=LoginUser.objects.get(id=user_id)).all().order_by("-id")

    cart = Cart.objects.filter(Q(payorder__in=order_numer) | Q(payorder = "0")).all().order_by("-id")
    print (cart)
    return render(request,"buyer/cart.html",locals())

# 订单页面
@LoginValid
def user_center_order(request):
    ## 返回登录用户订单
    user_id = request.COOKIES.get("user_id")

    payorder = PayOrder.objects.filter(order_user=LoginUser.objects.get(id=user_id)).all().order_by("order_status")
    return render(request,"buyer/user_center_order.html",locals())

## 收货地址
@LoginValid
def user_center_site(request):
    user_id = request.COOKIES.get("user_id")
    user = LoginUser.objects.get(id = user_id)
    ## get 请求  返回页面  和已经有的地址
    ## post请求  保存新的地址
    if request.method == "POST":
        data = request.POST
        ## 获取数据，保存数据
        useraddress = UserAddress()
        useraddress.user = user
        useraddress.address = data.get("address")
        useraddress.phone = data.get("phone")
        useraddress.name = data.get("name")
        useraddress.status = 0
        useraddress.save()
    ## 登录用户的所有地址
    user_address_all = UserAddress.objects.filter(user=user).all()
    return render(request,"buyer/user_center_site.html",locals())

### 修改地址
def updateAddress(request):
    if request.method == "POST":
        print (request.POST)
        address_id = request.POST.get("address")
        print (address_id)
        ## 完成修改地址状态
        ## 2. 修改之前选中的地址状态
        user_address = UserAddress.objects.filter(status = 1).first()
        user_address.status = 0
        user_address.save()

        ## 1. 修改选中的地址的状态
        user_address = UserAddress.objects.filter(id = address_id).first()
        user_address.status = 1
        user_address.save()

    return HttpResponseRedirect("/buyer/user_center_site/")




import time
@LoginValid
def place_order(request):
    ## 生成订单
    ## 获取 商品id
    ## 获取 商品购买数量
    ## 保存订单
    print (request.GET)
    user_id = request.COOKIES.get("user_id")
    goods_id = request.GET.get("goods_id")
    goods_count = request.GET.get("goods_count")
    address_id = request.GET.get("address_id")
    goods = Goods.objects.get(id=int(goods_id))
    ## 保存数据
    ## 保存订单
    payorder = PayOrder()
    payorder.order_number = str(time.time()).replace(".","")
    payorder.order_status = 1  ## 未支付
    payorder.order_total = goods.goods_price * int(goods_count)
    payorder.order_user = LoginUser.objects.get(id = int(user_id))
    payorder.order_address = address_id
    payorder.save()
    ## 保存订单详情

    orderinfo = OrderInfo()
    orderinfo.order_id = payorder
    orderinfo.goods = goods
    orderinfo.goods_price = goods.goods_price
    orderinfo.goods_count = int(goods_count)
    orderinfo.goods_total_price =  goods.goods_price * int(goods_count)
    orderinfo.save()
    ## 查询都选中的地址
    address = UserAddress.objects.get(id = address_id)
    return render(request,"buyer/place_order.html",locals())


@LoginValid
def place_order_more(request):
    # 生成订单
    # 获取 购物车id
    user_id = request.COOKIES.get("user_id")
    data = request.POST   ## 字典
    data = data.items()    ### 生成器
    res = []   ## 选中的购物车id
    for key,value in data:
        if key.startswith("cartid"):
            res.append(value)
    user = LoginUser.objects.get(id = user_id)

    ## 生成订单  2件    1笔订单   2笔订单详情
    if len(res) != 0:
        payorder = PayOrder()
        payorder.order_number = str(time.time()).replace(".", "")
        payorder.order_status = 1  ## 未支付
        payorder.order_total = 0
        payorder.order_user = user
        payorder.save()

        order_total = 0
        order_count = 0
        ## 订单详情
        for c_id in res:  ## c_id  购物车id
            cart = Cart.objects.get(id = c_id)
            goods = cart.goods
            orderinfo = OrderInfo()
            orderinfo.order_id = payorder
            orderinfo.goods = goods
            orderinfo.goods_price = goods.goods_price
            orderinfo.goods_count = cart.goods_number
            orderinfo.goods_total_price = cart.goods_total
            orderinfo.save()
            order_total += cart.goods_total
            order_count += cart.goods_number

            cart.payorder = payorder.order_number
            cart.save()


        payorder.order_total = order_total
        payorder.save()

    return render(request,"buyer/place_order.html",locals())




from django.http import HttpResponse
from Qshop.settings import alipay
def payorderAli(request):
    ## 完成付款
    ## 实例化订单
    order_id = request.GET.get("order_id")   ### 订单id
    payorder = PayOrder.objects.get(id=order_id)
    order_string = alipay.api_alipay_trade_page_pay(
        subject='生鲜交易',  ## 交易主题
        out_trade_no= payorder.order_number,  ## 订单号
        total_amount= str(payorder.order_total),  ## 交易总金额  需要是一个string
        return_url="http://127.0.0.1:8000/buyer/payresult/",  ## 返回的路径
        notify_url=None  ## 通知路径
    )
    ## 发送请求
    ## 构建一个请求url
    result = "https://openapi.alipaydev.com/gateway.do?" + order_string
    return HttpResponseRedirect(result)

def payresult(request):
    out_trade_no = request.GET.get("out_trade_no")   ### 订单号
    payorder = PayOrder.objects.get(order_number=out_trade_no)
    payorder.order_status = 2
    payorder.save()

    return render(request,"buyer/payresult.html",locals())

### 添加购物车
@LoginValid
def add_cart(request):
    """
     保存数据到 购物车表
    :param request:
        商品id
        商品的数量
    :return:
    """

    goods_id = request.POST.get("goods_id")
    count = request.POST.get("count",1)
    user_id = request.COOKIES.get("user_id")
    goods = Goods.objects.get(id = goods_id)
    user = LoginUser.objects.get(id=user_id)
    ## 增加商品数量
    ## 条件：  1. 用户  2. 商品   3.购物内容的状态
    has_cart = Cart.objects.filter(goods=goods,cart_user=user,payorder='0').first()
    if has_cart:
        ##已经有
        has_cart.goods_number += int(count)
        has_cart.goods_total += int(count) * goods.goods_price
        has_cart.save()
    else:
        ## 没有
        ## 保存
        cart = Cart()
        cart.goods = goods
        cart.goods_number = int(count)
        cart.cart_user = user
        cart.goods_total = int(count) * goods.goods_price
        cart.save()
    return JsonResponse({"code":10000,"msg":"添加购物成功"})


## 删除购物车内容
def delete_cart(request):
    ### 获取购物车id
    cart_id = request.GET.get("cart_id")
    Cart.objects.filter(id =cart_id).delete()
    return HttpResponseRedirect("/buyer/cart/")

def change_cart(reuqest):
    result = {"code":10001,"msg":""}
    ### 获取购物车id
    ## 每次请求，数量加1
    cart_id = reuqest.GET.get("cart_id")
    type = reuqest.GET.get("type")  ###   add(加)   reduce(减）
    cart = Cart.objects.filter(id = cart_id).first()
    if type == "add":
        cart.goods_number += 1
        cart.goods_total += cart.goods.goods_price
    else:
        cart.goods_number -= 1
        cart.goods_total -= cart.goods.goods_price
    try:
        cart.save()
        data = {
            "goods_number":cart.goods_number,
            "goods_total":cart.goods_total,
        }
        result = {"code":10000,"msg":"保存成功","data":data}
    except:
        result=  {"code":10001,"msg":"保存失败"}

    return JsonResponse(result)

def temptest(request):
    goods = Goods.objects.all()
    count = 10
    return render(request,'buyer/test.html',locals())

