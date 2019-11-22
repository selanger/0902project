#coding:utf-8
import requests

def sendcode(params):
    """
    发送短信
    :param params:  {"mobile":"","content":"123214"}
    :return:
    """
    url = "http://106.ihuyi.com/webservice/sms.php?method=Submit"
    #APIID
    account = "C09572371"
    #APIkey
    password = "c5cff620dc119a8e6b66b8566f833eb0"
    ## 接收人手机号
    # mobile = "19919961053"
    mobile = params.get("mobile")
    ## 发送内容
    content = "您的验证码是：%s。请不要把验证码泄露给其他人。" % (params.get("content"))
    ##  请求头
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    ## 构建发送参数
    data = {
        "account": account,
        "password": password,
        "mobile": mobile,
        "content": content,
    }
    ## 发送请求
    response = requests.post(url,headers = headers,data=data)
        #url 请求地址
        #headers 请求头
        #data 发送短信内容

    print(response.content.decode())