## 1. 导包
from django import template
## 2. 实例化对象
register = template.Library()


## 3.编写自定义的过滤器
@register.filter(name="MyAdd")
def myadd(a):
    print(222)
    ## 过滤器的方法
    return a + a
@register.filter()
def mymanyadd(a,b):
    return a + b
@register.simple_tag()
def myalladd(a,b,c,d):
    return a+b+c+d

@register.filter()
def getcount(data):
    print (data)
    num = len(data)
    return num


















