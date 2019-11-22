import smtplib
from email.mime.text import MIMEText

def sendemail(params):
    """
    发送邮件方法
    :param params:
    :param = {"subject":"","content":"","recver":""}
    :return:
    """
    subject = params.get("subject")
    content = params.get("content")
    sender = "str_wjp@163.com"
    recver = params.get("recver")
    password = "w123456"  ## 邮箱授权密码
    message = MIMEText(content, "plain", "utf-8")
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recver
    smtp = smtplib.SMTP_SSL("smtp.163.com", 465)
    smtp.login(sender, password)  ## 登录发送人的邮箱
    smtp.sendmail(sender, recver.split(","), message.as_string())
    smtp.close()

