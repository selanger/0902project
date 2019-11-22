import smtplib
from email.mime.text import MIMEText

## 构建邮件格式
subject = "0902测试"
content = """
    好好学习，天天向上
"""
## 发送人
sender = "str_wjp@163.com"
## 接收人
recver = """18910555570@163.com,18910555570@163.com,18910555570@163.com,18910555570@163.com"""

password = "w123456"   ## 邮箱授权密码

message = MIMEText(content,"plain","utf-8")
        ##  内容    内容类型    编码
message["Subject"] = subject
message["From"] = sender
message["To"] = recver

## 发送邮件
smtp = smtplib.SMTP_SSL("smtp.163.com",465)
smtp.login(sender,password)   ## 登录发送人的邮箱
smtp.sendmail(sender,recver.split(","),message.as_string())
# sender,  发送人
# recver,   接收人  可以是一个列表 []
# message.as_string()  发送内容
# as_string 类似于json的封装方式，目的是为了在协议上传输发送内容

smtp.close()












