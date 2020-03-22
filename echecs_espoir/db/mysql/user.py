# coding:utf-8


from db.mysql.session import sessionCM
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import CHAR, Integer, VARCHAR, BIGINT

from db.mysql.user_info import UserInfo
from db.mysql.base import Base


class User(Base):
    __tablename__ = 'user'


    id = Column(Integer, primary_key=True, doc='用户id')
    bsfb_id = Column(Integer, doc='宝石平台用户唯一id')
    nick_name = Column(VARCHAR(64), doc='昵称')
    user_name = Column(VARCHAR(64), doc='用户名')
    password = Column(VARCHAR(64), doc='用户密码')
    sex = Column(Integer, doc='性别 1：男 2：女')
    avater_url = Column(VARCHAR(200), doc='头像url地址')
    salt = Column(VARCHAR(64), doc='用户登录密码（加长码）')
    status = Column(Integer, doc='状态 1表示可用 0表示不可用（禁号')
    skey = Column(VARCHAR(64), doc='会话session key')
    register_time = Column(Integer, doc='注册时间')
    login_time = Column(Integer, doc='登录时间')
    logout_time = Column(Integer, doc='最后活动时间')
    register_ip = Column(VARCHAR(64), doc='注册ip')
    login_ip = Column(VARCHAR(64), doc='登录ip')
    is_visitor = Column(Integer, doc='是否游客')
    is_vip = Column(Integer, doc='是否vip 0普通玩家 1vip玩家')
    is_robot = Column(Integer, doc='是否为机器人')
    user_info_property = relationship('UserInfo', uselist=False, back_populates='user_property')

    def __init__(self, passwd, name, nickname, device_id='', phone='', introduction=''):
        self.name = name
        self.nickname = nickname
        self.passwd = passwd
        self.phone = phone
        self.device_id = device_id
        self.point = 0
        self.introduction = introduction

    def to_dict(self):
        return {"id": self.id, "name": self.user_name, "nick_name": self.nick_name,
                "money": self.user_info_property.money, "phone": self.user_info_property.phone}

    @classmethod
    def create(cls, passwd, name, nickname, device_id='', phone='', introduction=''):
        with sessionCM() as session:
            user = session.query(User).filter_by(name=name).first()
            if user:
                return 0
            new_user = cls(passwd, name, nickname, device_id, phone, introduction=introduction)
            session.add(new_user)
            session.commit()
            return new_user.id

    @classmethod
    def get_user_info_by_id(cls, user_id):
        with sessionCM() as session:
            user = session.query(User).filter_by(id=user_id).first()
            return user.to_dict() if user else {}

    @classmethod
    def get_passwd_by_name(cls, user_name):
        with sessionCM() as session:
            user = session.query(User).filter_by(id=user_name).first()
            return user.passwd if user else ""

    @classmethod
    def del_user(cls, user_id):
        """
        删除用户，慎用!!!!!!!!!!!!!!!
        :param accid:
        :return:
        """
        with sessionCM() as session:
            session.query(User).filter_by(id=user_id).delete()
            session.commit()
            return 1

    @classmethod
    def update_user_point(cls, user_id, point_change):
        with sessionCM() as session:
            user = session.query(User).filter_by(id=user_id).with_for_update(read=False).first()
            if user:
                user.point += point_change
                session.commit()
                return {"point": user.point}
            return {}


    @classmethod
    def to_dict_static(cls, player):
        data = {'uid': player.id, 'bsfb_id': player.bsfb_id, 'nick_name': player.nick_name,
                'user_name': player.user_name,
                'password': player.password, 'sex': player.sex, 'avater_url': player.avater_url,
                'salt': player.salt, 'status': player.status, 'skey': player.skey,
                'register_time': player.register_time, 'login_time': player.login_time,
                'logout_time': player.logout_time, 'register_ip': player.register_ip,
                'login_ip': player.login_ip, 'is_visitor': player.is_visitor, 'is_vip': player.is_vip,
                'is_robot': player.is_robot, 'login_days': player.user_info_property.login_days,
                'is_get_login_reward': player.user_info_property.is_get_login_reward,
                'platform_type': player.user_info_property.platform_type, 'imei': player.user_info_property.imei,
                'device_num': player.user_info_property.device_num, 'agent': player.user_info_property.agent,
                'payment': player.user_info_property.payment, 'point': player.user_info_property.point,
                'diamond': player.user_info_property.diamond, 'money': player.user_info_property.money,
                'can_change_nickname': player.user_info_property.can_change_nickname,
                'need_binding': player.user_info_property.need_binding, 'phone': player.user_info_property.phone}
        return data


