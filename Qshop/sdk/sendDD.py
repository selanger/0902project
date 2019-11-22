import requests
import json

def senddingding(params):
    """

    :param params:
    params = dict(content = "",isAtAll= True/False,"atMobiles":[])
    :return:
    """
    url = "https://oapi.dingtalk.com/robot/send?access_token=8bdb64b5071b59d84f4fe621a30fe7570d1e6bcd76773ac374ffb6d1f5705454"

    data = {
        "msgtype": "text",
        "text": {
            "content": params.get("content")
        },
        "at": {
            "atMobiles": params.get("atMobiles"),
            "isAtAll": params.get("isAtAll")
        }
    }

    headers = {
        'Content-type': 'application/json'
    }

    data = json.dumps(data)

    response = requests.post(url, headers=headers, data=data)

    print(response.content.decode())
