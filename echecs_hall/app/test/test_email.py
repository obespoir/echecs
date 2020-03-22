# coding=utf-8
import requests
import json


def test_email():
    # url = 'http://127.0.0.1:8888/majapi/getemail?base={"uid": 9166, "skey": "ae8fdd736a261bf9e6c518e7a26aeb78"}'
    url = 'http://127.0.0.1:8888/majapi/reademail?base={"uid": 9166, "skey": "ae8fdd736a261bf9e6c518e7a26aeb78", ' \
          '"param": {"id": 3}}'
    url = 'http://127.0.0.1:8888/majapi/confirmemail?base={"uid": 9166, "skey": "ae8fdd736a261bf9e6c518e7a26aeb78", ' \
          '"param": {"id": 4}}'
    requests.get(url)


if __name__ == '__main__':
    test_email()