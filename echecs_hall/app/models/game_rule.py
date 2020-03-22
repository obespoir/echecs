# coding=utf-8
from sqlalchemy import Column
from sqlalchemy.types import CHAR, Integer, VARCHAR, BIGINT
from sqlalchemy.orm import relationship, backref
from ..extensions.mysql.mysql_base import Base
from ..extensions.mysql.session import sessionCM
from app.models.user_info import UserInfo
from ..extensions.common import md5


class GameRule(Base):
    __tablename__ = 'game_rule'
    id = Column(Integer, primary_key=True, doc='唯一id')
    uid = Column(Integer, doc='用户id')
    useQuanPinDao = Column(Integer, doc='是否使用全频道玩法, 0:否， 1：是')
    useJiaMa = Column(Integer, doc='是否使用加马，0：不买马，1：自摸买马，2：亮倒买马')
    useJiaPiao = Column(Integer, doc='是否使用加漂，0：不漂，1：选一次漂，2：每小局选漂')
    area = Column(Integer, doc='地区，默认是襄阳，0：襄阳，2：十堰，1：孝感，3：随州')
    useMaxFan = Column(Integer, doc='结算封顶番数，默认是8，可以选择8或者16')
    chaDaJiao = Column(Integer, doc='是否使用查大叫，0：否，1：是')
    buFenLiang = Column(Integer, doc='是否使用部分亮，0：否，1：是')
    shuKan = Column(Integer, doc='是否使用数坎，0：否，1：是')
    shao12BuLiang = Column(Integer, doc='是否使用少于12张不能亮，0：否，1：是')
    play_times_limit = Column(Integer, doc='当前轮限定最大局数(int)')

    @classmethod
    def validate_game_rule_in_table(cls, uid):
        with sessionCM() as session:
            res = session.query(cls).filter(cls.uid == uid).all()
            if len(res) > 0:
                return True
            else:
                return False

    @classmethod
    def get_user_game_rule_by_uid(cls, uid):
        with sessionCM() as session:
            res = session.query(cls).filter(cls.uid == uid).first()
            if res:
                return cls.to_dict(res)
            else:
                return {}

    @classmethod
    def to_dict(cls, user_game_rule):
        data = {'id': user_game_rule.id, 'uid': user_game_rule.uid, 'useQuanPinDao': user_game_rule.useQuanPinDao,
                'useJiaMa': user_game_rule.useJiaMa, 'useJiaPiao': user_game_rule.useJiaPiao,
                'area': user_game_rule.area, 'useMaxFan': user_game_rule.useMaxFan,
                'chaDaJiao': user_game_rule.chaDaJiao, 'buFenLiang': user_game_rule.buFenLiang,
                'shuKan': user_game_rule.shuKan, 'shao12BuLiang': user_game_rule.shao12BuLiang,
                'play_times_limit': user_game_rule.play_times_limit}
        return data

