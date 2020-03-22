# coding=utf-8
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import CHAR, Integer, VARCHAR, BIGINT
from sqlalchemy.orm import relationship,backref

from ..extensions.mysql.mysql_base import Base
from ..extensions.mysql.session import sessionCM


class UserInfo(Base):
    __tablename__ = 'user_info'
    id = Column(Integer, primary_key=True, doc='唯一id')
    uid = Column(Integer, ForeignKey('user.id'), doc='用户id')
    login_days = Column(Integer, doc='连续登录天数')
    is_get_login_reward = Column(Integer, doc='是否领取连续登录的奖励')
    platform_type = Column(Integer, doc='平台类型 0 安卓平台 1 IOS平台')
    imei = Column(VARCHAR(64), doc='设备型号')
    device_num = Column(VARCHAR(64), doc='设备号')
    agent = Column(VARCHAR(64), doc='代理商')
    payment = Column(Integer, doc='支付方式(1 宝石 2 微信支付 3 支付宝支付 4 苹果支付)')
    point = Column(Integer, doc='用户积分')
    diamond = Column(Integer, doc='用户钻石')
    money = Column(Integer, doc='用户金币')
    can_change_nickname = Column(Integer, doc='是否能修改昵称')
    need_binding = Column(Integer, doc='是否绑定')
    phone = Column(VARCHAR(64), doc='玩家电话')
    user_property = relationship('User', back_populates="user_info_property")

    def __init__(self, data):
        self.uid = data['uid']
        self.login_days = data['login_days']
        self.is_get_login_reward = data['is_get_login_reward']
        self.platform_type = data['platform_type']
        self.imei = data['imei']
        self.device_num = data['device_num']
        self.agent = data['agent']
        self.payment = data['payment']
        self.point = data['point']
        self.diamond = data['diamond']
        self.money = data['money']
        self.can_change_nickname = data['can_change_nickname']
        self.need_binding = data['need_binding']
        self.phone = data['phone']

    @classmethod
    def add(cls, data):
        with sessionCM() as session:
            user_info = cls(data)
            session.add(user_info)
            session.flush()
            user_info_id = user_info.id
            session.commit()
            if user_info_id > 0:
                return user_info_id
            else:
                return 0