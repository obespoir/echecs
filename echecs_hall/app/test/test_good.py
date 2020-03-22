# coding=utf-8
import requests
import json


def test_good():
    # url = 'http://127.0.0.1:8888/majapi/getgood?base={"uid": 9166, "skey": "5bae59973c314dad6223bb1218422a78"}'
    url = 'http://127.0.0.1:8888/majapi/buygood?base={"uid": 9166, "skey": "5bae59973c314dad6223bb1218422a78", ' \
          '"param":{"id":1}}'

    requests.get(url)

if __name__ == '__main__':
    test_good()

