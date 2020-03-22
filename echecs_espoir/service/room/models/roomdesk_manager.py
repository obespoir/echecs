# coding=utf-8

__author__ = 'jamon'

from service.room.common_define import DeskType


class DeskManager(object):
    """
    管理房间中不同桌游戏
    """
    def __init__(self):
        self._room_desks = {}
        self.match_desks = {}

    def add_room_desk(self, room_desk):
        self._room_desks[room_desk.desk_id] = room_desk
        if room_desk.desk_type == DeskType.MATCH_DESK:
            self.match_desks[room_desk.desk_id] = room_desk

    def del_room_desk(self, desk_id):
        desk = self._room_desks.pop(desk_id, None)
        if desk.desk_type == DeskType.MATCH_DESK:
            self.match_desks.pop(desk_id)

    def get_room_desk(self, desk_id):
        return self._room_desks.get(desk_id, None)

    def exit_user(self, desk_id, user_id):
        desk = self.get_room_desk(desk_id)
        if desk.user_exit(user_id):
            return True
        return False

    def notify_player(self, desk_id, seat_id, command_id, data, code=200):
        """
        通知桌子上的单个玩家
        """
        desk = self.get_room_desk(desk_id)
        if desk:
            desk.notify_player(seat_id, command_id, data, code)


    def notify_desk(self, desk_id, command_id, data):
        """
        通知桌子上的所有玩家
        """
        print("notify_desk = ", data)
        desk = self.get_room_desk(desk_id)
        if desk:
            desk.notify_desk(command_id, data)

    def notify_desk_game_over(self, desk_id):
        """
        通知桌子游戏结束用于改变桌子状态
        """
        desk = self.get_room_desk(desk_id)
        if desk:
            desk.game_over()

    def notify_settle_data(self, desk_id, data):
        """
        游戏通知桌子，给予结算数据
        :param desk_id:
        :param data:
        :return:
        """
        desk = self.get_room_desk(desk_id)
        if desk:
            desk.notify_settle_data(data)


desk_mgr = DeskManager()