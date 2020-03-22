# coding=utf-8
import requests
import json
from obespoir.share.ob_log import logger


def notify_web_server_left_room(user_id, session_id, room_type=0):
    url = "http://127.0.0.1:8889/mj/left_room"
    params = {"user_id": user_id, "session_id": session_id, "room_type": room_type}
    r = requests.get(url, params)
    if r.status_code != 200:
        raise Exception("web server left_room error paras = %s"%params)
    data = json.loads(r.text)
    if data.get("ret"):
        raise Exception("web server left_room error ret = %s"%data.get("ret"))


def notify_web_server_restart():
    url = "http://127.0.0.1:8889/mj/restart_delete_room_info"
    params = {}
    r = requests.get(url, params)
    if r.status_code != 200:
        logger.error("web server left_room error paras = %s" % params)
        print("delete error!!")
        return
    data = json.loads(r.text)
    if data.get("ret"):
        raise Exception("web server left_room error ret = %s" % data.get("ret"))

    print("delete success!!")


def notify_web_server_join_room(user_id, session_id, room_type=0):
    url = "http://127.0.0.1:8889/mj/join_room"
    params = {"user_id": user_id, "session_id": session_id, "room_type": room_type}
    print("notify_web_server_join_room:", params)
    r = requests.get(url, params)
    if r.status_code != 200:
        raise Exception("web server join_room error paras = %s" % params)
    data = json.loads(r.text)

    print("join_room success!! data=", data)
    return data


def notify_web_server_match_room_start_game(user_id, session_id, room_name, room_type=0):
    url = "http://127.0.0.1:8889/mj/match_room_start_game"
    params = {"user_id": json.dumps(user_id), "session_id": session_id, "room_type": room_type, "room_name": room_name}
    print("xxxxxxxxxxxxx", params)
    r = requests.get(url, params)
    if r.status_code != 200:
        raise Exception("web server join_room error paras = %s" % params)
    data = json.loads(r.text)
    print("notify_web_server_match_room_start_game success!!")
    return data


def notify_web_server_match_room_game_over(user_id):
    url = "http://127.0.0.1:8889/mj/match_room_game_over"
    params = {"user_id": json.dumps(user_id)}
    r = requests.get(url, params)
    if r.status_code != 200:
        raise Exception("web server join_room error paras = %s" % params)
    data = json.loads(r.text)
    print("notify_web_server_match_room_start_game success!!")
    return data





