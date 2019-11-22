import requests
import json

url = "https://oapi.dingtalk.com/robot/send?access_token=8bdb64b5071b59d84f4fe621a30fe7570d1e6bcd76773ac374ffb6d1f5705454"

data = {
    "msgtype": "text",
    "text": {
        "content": "验证码：123123"
    },
    "at": {
        "atMobiles": [
        ],
        "isAtAll": True
    }
}

headers = {
    'Content-type': 'application/json'
}

data = json.dumps(data)

response = requests.post(url, headers=headers, data=data)

print(response.content.decode())
