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



def demo(request,id):
    print (id)
    return HttpResponse("demo")

def demo02(request,city,year):
    # print (year)
    # print (city)
    return HttpResponse("test")
    # return HttpResponse("%s年我在%s"% (year,city))
def test():
    pass