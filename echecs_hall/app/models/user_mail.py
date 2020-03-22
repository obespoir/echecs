# coding=utf-8
from sqlalchemy import Column
from sqlalchemy.types import CHAR, Integer, VARCHAR, BIGINT
from sqlalchemy.orm import relationship, backref
from ..extensions.mysql.mysql_base\
    import Base
from ..extensions.mysql.session import sessionCM
from app.models.user_info import UserInfo
from ..extensions.common import md5
import time


class UserMail(Base):
    __tablename__ = 'user_email'
    id = Column(Integer, primary_key=True, doc='用户邮件id')
    uid = Column(Integer, doc='用户id')
    eid = Column(Integer, doc='邮件详情id')
    is_read = Column(Integer, doc='是否已读(0 未读 1 已读)')
    is_receive = Column(Integer, doc='是否已接 (0 未接 1 已接)')
    send_date = Column(Integer, doc='发送时间')
    update_date = Column(Integer, doc='邮件更新时间')
    sender = Column(VARCHAR(64), doc='发送人')

    @classmethod
    def validate_user_mail_in_table(cls, uid):
        with sessionCM() as session:
            res = session.query(cls).filter(cls.uid == uid).all()
            if len(res) > 0:
                return True
            else:
                return False

    @classmethod
    def update_user_mail_by_id(cls, id, data):
        with sessionCM() as session:
            try:
                session.query(cls).filter(cls.id == id).update(
                    {cls.is_read: data['is_read'], cls.update_date: time.time()}
                )
                session.commit()
                return True
            except Exception:
                return False

    @classmethod
    def get_user_mail_by_uid(cls, uid):
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
    def get_one_user_mail_by_id(cls, id):
        with sessionCM() as session:
            res = session.query(cls).filter(cls.id == id).first()
            if res:
                return cls.to_dict(res)
            else:
                return {}

    @classmethod
    def to_dict(cls, user_email):
        data = {'id': user_email.id, 'uid': user_email.uid, 'eid': user_email.eid,
                'is_read': user_email.is_read, 'is_receive': user_email.is_receive,
                'send_date': user_email.send_date, 'update_date': user_email.update_date,
                'sender': user_email.sender}
        return data
