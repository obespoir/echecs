# coding=utf-8
import json

from app.extensions.redis.redis_utils import redis_db
from app.models.user import User
from app.models.room_cfg import RoomCFG


SESSION_KEY = "web_services:session:Session_userID"
USER_DESK_KEY = "web_services:hUserDesk"
elementary_room = {}  # 用于储存出机场人数
ELEMENTARY_ROOM = "web_services:u_elementary_room"
INTERMEDIATE_ROOM = "web_services:u_intermediate_room"
TOP_ROOM = "web_services:u_top_room"


def get_user_by_user_id(user_id):
    return redis_db.hgetall("hu:%s" % user_id)


def validate_user_password(user_id, pwd):
    return User.validate_password_for_id(user_id, pwd)


def notify_prev_user(session_id):
    pass


def exist_user_desk(user_id):
    r = redis_db.hget(USER_DESK_KEY, int(user_id))
    return r


def enter_game(user_id, session_id, room_name=None):
    data = {user_id: session_id}
    redis_db.hmset(SESSION_KEY, data)
    pass


def is_login(session_id):
    r = redis_db.hget(SESSION_KEY, session_id)
    return r


def join_room(session_id, user_id, room_type=0):
    """
    需要判定:1. 金币是否满足场次要求
                if 金币低于所选场次下限:
                    if 用户当前金币+低保金币 > 所选场次下限:
                        if 用户是否可以领取低保:
                            弹出窗口,领取低保
                            进入游戏
                    else:
                        根据场次要求显示对应快速充值弹窗
    :param session_id:
    :param user_id:
    :param room_type:
    :return:
    """
    room_name = _get_room_name()
    # data = {"user_id": user_id, "session_id": session_id, "room_name": room_name, "room_type": room_type}
    # r = redis_db.hset(USER_DESK_KEY, user_id, json.dumps(data))
    return room_name



def need_reconnect(session_id, user_id, room_name, room_type=0):
    """
    需要断线重连   在匹配场中, 游戏开始后, 游戏结束前需要断线重连,其他时间不需要断线重连
    :param session_id:
    :param user_id:
    :param room_type:
    :return:
    """
    r = None
    data = {"user_id": user_id, "session_id": session_id, "room_name": room_name, "room_type": room_type}
    if isinstance(user_id, list):
        for i in user_id:
            data["user_id"] = i
            r = redis_db.hset(USER_DESK_KEY, i, json.dumps(data))
        return bool(r)
    else:
        data["user_id"] = user_id
        r = redis_db.hset(USER_DESK_KEY, user_id, json.dumps(data))
    return bool(r)


def clear_need_reconnect(user_id):
    """
    需要断线重连   在匹配场中, 游戏开始后, 游戏结束前需要断线重连,其他时间不需要断线重连
    :param user_id:
    :return:
    """
    if isinstance(user_id, list):
        r = None
        for i in user_id:
            r = redis_db.hdel(USER_DESK_KEY, i)
        return bool(r)
    else:
        r = redis_db.hdel(USER_DESK_KEY, user_id)
    return bool(r)
    return r


def is_exits_in_desk(user_id):
    return redis_db.hget(USER_DESK_KEY, user_id)


def get_user_gold_by_id(user_id):
    """

    :param user_id:
    :return:
    """
    # TODO 通过数据库获取用户金币
    return User.get_user_money(user_id)


def is_can_get_income_support_by_id(user_id):
    # TODO 通过请求阿帆接口获取是否可以领取低保
    return True



def get_elementary_room_count(room_type):
    return len(_get_user_form_room_by_room_type(room_type))


def get_all_room_count():
    ret = []
    for i in [0, 1, 2]:
        ret.append(len(_get_user_form_room_by_room_type(i)))
    return ret


def get_room_cfg(name=None):
    """
    获取房间配置信息,如果有名字, 则根据名字获取, 如果没有名字则获取全部房间信息
    :param name:
    :return: [{}]
    """
    if name:
        room_cfg = RoomCFG.get_cfg_by_name(name)
    else:
        room_cfg = RoomCFG.get_cfg_all()
    return room_cfg


def left_room(session_id, user_id):
    if isinstance(user_id, list):
        r = None
        for i in user_id:
            r = redis_db.hdel(USER_DESK_KEY, i)
        return bool(r)
    else:
        r = redis_db.hdel(USER_DESK_KEY, user_id)
    return bool(r)


def delete_room():
    r = redis_db.delete(SESSION_KEY)
    r = redis_db.delete(USER_DESK_KEY)
    return bool(r)


def _get_room_name():
    """
    根据策略获取当前最需要加入的房间
    :return: 房间名
    """
    # TODO
    return "room_1"


def _get_user_form_room_by_room_type(room_type):
    """
    通过给定的房间类型, 查找该房间玩家桌子信息
    :param room_type:
    :return:
    """
    r = redis_db.hgetall(USER_DESK_KEY)
    ret = []
    if r:
        if isinstance(r, str):
            user_desk = json.loads(r)
        else:
            user_desk = r
        for i in user_desk.items():
            _room_type = json.loads(i[1]).get("room_type")
            if int(room_type) == int(_room_type):
                ret.append(i)
    return ret


def create_room_cfg(name, special_rule, min_enter_gold, min_play_gold, max_enter_gold, base_bet, service_charge,
                    draw_card_time, min_hu_fan, max_hu_fan, recommend_pay_num, room_type):
    room_cfg = RoomCFG.get_cfg_by_name(name)

    if room_cfg == [{}]:
        room_cfg_id = RoomCFG.create(name, special_rule, min_enter_gold, min_play_gold, max_enter_gold, base_bet,
                                 service_charge, draw_card_time, min_hu_fan, max_hu_fan, recommend_pay_num, room_type)
    else:
        return room_cfg[0].im_self.id
    return room_cfg_id


if __name__ == "__main__":
    pass