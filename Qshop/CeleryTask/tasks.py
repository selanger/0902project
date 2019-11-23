## 任务
from __future__ import absolute_import
from Qshop.celery import app   ## 导入实例化的celery应用

## 编写任务
## 将函数转变为 celery任务
@app.task
def Test():
    ## 没有参数
    import time
    time.sleep(10)
    print ("hello")
@app.task
def add(a,b):
    c = a+b
    print(c)
    return c

from sdk.sendDD import senddingding
@app.task
def sendDingDing(params):
    senddingding(params)





