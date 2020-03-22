# coding=utf-8

"""

"""
from db.mysql.user import User as MUser
from service.room.common_define import UserStatus
from obespoir.share.ob_log import logger


class User(object):
    def __init__(self, user_id, desk_id, session_id=""):
        self.user_id = user_id
        self.desk_id = desk_id
        self.session_id = session_id
        self.seat_id = -1
        self.is_offline = 0
        self.status = UserStatus.UNREADY

        self.point = 0
        self.user_name = ""
        self.nick_name = ""
        self.update()

    def to_dict(self):
        return {"user_id": self.user_id, "nick": self.nick_name,
                "point": self.point, "status": self.status, "seat_id": self.seat_id}

    def update(self):
        info = MUser.get_user_info_by_id(self.user_id)
        if info:
            self.point = info.get("money", 0)
            self.user_name = info.get("name", "")
            self.nick_name = info.get("nick_name", "")
        else:
            logger.warning("update user({0}) error!".format(self.user_id))

    def set_seat_id(self, seat_id):
        self.seat_id = seat_id

    def set_user_point(self, change_num):
        self.point += change_num
        ret, info = MUser.update_user_point(self.user_id, change_num)

        if self.point != info.get("point", ""):
            logger.error("set_user_point error! ({0}, {1})".format(self.user_id, change_num))
        return self.point

    def set_status(self, status):
        self.status = status

    def set_offline(self):
        self.is_offline = 1

    def can_leave_desk(self):
        """
        离开桌子
        :return: 0: 不能离开, 1： 能够离开
        """
        if UserStatus.PLAYING == self.status:
            return False
        return True

