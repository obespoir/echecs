# coding=utf-8
from sqlalchemy import Column
from sqlalchemy.types import CHAR, Integer, VARCHAR, BIGINT
from sqlalchemy.orm import relationship, backref
from ..extensions.mysql.mysql_base import Base
from ..extensions.mysql.session import sessionCM


class RewardInfo(Base):
    __tablename__ = 'reward_info'
    id = Column(Integer, primary_key=True, doc='奖励id')
    prop_id = Column(Integer, doc='道具id')
    reward_quantity = Column(Integer, doc='奖励道具数量')
    create_time = Column(Integer, doc='创建时间')

    @classmethod
    def get_all_reward_info(cls):
        data = []
        with sessionCM() as session:
            res = session.query(cls).filter().all()
            for item in res:
                data.append(cls.to_dict(item))
            return data

    @classmethod
    def to_dict(cls, reward_info):
        data = {'id': reward_info.id, 'prop_id': reward_info.prop_id, 'reward_quantity': reward_info.reward_quantity,
                'create_time': reward_info.create_time}
        return data

