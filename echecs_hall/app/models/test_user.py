# coding:utf-8


from sqlalchemy import Column
from sqlalchemy.types import CHAR, Integer, VARCHAR, BIGINT

from ..extensions.mysql.mysql_base import Base
from ..extensions.mysql.session import sessionCM


class TestUser(Base):
    __tablename__ = 'iw_user'

    id = Column(Integer, autoincrement=True, nullable=False, unique=True, primary_key=True)
    name = Column(VARCHAR(255), index=True)  # or Column(String(30))
    nick_name = Column(VARCHAR(255), index=True)
    passwd = Column(CHAR(32))
    phone = Column(VARCHAR(20), index=True, default="")
    device_id = Column(VARCHAR(50))
    point = Column(BIGINT)

    def __init__(self, passwd, name, nickname, device_id='', phone='', introduction=''):
        self.name = name
        self.nickname = nickname
        self.passwd = passwd
        self.phone = phone
        self.device_id = device_id
        self.point = 0
        self.introduction = introduction

    def to_dict(self):
        return {"id": self.id, "name": self.name, "nick_name": self.nick_name,
                "point": self.point, "phone": self.phone}

    @classmethod
    def create(cls, passwd, name, nickname, device_id='', phone='', introduction=''):
        with sessionCM() as session:
            user = session.query(TestUser).filter_by(name=name).first()
            if user:
                return 0
            new_user = cls(passwd, name, nickname, device_id, phone, introduction=introduction)
            session.add(new_user)
            session.commit()
            return new_user.id

    @classmethod
    def get_user_info_by_id(cls, user_id):
        with sessionCM() as session:
            user = session.query(TestUser).filter_by(id=user_id).first()
            return user.to_dict if user else {}

    @classmethod
    def validate_password(cls,user_id, pwd):
        with sessionCM() as session:
            user = session.query(TestUser).filter_by(id=user_id).first()
            print("user =", user)
            return user.passwd == pwd


    @classmethod
    def get_passwd_by_name(cls, user_name):
        with sessionCM() as session:
            user = session.query(TestUser).filter_by(id=user_name).first()
            return user.passwd if user else ""

    @classmethod
    def del_user(cls, user_id):
        """
        删除用户，慎用!!!!!!!!!!!!!!!
        :param accid:
        :return:
        """
        with sessionCM() as session:
            session.query(TestUser).filter_by(id=user_id).delete()
            session.commit()
            return 1

    @classmethod
    def update_user_point(cls, user_id, point_change):
        with sessionCM() as session:
            user = session.query(TestUser).filter_by(id=user_id).with_for_update(read=False).first()
            if user:
                user.point += point_change
                session.commit()
                return {"point": user.point}
            return {}




