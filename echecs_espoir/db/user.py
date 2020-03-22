# coding:utf-8


from db.mysql.user import User as MysqlUser


class User(object):
    def __init__(self):
        pass

    @classmethod
    def create(cls, passwd, name, nickname, device_id='', phone='', introduction=''):
        """
        创建用户
        :param passwd:
        :param name:
        :param nickname:
        :param device_id:
        :param phone:
        :param introduction:
        :return: 返回新用户id (int)
        """
        return MysqlUser.create(passwd, name, nickname, device_id=device_id, phone=phone, introduction=introduction)

    @classmethod
    def get_user_info_by_id(cls, user_id):
        """
        获取用户信息
        :param user_id:
        :return: 返回用户信息
            {"id": self.id, "name": self.name, "nick_name": self.nick_name, "point": self.point, "phone": self.phone}
        """
        return MysqlUser.get_user_info_by_id(user_id)

    @classmethod
    def validate_passwd_by_name(cls, user_name, passwd):
        """
        验证用户名和密码
        :param user_name:
        :param passwd:
        :return: 0: 验证错误, 1:验证通过
        """
        user_passwd = MysqlUser.get_passwd_by_name(user_name)
        if not user_passwd or user_passwd!=passwd:
            return 0
        return 1

    @classmethod
    def update_user_point(cls, user_id, point_change):
        """
        更改用户积分
        :param user_id:
        :param point_change:
        :return: 返回用户点数 {"point": user.point}
        """
        return MysqlUser.update_user_point(user_id, point_change)




