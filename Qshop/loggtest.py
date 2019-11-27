### 使用python3中模块 学习日志   txt
import logging


## 将日志收集到文件中
format = "%(asctime)s【%(levelname)s】%(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"
file_hadlers = logging.FileHandler("test.log",encoding="utf-8")
stream_hadlers = logging.StreamHandler()

## 日志的配置
##  level  -》 收集日志的等级
## format   ->   日志的格式
## datefmt  -》  时间格式
## handlers  -》 列表，放置文件句柄
logging.basicConfig(level=logging.DEBUG,format=format,datefmt=datefmt,handlers=[file_hadlers,stream_hadlers])  ##  代表收集日志 是从 INFO等级开始
# logging.basicConfig(level=logging.DEBUG)  ##  代表收集日志 是从 INFO等级开始

logging.debug("我是debug等级")
logging.info("我是info等级")
logging.warning("我是warning等级")
logging.error("我是error等级")
logging.critical("我是critical等级")


