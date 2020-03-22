# coding=utf-8
from app.extensions.globalobject import GlobalObject
from app.data_bridge import er_mj_bridge
from app.share.error_code import *



def join_room(session_id, user_id, room_type):
    """
    用户加入房间接口, 保持用户session_id 和user_id, 用于登录验证该用户是否需要断线重连
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
    :return:
    """
    ret = {"room_name": ""}
    code = 0
    room_cfg = GlobalObject().room_cfg_list[room_type]
    income_support = GlobalObject().income_support
    user_gold = er_mj_bridge.get_user_gold_by_id(user_id)
    print("user_gold = ", user_gold)
    print("room_type = ", room_type)
    print("room_cfg = ", room_cfg)
    # 金币是否满足场次要求
    if user_gold < room_cfg.get("min_enter_gold"):
        # 用户当前金币+低保金币 > 所选场次下限
        if (user_gold + income_support) > room_cfg.get("min_enter_gold"):
            # 用户是否可以领取低保
            if er_mj_bridge.is_can_get_income_support_by_id(user_id):
                code = GET_INCOME_SUPPORT
            else:
                code = SHOW_RECOMMEND_PAY_NUM
        else:
            code = SHOW_RECOMMEND_PAY_NUM
    else:
        ret["room_name"] = er_mj_bridge.join_room(session_id, user_id, room_type=room_type)
    print("join room ret=", ret)
    return code, ret


def match_room_game_start(session_id, user_id, room_name, room_type):
    """
    用户需要断下重连
    :param session_id: 用户session
    :param user_id: 用户ID
    :param room_name: 服务器节点名
    :param room_type: 房间类型 (初级,中级, 高级场)
    :return:
    """
    r = er_mj_bridge.need_reconnect(session_id, user_id, room_name, room_type=room_type)
    return r


def match_room_game_over(user_id):
    """
    用户需要断下重连
    :param user_id: 用户ID
    :return:
    """
    r = er_mj_bridge.clear_need_reconnect(user_id)
    return r


def left_room(session_id, user_id):
    """
    用户离开房间, 清楚必要信息
    :param session_id:
    :param user_id:
    :return:
    """
    return er_mj_bridge.left_room(session_id, user_id)


def delete_room():
    """
    用户离开房间, 清楚必要信息
    :param session_id:
    :param user_id:
    :return:
    """
    return er_mj_bridge.delete_room()


def is_exits_desk(user_id):
    return er_mj_bridge.is_exits_in_desk(user_id)


def get_room_players_by_room_type(room_typ):
    """
    通过房间类型过去房间人数
    :param room_typ:
    :return:
    """
    return er_mj_bridge.get_elementary_room_count(room_typ)


def _get_room_players_count():
    """
    获取当前所有房间人数 默认 [初级场,中级场,高级场]
    :param room_typ:
    :return:
    """
    return er_mj_bridge.get_all_room_count()


def _get_room_cfg(room_type=None):
    """
    获取当前场次所有配置,或者根据room_type获取某个游戏场配置
    :return:
    """
    return er_mj_bridge.get_room_cfg(room_type)


def get_hall_room_info():
    """
    获取游戏大厅内场次相关信息(底分,进入上限,进入下限,当前人数)
    :return:
    """
    room_cfgs = _get_room_cfg()
    cur_player_count = _get_room_players_count()
    if not room_cfgs == [{}]:
        for index, i in enumerate(cur_player_count):
            room_cfgs[index]['cur_player_count'] = cur_player_count[index]
    return room_cfgs

def get_hall_room_people_count():
    """
    获取游戏大厅内场次相关信息(底分,进入上限,进入下限,当前人数)
    :return:
    """
    cur_player_count = _get_room_players_count()
    return cur_player_count

def init_room_cfg():
    """
    初始化三个场次的基本信息, 根据策划需求初始化房间基本信息
    :return:
    """
    id1 = er_mj_bridge.create_room_cfg("初级场", "{}", 1000, 999, 0, 60, 90, 12, 6, 0, 6, 0)
    id2 = er_mj_bridge.create_room_cfg("中级场", '{"pass_hu_double":1}', 10000, 4000, 0, 150, 220, 12, 10, 0, 6, 1)
    id3 = er_mj_bridge.create_room_cfg("高级场", '{"pass_hu_double":1}', 40000, 20000, 0, 500, 750, 12, 12, 0, 6, 2)
    return [id1, id2, id3]
