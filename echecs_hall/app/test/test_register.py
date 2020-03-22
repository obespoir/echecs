#!/usr/bin/env python
# coding=utf-8
import requests
import json


def test_register():
    for i in range(50, 101):
        user_name = "oldboy{}".format(i)
        data = json.dumps({"user": user_name, "password": "123456", "nickname": user_name})
        url = 'http://127.0.0.1:8889/majapi/register?base={}'.format(data)

        r = requests.get(url)
        print(r.text)


if __name__ == '__main__':
    test_register()
