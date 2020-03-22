# coding=utf-8
import requests
import json


class MessageRoute(object):
    """
    获取消息需要转发的下游节点
    """
    def __init__(self):
        pass

    def get_route(self, user_id, session_id=""):
        """
        获取路由信息
        :param user_id: 用户id
        :return: {"code":int,"info":{"room":room_name, ...}}
        """
        # 验证用户是否已经登录，同时用户id和session_id对应关系是否正确
        return {"code": 200, "info": {"room": "room_1"}}

    def login(self, user_id, passwd, new_sessionid, data):
        """
        登录
        :param user_id:
        :param new_sessionid:
        :param data:  json串, {"passwd": 32md5}
        :return:
        """
        # 验证用户id和密码是否正确，正确时得到用户所在的房间名（空时代表新登录，有值时代表断线重连）
        passwd = data.get("passwd")
        url = "http://127.0.0.1:8889/mj/login"
        params = {"user_id": user_id, "session_id": new_sessionid, "password": passwd}
        r = requests.post(url, params)
        if r.status_code != 200:
            raise Exception("login web serve error! code=%s"%r.status_code)
        data = json.loads(r.text)
        print(data)
        if data.get("ret") == 0:
            return {"code": 200, "info": data.get("data")}
        else:
            return data

    def clear_room(self, room_name):
        return


route_ins = MessageRoute()