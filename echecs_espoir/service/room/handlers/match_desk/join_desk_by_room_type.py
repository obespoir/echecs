# coding=utf-8

import random

from db.desk import Desk as DBDesk
from service.room.common_define import DeskType
from service.room.handlers.basehandler import BaseHandler, RegisterEvent
from service.room.models.room_desk import RoomDesk
from service.room.models.roomdesk_manager import desk_mgr
from service.room.models.user_manager import UserManager
from service.room.validators.match_desk.join_desk_by_room_type import JoinMatchDeskByTypeValidator
# from service.session_gate_rel import session_gate_ins
from config.globalconfig import GlobalConfig
from share.commontool import weight_choice
from share.notify_web_server import notify_web_server_join_room
from share.message_ids import *


@RegisterEvent(JOIN_MATCH_DESK_BY_TYPE)
class JoinMatchDeskByTypeHandler(BaseHandler):
    def execute(self, *args, **kwargs):
        """
        加入指定匹配场桌子请求处理
        :param args:
        :param kwargs:
        :return:
        """
        validator = JoinMatchDeskByTypeValidator(handler=self)
        desk, user = _apply_match_desk(validator.user_id.data, validator.session_id.data, max_player_num=2,
                                       room_type=validator.room_type.data)
        # session_gate_ins.update_rel(validator.session_id.data, self.gate_name)
        data = user.to_dict()
        desk.notify_desk_some_user(PUSH_USER_JOIN_DESK, data, [user.user_id])
        return {"desk_id": desk.desk_id, "seat_info": desk.get_users_info(), "room_type": validator.room_type.data}


def _apply_match_desk(user_id, session_id, max_player_num=4, room_type=0):
    """
    申请一张匹配桌
    :return: 返回桌子对象, 用户对象
    """
    cur_desk_player_count = [[] for _ in range(max_player_num)]  # 当前桌子人数统计[[desk_id1, ...], [desk_id2, ...]...}
    # num = 0
    for _id, desk in desk_mgr.match_desks.items():
        max_player_num = desk.max_player_num  # 匹配场麻将最大人数默认不变
        if desk.is_full():
            continue
        num = desk.people_count
        if desk.room_type == room_type:
            if num in cur_desk_player_count:
                cur_desk_player_count[num].append(desk)
            else:
                cur_desk_player_count[num] = [desk]

    desk_weight = [100 for _ in range(max_player_num)]
    for i, lst in enumerate(cur_desk_player_count):
        if 0 == len(lst):
            desk_weight[i] = 0
        else:
            desk_weight[i] = desk_weight[i] * (1 + 10 * i)
    desk_weight[0] = 100

    index = weight_choice(desk_weight)
    print("index = ", index)
    if 0 == index:
        # 创建桌子
        desk_id = DBDesk.get_a_id()
        custom_config = GlobalConfig().room_cfg_list[room_type]
        desk = RoomDesk(desk_id, max_player_num=max_player_num, desk_type=DeskType.MATCH_DESK, custom_config=custom_config)
        desk_mgr.add_room_desk(desk)
        user = UserManager().add_user(user_id, desk_id, session_id)
        desk.user_sit(user, seat_id=0)
        return desk, user
    else:
        desk = random.choice(cur_desk_player_count[index])
        user = UserManager().add_user(user_id, desk.desk_id, session_id)
        desk.user_sit(user)
        return desk, user
