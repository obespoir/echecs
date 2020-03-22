# coding=utf-8
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import CHAR, Integer, VARCHAR, BIGINT, TEXT
from sqlalchemy.orm import relationship,backref

from ..extensions.mysql.mysql_base import Base
from ..extensions.mysql.session import sessionCM


class EmailInfo(Base):
    __tablename__ = 'email_info'
    id = Column(Integer, primary_key=True, doc='邮件id')
    title = Column(VARCHAR(64), doc='邮件标题')
    content = Column(TEXT(1000), doc='邮件内容')
    create_time = Column(Integer, doc='创建时间')
    reward_id = Column(VARCHAR(100), doc='奖励id')
    author = Column(VARCHAR(64), doc='发送人')
    icon = Column(VARCHAR(200), doc='邮件图标')
    status = Column(Integer, doc='判断此邮件信息是否可用')

    @classmethod
    def get_email_info_by_id(cls, id):
        with sessionCM() as session:
            res = session.query(cls).filter(cls.id == id).first()
            return cls.to_dict(res)

    @classmethod
    def get_all_email_info(cls):
        data = []
        with sessionCM() as session:
            res = session.query(cls).filter(cls.status == 1).all()
            for item in res:
                data.append(cls.to_dict(item))
            return data

    @classmethod
    def to_dict(cls, email_info):
        data = {'id': email_info.id, 'title': email_info.title, 'content': email_info.content,
                'create_time': email_info.create_time, 'reward_id': email_info.reward_id,
                'author': email_info.author, 'icon': email_info.icon}
        return data
