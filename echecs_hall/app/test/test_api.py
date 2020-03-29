# coding=utf-8
import requests
import json
from app.extensions.common import md5


def test_login():
    url = "http://127.0.0.1:8889/mj/login"
    pwd = md5("112233" + "123456")
    params = {"user_id": 9169, "session_id": "proxy_1,100", "password": "112233"}
    r = requests.post(url, params)
    print(r.status_code)
    print(r.text)


def test_join_room():
    url = "http://127.0.0.1:8889/mj/join_room"
    params = {"user_id": 9172, "session_id": "proxy_1,100", "room_type": 0}
    r = requests.get(url, params)
    print(r.status_code)
    print(r.text)


def test_match_room_start_game():
    url = "http://127.0.0.1:8889/mj/match_room_start_game"
    params = {"user_id": json.dumps([9172, 9171]), "session_id": "proxy_1,100", "room_type": 0, "room_name": "room_1"}
    print("test_match_room_start_game =", params)
    r = requests.get(url, params)
    print(r.status_code)
    print(r.text)


def test_match_room_game_over():
    url = "http://127.0.0.1:8889/mj/match_room_game_over"
    params = {"user_id": json.dumps([9172,9171])}
    r = requests.get(url, params)
    print(r.status_code)
    print(r.text)


def test_left_room():
    url = "http://127.0.0.1:8889/mj/left_room"
    params = {"user_id": json.dumps([9169, 9168]), "session_id": "proxy_1,100", "room_type": 0}
    r = requests.get(url, params)
    print(r.status_code)
    print(r.text)


def test_delete_room_info():
    url = "http://127.0.0.1:8889/mj/delete_room_info"
    params = {}
    r = requests.get(url, params)
    print(r.status_code)
    print(r.text)


def test_get_hall_room_info():
    url = "http://127.0.0.1:8889/mj/get_hall_room_info"
    params = {}
    r = requests.get(url, params)
    print(r.status_code)
    print(r.text)


def test_get_hall_room_info2():
    url = "http://127.0.0.1:8889/mj/get_hall_room_info2"
    params = {}
    r = requests.get(url, params)
    print(r.status_code)
    print(r.text)


def test_init_room_cfg():
    url = "http://127.0.0.1:8889/mj/init_room_cfg"
    params = {}
    r = requests.get(url, params)
    print(r.status_code)
    print(r.text)


def test_restart_delete_room_info():
    url = "http://127.0.0.1:8889/mj/restart_delete_room_info"
    params = {}
    r = requests.get(url, params)
    print(r.status_code)
    print(r.text)


def test_pic_get_name():
    url = "http://127.0.0.1:8889/mj/pic_get_name"
    params = {"index":1}
    r = requests.get(url, params)
    print(r.status_code)
    print(r.text)



def test_get_hall_room_people_count():
    url = "http://127.0.0.1:8889/mj/get_hall_room_people_count"
    params = {}
    r = requests.get(url, params)
    print(r.status_code)
    print(r.text)


class TT(object):
    a = 1
    b = 2

    def __init__(self, name):
        self.name = name

    def validate(self):
        print("aaaa")


if __name__ == "__main__":
    # print(TT._unbound_fields)
    # print(dir(TT))
    # test_restart_delete_room_info()
    # test_match_room_game_over()
    test_get_hall_room_info2()
    test_init_room_cfg()