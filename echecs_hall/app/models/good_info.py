# coding=utf-8
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import CHAR, Integer, VARCHAR, BIGINT, TEXT, FLOAT
from sqlalchemy.orm import relationship,backref

from ..extensions.mysql.mysql_base import Base
from ..extensions.mysql.session import sessionCM


class GoodInfo(Base):
    __tablename__ = 'good_info'
    id = Column(Integer, primary_key=True, doc='商品id')
    name = Column(VARCHAR(64), doc='商品名称')
    desc = Column(VARCHAR(100), doc='商品描述')
    type = Column(Integer, doc='商品类型 (1 金币)')
    selling_price = Column(Integer, doc='购买所需钻石')
    rmb_price = Column(FLOAT, doc='RMB价值')
    quantity = Column(Integer, doc='商品数量')
    prop_id = Column(Integer, doc='道具id')
    icon = Column(VARCHAR(200), doc='商品图标')
    status = Column(Integer, doc='商品状态')
    create_time = Column(Integer, doc='创建时间')
    update_time = Column(Integer, doc='修改时间')

    @classmethod
    def get_good_info_by_id(cls, id):
        with sessionCM() as session:
            res = session.query(cls).filter(cls.id == id).first()
            if res:
                return cls.to_dict(res)
            else:
                return {}

    @classmethod
    def get_all_good_info(cls):
        data = []
        with sessionCM() as session:
            res = session.query(cls).filter(cls.status == 1).all()
            if len(res) > 0:
                for item in res:
                    data.append(cls.to_dict(item))
            return data

    @classmethod
    def to_dict(cls, good_info):
        data = {'id': good_info.id, 'name': good_info.name, 'desc': good_info.desc, 'type': good_info.type,
                'selling_price': good_info.selling_price, 'rmb_price': good_info.rmb_price,
                'quantity': good_info.quantity, 'prop_id': good_info.prop_id, 'icon': good_info.icon,
                'status': good_info.status, 'create_time': good_info.create_time, 'update_time': good_info.update_time}
        return data
