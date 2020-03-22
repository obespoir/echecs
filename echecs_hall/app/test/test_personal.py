# coding=utf-8
import json

import requests


def test_personal():
    # url = 'http://127.0.0.1:8888/majapi/getpersonal?base={"uid": 9166, "skey": "e190f9cb4e09577ef3cc291d4429c2df"}'

    url = 'http://127.0.0.1:8888/majapi/getcurrency?base={"uid": 9166, "skey": "e557c506a2863c67796b805b828bd6af"}'
    requests.get(url)


def test_get_user_info_by_id():
    url = 'http://127.0.0.1:8889/majapi/get_userinfo?base={"uid": 9167}'
    r = requests.get(url)
    print("code = ", r.status_code)
    print("text = ", r.text)


def test_dd_roboot():
    url = "https://oapi.dingtalk.com/robot/send?access_token=ad41bef77276dd44bd91dd4c32145eff3525bd3cff3e67d12be8ca1dbd32989c"
    headers = {'Content-Type': 'application/json'}
    params = {
        "msgtype": "text",
        "text": {
            "content": "请问你是不是群里最性感的小美女!!",
        },
        "at": {
            "atMobiles": [
                "15002039236"
            ],
            "isAtAll": False
        }
    }
    data = json.dumps(params)
    r = requests.post(url, data, headers=headers)

    print("code = ", r.status_code)
    print("text = ", r.text)


def test_dd_roboot_md():
    url = "https://oapi.dingtalk.com/robot/send?access_token=ad41bef77276dd44bd91dd4c32145eff3525bd3cff3e67d12be8ca1dbd32989c"
    headers = {'Content-Type': 'application/json'}
    params = {
        "msgtype": "markdown",
        "markdown": {
            "title": "妖精别跑",
            "text": "#### 小妖精的照片 @15002039236\n" +
                    "> 你跑的出法海的手掌吗?\n\n" +
                    "> ![screenshot](http://ozgj3gqsu.bkt.clouddn.com/user3.png)\n" +
                    "> ###### 南无阿弥陀佛!! \n"
        },
        "at": {
            "atMobiles": [
                "15002039236"
            ],
            "isAtAll": False
        }
    }
    data = json.dumps(params)
    r = requests.post(url, data, headers=headers)

    print("code = ", r.status_code)
    print("text = ", r.text)

# 独立跳转ActionCard类型
def test_dd_roboot_action_card():
    url = "https://oapi.dingtalk.com/robot/send?access_token=ad41bef77276dd44bd91dd4c32145eff3525bd3cff3e67d12be8ca1dbd32989c"
    headers = {'Content-Type': 'application/json'}
    params = {
        "actionCard": {
            "title": "看图猜明星",
            "text": "![screenshot](http://ozgj3gqsu.bkt.clouddn.com/user2.png) 20 ### 请注意图中的人物 20 她的名字是???",
            "hideAvatar": "0",
            "btnOrientation": "0",
            "btns": [
                {
                    "title": "a",
                    "actionURL": "http://127.0.0.1:8889/mj/pic_get_name?index=1"
                },
                {
                    "title": "b",
                    "actionURL": "http://127.0.0.1:8889/mj/pic_get_name?index=2"
                },
                {
                    "title": "c",
                    "actionURL": "http://127.0.0.1:8889/mj/pic_get_name?index=3"
                },
                {
                    "title": "d",
                    "actionURL": "http://127.0.0.1:8889/mj/pic_get_name?index=4"
                }
            ]
        },
        "msgtype": "actionCard"
    }
    data = json.dumps(params)
    r = requests.post(url, data, headers=headers)

    print("code = ", r.status_code)
    print("text = ", r.text)


if __name__ == '__main__':
    test_get_user_info_by_id()
