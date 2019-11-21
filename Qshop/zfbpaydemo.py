from alipay import AliPay
## 公钥的配置
alipay_public_key_string="""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAy1o2kzDLr8rXWVgtQ2HcaCXwlFyskx7V5PlWkRqqIqgVQQ7kiPw4Ru9PWou3fA5hBWCNQmJEgIBfGukdqoeitXcft1K5U5/gEOrUL8dqBf/VsN4iAwzptgfDXnC6UGz0NmOWihi6LtXftds7uMVNYAXHs3vf9TgJJusehVpkT7Evf+46VAKh7TnHWbWCVLo1OLOtjyIQFf0cOUkVNc+zXloTafqcjCSzBWuFlinGrhPhZpdec7ZTC+JSd4mgD/RvfW1hdy72I2c/X6chCuJ/ZiVCaKKTCbkfB1YReqXzsvmypQBQLO1CiyP8k36yQA8HNRma2CV/o5IA5nQi9+kNswIDAQAB
-----END PUBLIC KEY-----"""
## 私钥的配置
app_private_key_string ="""-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAy1o2kzDLr8rXWVgtQ2HcaCXwlFyskx7V5PlWkRqqIqgVQQ7kiPw4Ru9PWou3fA5hBWCNQmJEgIBfGukdqoeitXcft1K5U5/gEOrUL8dqBf/VsN4iAwzptgfDXnC6UGz0NmOWihi6LtXftds7uMVNYAXHs3vf9TgJJusehVpkT7Evf+46VAKh7TnHWbWCVLo1OLOtjyIQFf0cOUkVNc+zXloTafqcjCSzBWuFlinGrhPhZpdec7ZTC+JSd4mgD/RvfW1hdy72I2c/X6chCuJ/ZiVCaKKTCbkfB1YReqXzsvmypQBQLO1CiyP8k36yQA8HNRma2CV/o5IA5nQi9+kNswIDAQABAoIBAQCTl0BxCENtrZ0rPXJsq4RbGt5H8BNZHFJGRCnuWxoM2U3D0FlSiy0VXu+LWkisA4uraW5dNhFd6s4cLAHaGWOgrXsZhTL5XNo1rRqgKu3quMqR+kdZS2/9LBlCXDL92HZPW2yRgmzvPU+HID1yV9FW1hshS9E6m5cY5iFazEZuB3JjBNbnKIDljvBHrqsrolZmSlROEzALJjC3w2s9wTwzMsdJx2+NyJg0t8qX7nDjRzBxEUvsvHQ9HpAyHWGP5E1yKR6CPaJEg7LnDJDL3cr1wecFd1IQA7X0i+KqFgnUd4k86PQ7tbq0q7bWRLNfcXHVUs4eORl9xXQP6zTccIYhAoGBAO3iQqmoc7GCXkqe1lis98RJJP00NYL/J5zwG/483Sfq7YjTXD1Ie+jno5gcgkqzEIOMooss6CPJVf7lyno6Z/NFLoYA4GGMPkyKn/83Ar4YxEr5eIdfrQFdroh+7uqP+ckPhvjmeA78cITTwvMWf446jRCfk5neaGPfV9OcTSnrAoGBANrWu/hIyon/aX9Xn2RqEB/sLzADkPLs7bIES+8V5mc3ieRjqzTWO1dgOiMlXdqsQKtGgHjTm21ZVMm2E9GvaaVQax197VX2+y7m5iFtUoQtDMQzdx5HXUFHhR24YedbSbkDrLjY5C/JsjuJCIR3LNiUkUdyR6YpOvR/1SqkzrFZAoGARpD094EZ+NFUiUw/B4Uf5qFQELCZIyfvp1Vu6GdDr6C4H/ubBC7pWvjEBc6HNAOUZYGlgiWrI1qJYRjnjISg64BdQbEm3qkMngYNWlcGQD/2kssYXwgZuSsCKEmHNBvLnEI35sPvX3qxIiXzUcsdwaJK0GCWF3Hrg5zwX7yhA0sCgYEAnQVW+l/AdCP/3o9Qnww7Zaxib2EfsC6wnvrWQUbFe2ouVuHtBoxxJ9Cz5mP5Y94UyNBdflTXQS7H17P9pIboluWM9ixVD0mYEZ87oOCARLbOYjlLTz6Fe0GGEj0qgobN7yLj2/5EPMXMTUuWAPZCB2USmOE259LNqoHOwjpe1IECgYBmaCV3SBB0GAktHAnSxabQLvQCrVWu65yROD/pJR1yRkLguhUES6jye+7LBSPAjbv/0vMpT7JhisaAT7piv/MYzzLJyTf+be1tYyzuqMtgHnS7sktc6jOmu09VZfDULbbLz2fS3YYckF/MqXiz7oQIXEsSVnRO1b+c9K1WGEPgnw==
-----END RSA PRIVATE KEY-----"""


## 实例化对象
alipay = AliPay(
        appid="2016101300673550",
        app_notify_url=None,
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",
        debug=False
)
## 实例化订单
order_string = alipay.api_alipay_trade_page_pay(
    subject='生鲜交易',    ## 交易主题
    out_trade_no = '13244768914487',    ## 订单号
    total_amount = '10000',   ## 交易总金额  需要是一个string
    return_url=None,     ## 返回的路径
    notify_url=None      ## 通知路径
)
## 发送请求
## 构建一个请求url
result = "https://openapi.alipaydev.com/gateway.do?" + order_string
print (result)



