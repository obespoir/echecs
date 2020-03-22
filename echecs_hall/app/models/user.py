#!/usr/bin/env python
# coding=utf-8

from sqlalchemy import Column
from sqlalchemy.types import CHAR, Integer, VARCHAR, BIGINT
from sqlalchemy.orm import relationship, backref
from ..extensions.mysql.mysql_base import Base
from ..extensions.mysql.session import sessionCM
from app.models.user_info import UserInfo
from ..extensions.common import md5


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

    def __init__(self, data):
        self.bsfb_id = data['bsfb_id']
        self.nick_name = data['nick_name']
        self.user_name = data['user_name']
        self.password = data['password']
        self.sex = data['sex']
        self.avater_url = data['avater_url']
        self.salt = data['salt']
        self.status = data['status']
        self.skey = data['skey']
        self.register_time = data['register_time']
        self.login_time = data['login_time']
        self.logout_time = data['logout_time']
        self.register_ip = data['register_ip']
        self.login_ip = data['login_ip']
        self.is_visitor = data['is_visitor']
        self.is_vip = data['is_vip']
        self.is_robot = data['is_robot']

    @classmethod
    def add(cls, data):
        with sessionCM() as session:
            user = cls(data)
            session.add(user)
            session.flush()
            user_id = user.id
            session.commit()
            if user_id > 0:
                return user_id
            else:
                return 0

    @classmethod
    def check_user_is_exist(cls, username):
        username = str(username)
        with sessionCM() as session:
            res = session.query(cls).join(UserInfo, isouter=True).filter(cls.user_name == username).all()
            if len(res) > 0 and len(res) == 1:
                return True
            else:
                return False

    @classmethod
    def get_user_info_by_username(cls, username):
        username = str(username)
        with sessionCM() as session:
            res = session.query(cls).join(UserInfo).filter(cls.user_name == username).first()
            if res:
                return cls.to_dict(res)
            else:
                return {}

    @classmethod
    def validate_password(cls, username, password):
        passwd = password if 32 == len(password) else md5(password + '123456')
        with sessionCM() as session:
            res = session.query(cls).join(UserInfo, isouter=True).filter(cls.user_name == username).first()
            return res.password == passwd

    @classmethod
    def validate_password_for_id(cls, user_id, password):
        passwd = password if 32 == len(password) else md5(password + '123456')
        with sessionCM() as session:
            res = session.query(cls).join(UserInfo, isouter=True).filter(cls.id == user_id).first()
            return res.password == passwd

    @classmethod
    def validate_user_status(cls, uid):
        with sessionCM() as session:
            res = session.query(cls).join(UserInfo, isouter=True).filter(cls.id == uid).first()
            if res.status:
                return True
            else:
                return False


    @classmethod
    def get_info_by_uid(cls, uid):
        with sessionCM() as session:
            res = session.query(cls).filter(cls.id == uid).first()
            if res:
                return cls.to_dict(res)
            else:
                return {}

    @classmethod
    def get_user_money(cls, uid):
        with sessionCM() as session:
            user_info = session.query(cls).join(UserInfo).filter(cls.id == uid).first()
            if user_info:
                return user_info.user_info_property.money
            else:
                return 0


    @classmethod
    def to_dict(cls, player):
        data = {'uid': player.id, 'bsfb_id': player.bsfb_id, 'nick_name': player.nick_name, 'user_name': player.user_name,
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


