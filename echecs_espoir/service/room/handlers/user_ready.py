# coding=utf-8
from obespoir.base.global_object import GlobalObject

from service.room.handlers.basehandler import BaseHandler, RegisterEvent
from service.room.validators.user_ready import UserReadyValidator
from service.room.common_define import DeskStatus, UserStatus
from service.room.models.room_manager import room_mgr
from share.message_ids import *
from share.notify_web_server import notify_web_server_match_room_start_game


@RegisterEvent(USER_READY)
class UserReadyHandler(BaseHandler):

    def execute(self, *args, **kwargs):
        """
        用户准备/取消准备
        :param args:
        :param kwargs:
        :return:
        """
        print("readddddddddddy:", self.params)
        validator = UserReadyValidator(handler=self)

        if 1 == validator.ready.data:
            validator.user.set_status(UserStatus.READY)
        else:
            validator.user.set_status(UserStatus.UNREADY)
        print("readddddddddddy2222222:", self.params)
        data = {"user_id": validator.user.user_id, "nick": validator.user.nick_name,
                "ready": validator.ready.data, "seat_id": validator.user.seat_id}
        validator.desk.notify_desk_some_user(PUSH_USER_READY, data, [validator.user.user_id])

        response_data = {"ready": validator.ready.data}
        validator.desk.notify_player(validator.user.seat_id, USER_READY, response_data)
        print("readddddddddddy222222233333:", self.params)
        # 当所有玩家都准备好时，默认触发游戏开始
        all_ready = 1
        for u in validator.desk.users:
            if not u or u.status == UserStatus.UNREADY:
                all_ready = 0
                break
        print("allllllllllll_ready:", all_ready)
        if all_ready:
            # 通知web服务器记录是否开始
            user_ids = []
            for i in validator.desk.users:
                user_ids.append(i.user_id)
            ret = notify_web_server_match_room_start_game(user_ids,
                                              validator.session_id.data,
                                              room_name=GlobalObject().name,
                                              room_type=validator.desk.room_type)
            print("readddddddddddy222222244444444:", self.params)
            if ret.get("ret") == 0:
                validator.desk.start_game()
            else:
                raise Exception("start game error ret=%s" % ret)

        return {"need_push": 0}
