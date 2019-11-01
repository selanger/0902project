"""
正则：是一种字符串的处理方式，用于匹配字符串

字符串的匹配两种：
内容匹配：
    通过描述要匹配内容的类型，长度，获取匹配到的结果
    re
结构匹配：
    xpath 爬虫
    通过描述要匹配的内容，在整体中的结构去匹配到想要的内容
"""
import re
###   re.findall()  返回列表，返回的结果是所有符合条件的结果
###  内容匹配
## 类型匹配   原样匹配 . \d \D \w \W [] | ()
## 长度匹配   * ? + {}
## 特殊匹配   ^ $


string = "hello \n world 123 ___ "
# 原样匹配
# res = re.findall("hello",string)
# print (res)
# .  除了  \n 的 所有字符
# res = re.findall(".",string)
# print (res)
# \d  匹配的是数字
# res = re.findall("\d",string)
# print (res)
# # \D 除了数字
# res = re.findall("\D",string)
# print (res)
# \w  数字  字母   _
# res = re.findall("\w",string)
# print (res)
#
# # \W 非数字  非字母 非_
# res = re.findall("\W",string)
# print (res)
# []  返回括号中的任意一个字符
res = re.findall("[a-zA-Z0-9]",string)
print (res)
## ^ 代表取反
res = re.findall("[^a-zA-Z0-9]",string)
print (res)
# # |  或者
#
# res = re.findall("hellowewewe|world",string)
# print (res)
# string = "hello \n world 1235 12 45 7 h ___ "
# # () 组匹配  ()后面的是条件
# res = re.findall("(\d)\d",string)    ## 34h       56h      2wh
# print (res)
# P 起一个组名
# string = "132 244 363 578"
# res = re.findall("(?P<id>\d)\d",string)    ## 34h       56h      2wh
# print (res)
# # (?P=id) 使用 id的值
# res = re.findall("(?P<id>\d)\d(?P=id)",string)    ## 34h       56h      2wh
# print (res)


#   长度匹配   * ? + {}
# string = "hello \n world 123 ___ "

# *   匹配  0次或多次
# res = re.findall("\d*",string)
# print (res)
# + 匹配一次或多次
# res = re.findall("\d+",string)
# print (res)
# ? 匹配 0次或1次
# res = re.findall("\d?",string)
# print (res)
# {}  匹配指定次数
# res = re.findall("\d{3}",string)
# print (res)


## 特殊匹配   ^ $
# ^  开始  匹配开头
# string = "hello \n world 123 ___ "
# res = re.findall("^hello",string)
# print (res)


# $ 结束   匹配结尾
# res = re.findall(" $",string)
# print (res)

