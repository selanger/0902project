from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse

##编写 中间件
class MiddleWareTest(MiddlewareMixin):
    def process_request(self,request):
        """
        请求进来，第一个要触发的方法
        只能针对request 进行处理 还能 针对服务进行处理
        :param request:  包含请求信息的请求对象
        :return:   返回None  之后才会执行下面的流程，否则直接返回到浏览器

        校验请求的ip   黑名单
        """
        ## 先获取到请求的ip
        rep_ip = request.META.get("REMOTE_ADDR")
        print (rep_ip)
        ## 判断ip是否在黑名单中
        if rep_ip == "10.10.92.244":
            ## 返回响应
            return HttpResponse("同学，请绕路，不支持你访问！！！")
        print("我是 process_request")

    def process_view(self,request,callback,callbackargs,callbackkwargs):
        """
        请求通过process_request 第二个方法被触发
        :param request:  包含请求信息的请求对象
        :param callback:  要访问的视图函数，要处理请求的视图函数
        :param callbackargs:   元祖    传递请求的参数
        :param callbackkwargs:   字典    参数
                参数传递：  通过路由正则进行传递
                        元祖：  没有组名   re_path("/index/(\w+)/",view)
                        字典：  有组名     re_path("/index/(?P<name>\w+)/",view)   -> {"name":""}
        :return:  返回None  执行下面的流程
        """
        print("我是 process_view")
        # print(callback)
        print(callbackargs)
        print(callbackkwargs)
        version = callbackkwargs.get("date")
        print (version)
        if version == "v1":
            return HttpResponse("版本过期")




    def process_exception(self,request,exception):
        """
        处理异常   写入日志
        :param request:
        :param exception:  异常信息
        :return:
        """
        print("我是 process_exception")
        print(exception)
        ## 获取到异常信息
        ## 写入日志文件
        from Qshop.settings import BASE_DIR
        import os
        import time
        file = os.path.join(BASE_DIR,"error.log")
        now_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        with open(file,"a") as f:
            content = "[%s]:%s \n" % (now_time,str(exception))
            f.write(content)


    def process_template_response(self,request,response):
        """
        需要返回一个render对象
        :param request:
        :param response:
        :return:
        """
        print("我是 process_template_response")
        return response
    def process_response(self,request,response):
        """
        返回响应: 所有给用户的响应都需要经过这个方法
                正常的响应
                异常的响应
        可以针对响应做统一的处理   status_code   context_type
        :param request:
        :param response:
        :return:
        """
        print("我是 process_response")
        print(response)
        return response












