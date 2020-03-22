# coding=utf-8

from service.room.handlers.basehandler import BaseHandler, RegisterEvent
from service.room.validators.friend_desk.create_desk import CreateDeskValidator
from service.room.common_define import DeskType
from service.room.models.user_manager import UserManager
from service.room.models.user import User
from service.room.models.room_desk import RoomDesk
from service.room.models.roomdesk_manager import desk_mgr
# from service.session_gate_rel import session_gate_ins
from db.desk import Desk as DBDesk
from share.message_ids import *


@RegisterEvent(CREATE_FRIEND_DESK)
class CreateDeskHandler(BaseHandler):

    def execute(self, *args, **kwargs):
        """
        创建桌子请求处理
        :param args:
        :param kwargs:
        :return:
        """
        validator = CreateDeskValidator(handler=self)
        desk_id = DBDesk.get_a_id()
        # user = User(validator.user_id.data, desk_id, session_id=validator.session_id.data)
        # UserManager().add_user(user)
        user = UserManager().add_user(validator.user_id.data, desk_id, validator.session_id.data)
        # session_gate_ins.update_rel(validator.session_id.data, self.gate_name)
        desk = RoomDesk(desk_id, max_player_num=4, desk_type=DeskType.FRIEND_DESK)
        desk_mgr.add_room_desk(desk)
        desk.user_sit(user, seat_id=0)

        return {"desk_id": desk_id, "seat_id": 0}
