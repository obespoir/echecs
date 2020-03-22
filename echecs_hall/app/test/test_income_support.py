# coding=utf-8
import requests
import json


def test_income_support():
    url = 'http://127.0.0.1:8888/majapi/receiveincomesupport?base={"uid": 9166, "skey": "efede33028c0a8ffb0d3e5cbaca9696c"}'
    url = 'http://127.0.0.1:8888/majapi/getincomesupport?base={"uid": 9166, "skey": "efede33028c0a8ffb0d3e5cbaca9696c"}'

    requests.get(url)

if __name__ == '__main__':
    test_income_support()

