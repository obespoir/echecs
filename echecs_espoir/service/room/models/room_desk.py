# coding=utf-8

__author__ = 'jamon'


from obespoir.share.ob_log import logger
from share.message_ids import PUSH_GAME_SETTLE, PUSH_GAME_OVER
from share.notify_web_server import notify_web_server_match_room_game_over
from service.room.common_define import DeskStatus, DeskType
from service.push_service import push_msg
from service.room.notifybridge import start_game, get_reconnect_desk_info
from service.room.common_define import UserStatus


class RoomDesk(object):
    """
    房间桌子
    """
    def __init__(self, desk_id, max_player_num, desk_type=DeskType.FRIEND_DESK, custom_config={}):
        self.desk_id = desk_id
        self.desk_type = desk_type
        self.max_player_num = max_player_num
        self.can_play_num = 1                 # 当桌当轮最大可玩局数
        self.cur_play_num = 1                 # 当前正在第几局
        self.users = [None for _ in range(max_player_num)]
        self.status = DeskStatus.READY
        self.owner_seat = 0                   # 房主座位位置, 默认为第一个进入桌子的玩家

        self.dissolve_agreed_users = []       # 同意解散房间的用户id
        self.dissolve_reject_users = []       # 拒绝解散房间的用户id

        self.custom_config = custom_config               # 自定义配置
        self.room_type = custom_config.get("room_type", 0)

    @property
    def owner(self):
        return self.users[self.owner_seat]

    @property
    def people_count(self):
        num = 0
        for user in self.users:
            if user:
                num += 1
        return num

    def get_desk_info(self):
        return {
            "desk_id": self.desk_id,
            "users": self.get_users_info(),
            "custom_config": self.custom_config
        }

    def get_users_info(self):
        """获取桌子中玩家的基本信息"""
        info = []
        for i, user in enumerate(self.users):
            if user:
                info.append(user.to_dict())
        return info

    def is_last_round(self):
        """是否当轮最后一局"""
        return self.can_play_num == self.cur_play_num

    def is_full(self):
        num = 0
        for user in self.users:
            if user:
                num += 1
        return num == self.max_player_num

    def is_in_desk(self, user_id):
        for u in self.users:
            if u and u.user_id == user_id:
                return 1
        return 0

    def user_sit(self, user, seat_id=-1):
        """
        用户进入桌子
        :param user: user object
        :param seat_id: int, -1时表示自动安排座位
        :return:
        """
        if self.is_in_desk(user.user_id):
            return 1

        if 0 <= seat_id:
            if not self.users[seat_id]:
                self.users[seat_id] = user
                user.set_seat_id(seat_id)
                return 1
        else:
            for seat in range(self.max_player_num):
                if not self.users[seat]:
                    self.users[seat] = user
                    user.set_seat_id(seat)
                    return 1
        return 0

    def user_exit(self, user_id):
        for i, u in enumerate(self.users):
            if not u:
                continue
            if u.user_id == user_id:
                self.users[i] = None
        return 1

    def set_custom_config(self, custom_config):
        self.custom_config = custom_config

    def start_game(self):
        self.status = DeskStatus.PLAYING
        start_game(self.desk_id, custom_config=self.custom_config)

    def game_over(self):
        # 改变桌子自己状态
        self.status = DeskStatus.OVER
        # 改变桌子内每个玩家的用户状态
        for i in range(self.max_player_num):
            self.users[i].status = UserStatus.UNREADY

    def get_reconnect_info(self, seat_id):
        return get_reconnect_desk_info(self.desk_id, seat_id)

    def notify_player(self, seat_id, command_id, data, code=200):
        """
        通知单个玩家
        :param seat_id:
        :param command_id:
        :param data:
        :return:
        """
        if self.users[seat_id]:
            push_msg(command_id, data, [self.users[seat_id].session_id], code)
        else:
            logger.error("room_desk->notify_player-> self.user[%s] = None"%str(seat_id))

    def notify_desk(self, command_id, data):
        """
        通知桌子上的所有玩家
        """
        session_list = []
        user_ids = []
        for i in range(self.max_player_num):
            if self.users[i]:
                session_list.append(self.users[i].session_id)
                user_ids.append(self.users[i].user_id)
        if command_id == PUSH_GAME_OVER and self.desk_type == DeskType.MATCH_DESK:
            notify_web_server_match_room_game_over(user_ids)


        session_list = [self.users[seat_id].session_id for seat_id in range(self.max_player_num) if self.users[seat_id]]
        push_msg(command_id, data, session_list)

    def notify_settle_data(self, data):
        """
        游戏通知桌子，给予结算数据
        :param data:
        :return:
        """
        # TODO 需要对结算数据进行封装，添加上用户个人信息
        data = data
        self.notify_desk(PUSH_GAME_SETTLE, data)

    def notify_desk_some_user(self, command_id, data, exclude_user=[]):
        """
        通知桌子上的所有玩家
        :param command_id:
        :param data:
        :param exclude_user: 不进行通知的玩家user_id
        :return:
        """
        session_list = [self.users[seat_id].session_id for seat_id in range(self.max_player_num)
                        if self.users[seat_id] and self.users[seat_id].user_id not in exclude_user]
        push_msg(command_id, data, session_list)





