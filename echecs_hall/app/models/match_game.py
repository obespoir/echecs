# coding=utf-8
from sqlalchemy import Column
from sqlalchemy.types import CHAR, Integer, VARCHAR, BIGINT
from sqlalchemy.orm import relationship, backref
from ..extensions.mysql.mysql_base import Base
from ..extensions.mysql.session import sessionCM
from app.models.user_info import UserInfo
from ..extensions.common import md5


class MatchGame(Base):
    __tablename__ = 'match_game'
    id = Column(Integer, primary_key=True, doc='唯一id')
    uid = Column(Integer, doc='用户id')
    win_count = Column(Integer, doc='用户赢的局数')
    lose_count = Column(Integer, doc='用户输的局数')
    winning_streak = Column(Integer, doc='用户连胜数')
    highest_winning_streak = Column(Integer, doc='用户最高连胜')

    @classmethod
    def validate_match_data_in_table(cls, uid):
        with sessionCM() as session:
            res = session.query(cls).filter(cls.uid == uid).all()
            if len(res) > 0:
                return True
            else:
                return False

    @classmethod
    def get_user_match_data_by_uid(cls, uid):
        with sessionCM() as session:
            res = session.query(cls).filter(cls.uid == uid).first()
            if res:
                return cls.to_dict(res)
            else:
                return {}

    @classmethod
    def to_dict(cls, user_match_data):
        data = {'id': user_match_data.id, 'uid': user_match_data.uid, 'win_count': user_match_data.win_count,
                'lose_count': user_match_data.lose_count, 'winning_streak': user_match_data.winning_streak,
                'highest_winning_streak': user_match_data.highest_winning_streak}
        return data
