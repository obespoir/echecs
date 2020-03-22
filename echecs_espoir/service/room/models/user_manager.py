# coding=utf-8

"""

"""

from obespoir.share.singleton import Singleton

from service.room.models.user import User


class UserManager(object, metaclass=Singleton):

    def __init__(self):
        self._session_user_dict = {}      # session_id -> user
        self._id_user_dict = {}           # user_id -> user

    def add_user(self, user_id, desk_id, session_id):
        """
        添加用户, 返回user对象
        :param user_id:
        :param desk_id:
        :param session_id:
        :return:
        """
        if self._id_user_dict.get(user_id, None):
            # 断线重连, 更新session_id
            print("add_userrrrrrrrrrrrrrrrrrrrrr:", user_id, desk_id)
            old_session_id = self._id_user_dict[user_id].session_id
            self._id_user_dict[user_id].session_id = session_id
            if old_session_id in self._session_user_dict.keys():
                self._session_user_dict.pop(old_session_id)
            self._session_user_dict[session_id] = self._id_user_dict[user_id]
            return self._id_user_dict[user_id]
        else:
            user = User(user_id, desk_id, session_id)
            self._id_user_dict[user_id] = user
            if session_id not in self._session_user_dict.keys():
                self._session_user_dict[session_id] = user
            return user

    def offline_user(self, session_id):
        if session_id in self._session_user_dict.keys():
            self._id_user_dict[int(self._session_user_dict[session_id].user_id)].session_id = None
            self._session_user_dict.pop(session_id)

    def exit_user(self, user_id):
        if user_id in self._id_user_dict.keys():
            session_id = self._id_user_dict[user_id].session_id
            if session_id in self._session_user_dict.keys():
                self._session_user_dict.pop(session_id)
            self._id_user_dict.pop(user_id)
        return 1

    def get_user_by_id(self, user_id):
        return self._id_user_dict.get(user_id, None)

    def get_user_by_sessionid(self, session_id):
        return self._session_user_dict.get(session_id, None)

    def get_session_list(self):
        """
        获取当前游戏在线用户会话列表
        """
        session_list = []
        for k, v in self._id_user_dict.items():
            session_list.append(v.session_id)
        return session_list

    def get_session_id_user_id_list(self):
        """
        获取当前用户session userid username list表
        :return:
        """
        session_list = []
        for k, v in self._id_user_dict.items():
            session_list.append(str(k)+":"+v.session_id)
        return session_list
