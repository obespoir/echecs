# coding=utf-8
from sqlalchemy import Column
from sqlalchemy.types import CHAR, Integer, VARCHAR, BIGINT
from sqlalchemy.orm import relationship, backref
from ..extensions.mysql.mysql_base import Base
from ..extensions.mysql.session import sessionCM


class PropInfo(Base):
    __tablename__ = 'prop_info'
    id = Column(Integer, primary_key=True, doc='道具id')
    name = Column(VARCHAR(64), doc='道具名称')
    desc = Column(VARCHAR(200), doc='道具描述')
    icon = Column(VARCHAR(200), doc='道具图标')
    create_time = Column(Integer, doc='创建时间')

    @classmethod
    def get_all_prop_info(cls):
        data = []
        with sessionCM() as session:
            res = session.query(cls).filter().all()
            for item in res:
                data.append(cls.to_dict(item))
            return data

    @classmethod
    def to_dict(cls, prop_info):
        data = {'id': prop_info.id, 'name': prop_info.name, 'desc': prop_info.desc, 'icon': prop_info.icon,
                'create_time': prop_info.create_time}
        return data
