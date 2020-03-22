#!/usr/bin/env python
# coding=utf-8
import requests
import json


def test_login():
    param = {'user': 'test', 'password': '112233'}
    url = 'http://127.0.0.1:8889/majapi/login'
    r = requests.post(url, json=param)
    print(r.text)


if __name__ == '__main__':
    test_login()

