# coding=utf-8
from sqlalchemy import Column
from sqlalchemy.types import CHAR, Integer, VARCHAR, BIGINT
from sqlalchemy.orm import relationship, backref
from ..extensions.mysql.mysql_base import Base
from ..extensions.mysql.session import sessionCM


class IncomeSupport(Base):
    __tablename__ = 'income_support'
    id = Column(Integer, primary_key=True, doc='唯一id')
    uid = Column(Integer, doc='用户id')
    collection_time = Column(Integer, doc='领取补助时间')
    income_support_times = Column(Integer, doc='领取补助次数')

    def __init__(self, data):
        self.uid = data['uid']
        self.collection_time = data['collection_time']
        self.income_support_times = data['income_support_times']

    @classmethod
    def get_income_support_by_uid(cls, uid):
        with sessionCM() as session:
            res = session.query(cls).filter(cls.uid == uid).first()
            if res:
                return cls.to_dict(res)
            else:
                return {}

    @classmethod
    def add(cls, data):
        with sessionCM() as session:
            income_support = cls(data)
            session.add(income_support)
            session.flush()
            id = income_support.id
            session.commit()
            if id > 0:
                return id
            else:
                return 0

    @classmethod
    def update_income_support_by_id(cls, id, data):
        with sessionCM() as session:
            try:
                session.query(cls).filter(cls.id == id).update(
                    {cls.collection_time: data['collection_time'],
                     cls.income_support_times: data['income_support_times']}
                )
                session.commit()
                return True
            except Exception:
                return False

    @classmethod
    def to_dict(cls, income_support):
        data = {'id': income_support.id, 'uid': income_support.uid, 'collection_time': income_support.collection_time,
                'income_support_times': income_support.income_support_times}
        return data
