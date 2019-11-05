from django.http import HttpResponse


def index(request):
    """
    视图： 函数视图-》 以函数定义的视图
    :param request: 包含请求信息的请求对象
    :return: HttpResponse  响应对象
    """

    return HttpResponse("hello world")




def hello(request):
    return HttpResponse("wo shi hello")


def demo(request, id):
    print(id)
    return HttpResponse("demo")


def demo02(request, city, year):
    # print (year)
    # print (city)
    return HttpResponse("test")
    # return HttpResponse("%s年我在%s"% (year,city))


def test():
    pass


def demo1(request):
    """
    视图函数：处理用户请求，返回响应
    :param request:  包含请求信息的请求对象
    :return:    HttpResponse  响应对象
    """

    return HttpResponse("demo1")
    # return "demo1"


import time


def getDay(request, year, month, day):
    t = (int(year), int(month), int(day), 0, 0, 0, 0, 0, 0)
    mktime = time.mktime(t)
    print(mktime)
    now = time.localtime(mktime)
    day = now.tm_yday
    print(day)
    return HttpResponse(day)


from django.template import Template, Context


def tpltest(request):
    html = """
    <html>
    <head></head>
    <body>
    <h1>这个是tpltest页面</h1>
    <h2>姓名:{{ name }}</h2>
    <img src ="https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1572840692157&di=e24697b23c4e67b5ed95845b0a6989fa&imgtype=0&src=http%3A%2F%2Fs9.rr.itc.cn%2Fr%2FwapChange%2F20167_1_23%2Fa2jx1g6563802381352.jpg">
    <a href = "https://www.baidu.com">百度</a>
    </body>
    </html>
    """
    ## 数据的渲染
    name = "laoli"
    ## 1. 实例化一个template对象
    template_obj = Template(html)
    ##
    params = dict(name=name)
    ## 2. 实例化一个 context实力对象
    context_obj = Context(params)
    ##3. 进行数据渲染
    result = template_obj.render(context_obj)
    ##4. 返回结果
    return HttpResponse(result)

    # return HttpResponse(html)
    # return HttpResponse("tpltest")


from django.shortcuts import render, render_to_response


def myindex(request):
    return render(request, "index.html", {"name": "laowang"})


def myindex2(request):
    return render_to_response("index.html", {"name": "index2"})


from django.template.loader import get_template


def myindex3(request):
    name = "lisi"
    template = get_template("index.html")
    result = template.render({"name": name})

    return HttpResponse(result)


from datetime import datetime


def tmptest(request):
    # return render(request,"tmptest.html",{"name":"laowang","age":19})
    params = dict(name="lisi1111",age=19)
    return render(request,"tmptest.html",params)

    # name = "hello"
    # age = 18
    # # params = {"name":name,"age":age}
    # hobby = ["singing", "football", "dancer", "rapper"]
    # score = {"shuxue": 100, "yuwen": 90, "yingyu": 90}
    # now_time = datetime.now()
    # # now_time = now_time.strftime("%Y-%m-%d %H:%M:%S")
    # js = """
    # <script>
    #     alert("111111");
    # </script>
    # """
    # return render(request, "tmptest.html", locals())


def statictest(request):
    return render(request, "statictest.html")


def demotest(request):

    params = [
        {"name":"麦迪","img":"md.jpg","url":"https://www.baidu.com"},
        {"name":"科比","img":"kb.jpg","url":"https://www.sina.com"},
        {"name":"詹姆斯","img":"zms.jpg","url":"https://www.taobao.com"},
        {"name":"杜老二","img":"dlt.jpg","url":"http://127.0.0.1:8000/index"},
    ]

    return render(request,"demotest.html",locals())




