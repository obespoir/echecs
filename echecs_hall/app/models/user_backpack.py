# coding=utf-8
from sqlalchemy import Column
from sqlalchemy.types import CHAR, Integer, VARCHAR, BIGINT
from sqlalchemy.orm import relationship, backref
from ..extensions.mysql.mysql_base import Base
from ..extensions.mysql.session import sessionCM

class UserBackpack(Base):
    __tablename__ = 'user_backpack'
    id = Column(Integer, primary_key=True, doc='背包id')
    uid = Column(Integer, doc='用户id')
    prop_id = Column(Integer, doc='道具id')
    count = Column(Integer, doc='道具数量')
    create_time = Column(Integer, doc='创建时间')
    status = Column(Integer, doc='道具状态，0 不可用 1 可用')

    @classmethod
    def validate_user_backpack_in_table(cls, uid):
        with sessionCM() as session:
            res = session.query(cls).filter(cls.uid == uid).all()
            if len(res) > 0:
                return True
            else:
                return False

    @classmethod
    def get_user_backpack_by_uid(cls, uid):
        data = []
        with sessionCM() as session:
            res = session.query(cls).filter(cls.uid == uid).all()
            if res:
                for item in res:
                    data.append(cls.to_dict(item))
            else:
                data = []
            return data

    @classmethod
    def to_dict(cls, user_backpack):
        data = {'id': user_backpack.id, 'uid': user_backpack.uid, 'prop_id': user_backpack.prop_id,
                'count': user_backpack.count, 'create_time': user_backpack.create_time,
                'status': user_backpack.status}
        return data

