# coding=utf-8
import requests
import ujson

from service.room.handlers.basehandler import BaseHandler, RegisterEvent
from service.room.validators.friend_desk.dissolve_desk import DissolveDeskValidator
from service.room.models.room_manager import room_mgr
from service.room.models.user_manager import UserManager
from share.message_ids import *
from share.notify_web_server import notify_web_server_restart

print("init dissolve match desk")
notify_web_server_restart()

@RegisterEvent(DISSOLVE_MATCH_DESK)
class DissolveDeskHandler(BaseHandler):

    def execute(self, *args, **kwargs):
        """
        解散二人麻将匹配桌子请求处理
        :param args:
        :param kwargs:
        :return: {need_agree: 0/1} 成功退出时0, 1表示需要其他玩家同意
        """
        print("DissolveDeskHandler!!")
        validator = DissolveDeskValidator(handler=self)
        url = "http://127.0.0.1:8889/mj/left_room"
        print("DissolveDeskHandler desk_user_ids=", validator.desk_user_ids)
        params = {"user_id": ujson.dumps(validator.desk_user_ids), "session_id": validator.session_id.data, "room_type": 0}
        print("DissolveDeskHandler params=", params)
        r = requests.get(url, params)
        print("DissolveDeskHandler r=", r.text)
        # 房主退出, 桌子直接解散
        response_data = {"need_agree": 0}
        validator.desk.notify_player(validator.user.seat_id, DISSOLVE_MATCH_DESK, response_data)

        data = {"user_id": validator.user_id.data, "nick": validator.user.nick_name, "success": 1}
        validator.desk.notify_desk(PUSH_MATCH_DESK_DISSOLVE_RESULT, data)
        room_mgr.del_desk(validator.desk.desk_id)
        UserManager().exit_user(validator.user_id.data)
        return {"need_push": 0}
