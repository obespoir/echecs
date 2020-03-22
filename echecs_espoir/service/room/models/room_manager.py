# coding=utf-8

from service.room.models.user_manager import UserManager
from service.room.models.roomdesk_manager import desk_mgr


class RoomManager(object):
    """
    房间管理类,包括所有类型房间
    """
    def __init__(self):
        pass

    def get_desk_by_user_id(self, user_id):
        desk_id = UserManager().get_user_by_id(user_id).desk_id
        return desk_mgr.get_room_desk(desk_id)

    def user_exit(self, user_id):
        desk_id = UserManager().get_user_by_id(user_id)
        if desk_mgr.exit_user(desk_id, user_id):
            return UserManager().exit_user(user_id)
        return 0

    def del_desk(self, desk_id):
        """
        解散桌子
        :param desk_id:
        :return:
        """
        desk = desk_mgr.get_room_desk(desk_id)
        desk_mgr.del_room_desk(desk_id)
        for user in desk.users:
            if user:
                UserManager().exit_user(user.user_id)


room_mgr = RoomManager()