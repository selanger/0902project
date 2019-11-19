from django.shortcuts import render
from Seller.models import *
from Seller.views import setPassword
from django.http import HttpResponseRedirect
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


# @LoginValid
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
    return render(request,'buyer/detail.html',locals())

## 个人中心
@LoginValid
def person_info(request):
    return render(request,"buyer/person_info.html")
## 购物车
@LoginValid
def cart(request):
    return render(request,"buyer/cart.html")

# 订单页面
@LoginValid
def user_center_order(request):
    return render(request,"buyer/user_center_order.html")

## 收货地址
@LoginValid
def user_center_site(request):
    return render(request,"buyer/user_center_site.html")
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
    goods = Goods.objects.get(id=int(goods_id))
    ## 保存数据
    ## 保存订单
    payorder = PayOrder()
    payorder.order_number = str(time.time()).replace(".","")
    payorder.order_status = 1  ## 未支付
    payorder.order_total = goods.goods_price * int(goods_count)
    payorder.order_user = LoginUser.objects.get(id = int(user_id))
    payorder.save()
    ## 保存订单详情

    orderinfo = OrderInfo()
    orderinfo.order_id = payorder
    orderinfo.goods = goods
    orderinfo.goods_price = goods.goods_price
    orderinfo.goods_count = int(goods_count)
    orderinfo.goods_total_price =  goods.goods_price * int(goods_count)
    orderinfo.save()


    return render(request,"buyer/place_order.html",locals())