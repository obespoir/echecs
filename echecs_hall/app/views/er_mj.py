# coding=utf-8
import json

from app.controller.server_api_controller import room_controller
from app.controller.server_api_controller import login_controller
from app.extensions.blueprint import Blueprint
from app.extensions.globalobject import GlobalObject
from app.models.test_user import TestUser
from app.share.error_code import *
from app.share.message_id import COMMAND_ID_USER_LOGIN, COMMAND_ID_VALIDATE_USER_LOGIN
from .base_handler import BaseHandler

er_mj = Blueprint('api', url_prefix="/mj")


@er_mj.route('/hello', name="hello")
class HelloHandler(BaseHandler):
    def get(self):
        return self.write('hello world')


@er_mj.route('/login', name='login')
class LoginHandler(BaseHandler):
    """
    登录接口
    用户需要提供 user_id , pwd 用于登录游戏服务器
    @:param user_id
    @:param password
    @:return {"code": 200, "info": {"room": "room_1", "old_session": None, "reconnect": False}}
    """

    def get(self):
        return self.write(u"登录接口, 用户需要提供 user_id , pwd 用于登录游戏服务器")

    def post(self):
        user_id = self.get_argument("user_id")
        pwd = self.get_argument("password")
        session_id = self.get_argument("session_id")
        user_in_db = login_controller.validate_user_in_redis(user_id)
        if not user_in_db:
            return self.write(self.get_ret(USER_NOT_IN_DB, COMMAND_ID_USER_LOGIN))
        is_right = login_controller.validate_user_password(user_id, pwd)
        if is_right:

            exist_desk_dict = login_controller.exist_user_desk(user_id)
            if isinstance(exist_desk_dict, str):
                exist_desk_dict = json.loads(exist_desk_dict)
            room_name = login_controller.get_room_name(user_id)
            info = {
                "room": exist_desk_dict.get("room_name", room_name) if exist_desk_dict else "",
                "old_session": exist_desk_dict.get("session_id", "") if exist_desk_dict else "",
                "reconnect": 1 if bool(exist_desk_dict) else 0
            }
            if not exist_desk_dict:
                login_controller.enter_game(user_id, session_id, room_name)
            print("login info=", info)
            return self.write(self.get_ret(SUCCESS, info))
        else:
            return self.write(self.get_ret(PASSWORD_ERROR, COMMAND_ID_USER_LOGIN))


@er_mj.route('/is_login', name="is_login")
class ValidateLogin(BaseHandler):
    """
    验证是否登录
    """

    def get(self):
        session_id = self.get_argument("session_id")
        r = login_controller.is_login(session_id)
        if r:
            return self.write(self.get_ret(SUCCESS, COMMAND_ID_VALIDATE_USER_LOGIN, r))
        else:
            return self.write(self.get_ret(USER_NOT_IN_DB, COMMAND_ID_VALIDATE_USER_LOGIN, r))


@er_mj.route("/join_room", name="join_room")
class JoinRoom(BaseHandler):
    """
    加入房间
    @:param room_typ 房间类型  [0,1,2]
    @:param user_id 用户ID
    @:param session_id 用户session
    """

    def get(self):
        session_id = self.get_argument("session_id")
        user_id = self.get_argument("user_id")
        room_type = int(self.get_argument("room_type"))
        if room_type not in [0, 1, 2]:
            return self.write(self.get_ret(PARAMS_ERROR))
        if room_controller.is_exits_desk(user_id):
            return self.write(self.get_ret(USER_IN_OTHER_DESK))
        code, server_name = room_controller.join_room(session_id, user_id, room_type)
        if code == 0:
            return self.write(self.get_ret(SUCCESS, {"room": server_name}))
        else:
            return self.write(self.get_ret(SUCCESS, {"code": code, "desc": ERROR_CODE_DESC[code]}))


@er_mj.route("/match_room_start_game", name="match_room_start_game")
class MatchRoomStartGame(BaseHandler):
    """
    记录游戏开始相关信息,
    @:param room_typ 房间类型  [0,1,2]
    @:param user_id 用户ID
    @:param session_id 用户session
    """
    def get(self):
        session_id = self.get_argument("session_id")
        user_id = self.get_argument("user_id")
        room_type = int(self.get_argument("room_type"))
        room_name = self.get_argument("room_name")
        r = room_controller.match_room_game_start(session_id, json.loads(user_id), room_name, room_type)
        print("MatchRoomStartGame r=", r)
        if r:
            return self.write(self.get_ret(SUCCESS,{"ret":0}))
        else:
            return self.write(self.get_ret(MATCH_START_GAME_WRITE_ERROR,))


@er_mj.route("/match_room_game_over", name="match_room_game_over")
class MatchRoomGameOver(BaseHandler):
    """
    记录游戏结束相关信息,
    @:param user_id 用户ID
    """
    def get(self):
        user_id = self.get_argument("user_id")
        r = room_controller.match_room_game_over(json.loads(user_id))
        print("MatchRoomGameOver r=", r)
        if r:
            return self.write(self.get_ret(SUCCESS,{"ret":0}))
        else:
            return self.write(self.get_ret(MATCH_GAME_OVER_WRITE_ERROR,))


@er_mj.route("/left_room", name="left_room")
class LeftRoom(BaseHandler):
    """
    退出房间
    """

    def get(self):
        session_id = self.get_argument("session_id")
        user_id = self.get_argument("user_id")
        print("left_room user_id = %s"%user_id)
        r = room_controller.left_room(session_id, json.loads(user_id))
        if r:
            return self.write(self.get_ret(SUCCESS))
        else:
            return self.write(self.get_ret(UNKNOWN_ERROR, ))


@er_mj.route("/restart_delete_room_info", name="restart_delete_room_info")
class RestartDeleteRoomInfo(BaseHandler):
    """
    删除房间
    """

    def get(self):
        r = room_controller.delete_room()
        return self.write(self.get_ret(SUCCESS))


@er_mj.route("/get_hall_room_info")
class GetHallRoomInfo(BaseHandler):
    """
    获取游戏大厅相关信息
    """

    def get(self):
        ret = room_controller.get_hall_room_info()
        return self.write(self.get_ret(SUCCESS, info={"room_cfg_info": ret}))


@er_mj.route("/get_hall_room_info2")
class GetHallRoomInfo2(BaseHandler):
    """
    获取游戏大厅相关信息2
    """

    def get(self):
        ret = GlobalObject().room_cfg_list
        return self.write(self.get_ret(SUCCESS, info={"room_cfg_info": ret}))


@er_mj.route("/get_hall_room_people_count")
class GetHallRoomPeopleCount(BaseHandler):
    """
    获取游戏大厅房间人数
    """

    def get(self):
        ret = room_controller.get_hall_room_people_count()
        print("ret=" , ret)
        return self.write(self.get_ret(SUCCESS, info={"room_people_count": ret}))


@er_mj.route("/init_room_cfg", name="create_room_cfg")
class InitRoomCFG(BaseHandler):
    def get(self):
        ret = room_controller.init_room_cfg()
        return self.write(self.get_ret(SUCCESS, info={"rooms_id": ret}))


@er_mj.route("/create_user", name="create_user")
class CreateUser(BaseHandler):
    def get(self):
        r = TestUser.create("123456","test1","niudun")
        return self.write("ok")




@er_mj.route("/pic_get_name", name="pic_get_name")
class PicGetName(BaseHandler):
    def get(self):
        index = self.get_argument("index")
        if int(index) == 4:
            return self.write("YES")
        else:
            return self.write("No")


