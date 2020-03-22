# coding:utf-8


from sqlalchemy import Column
from sqlalchemy.types import Integer, VARCHAR, String

from ..extensions.mysql.mysql_base import Base
from ..extensions.mysql.session import sessionCM


class RoomCFG(Base):
    __tablename__ = 'iw_room_cfg'

    id = Column(Integer, autoincrement=True, nullable=False, unique=True, primary_key=True)
    name = Column(VARCHAR(255), index=True, default=u"初级场")  # or Column(String(30))
    special_rule = Column(String(2040), doc=u"特殊玩法")  #
    min_enter_gold = Column(Integer, default=1000, doc=u"准入金币")  #
    min_play_gold = Column(Integer, default=999, doc=u"玩牌下限")  #
    max_enter_gold = Column(Integer, default=0, doc=u"金币上限")  #
    base_bet = Column(Integer, default=0, doc=u"底注")  #
    service_charge = Column(Integer, default=90, doc=u"台费")  # 台费
    draw_card_time = Column(Integer, default=12, doc=u"出牌时间默认12秒")
    min_hu_fan = Column(Integer, default=6, doc=u"最小起胡番数")
    max_hu_fan = Column(Integer, default=0, doc=u"封顶番数")
    recommend_pay_num = Column(Integer, default=6, doc=u"推荐充值金额")
    room_type = Column(Integer, default=0, doc=u"房间类型[0:初级场,1:中级场,2:高级场]")
    desc = Column(VARCHAR(255), default="")  # 房间描述

    def __init__(self, name, special_rule, min_enter_gold, min_play_gold, max_enter_gold, base_bet, service_charge,
                 draw_card_time, min_hu_fan, max_hu_fan, recommend_pay_num, room_type):
        self.name = name
        self.special_rule = special_rule
        self.min_enter_gold = min_enter_gold
        self.min_play_gold = min_play_gold
        self.max_enter_gold = max_enter_gold
        self.base_bet = base_bet
        self.service_charge = service_charge
        self.draw_card_time = draw_card_time
        self.min_hu_fan = min_hu_fan
        self.max_hu_fan = max_hu_fan
        self.recommend_pay_num = recommend_pay_num
        self.room_type = room_type

    def to_dict(self):
        return {"id": self.id, "name": self.name,
                "special_rule": self.special_rule,
                "min_enter_gold": self.min_enter_gold,
                "min_play_gold": self.min_play_gold,
                "max_enter_gold": self.max_enter_gold,
                "base_bet": self.base_bet,
                "service_charge": self.service_charge,
                "draw_card_time": self.draw_card_time,
                "min_hu_fan": self.min_hu_fan,
                "max_hu_fan": self.max_hu_fan,
                "recommend_pay_num": self.recommend_pay_num,
                "room_type": self.room_type}

    @classmethod
    def create(cls, name, special_rule, min_enter_gold, min_play_gold, max_enter_gold, base_bet, service_charge,
               draw_card_time, min_hu_fan, max_hu_fan, recommend_pay_num, room_type):
        with sessionCM() as session:
            user = session.query(RoomCFG).filter_by(name=name).first()
            if user:
                return 0
            new_user = cls(name, special_rule, min_enter_gold, min_play_gold, max_enter_gold, base_bet,
                           service_charge, draw_card_time, min_hu_fan, max_hu_fan, recommend_pay_num, room_type)
            session.add(new_user)
            session.commit()
            return new_user.id

    @classmethod
    def get_cfg_info_by_id(cls, _id):
        with sessionCM() as session:
            room_cfg = session.query(RoomCFG).filter_by(id=_id).first()
            return room_cfg.to_dict if room_cfg else {}

    @classmethod
    def get_cfg_by_name(cls, name):
        with sessionCM() as session:
            room_cfg = session.query(RoomCFG).filter_by(name=name).first()
            return [room_cfg.to_dict] if room_cfg else [{}]

    @classmethod
    def get_cfg_all(cls):
        with sessionCM() as session:
            room_cfgs = session.query(RoomCFG).all()
            ret = []
            for i in room_cfgs:
                ret.append(i.to_dict())
            return ret if room_cfgs else [{}]

    @classmethod
    def del_user(cls, _id):
        """
        删除用户，慎用!!!!!!!!!!!!!!!
        :param accid:
        :return:
        """
        with sessionCM() as session:
            session.query(RoomCFG).filter_by(id=_id).delete()
            session.commit()
            return 1

    @classmethod
    def update_room_cfg(cls, **kwargs):
        _id = kwargs.get("_id")
        if _id:
            with sessionCM() as session:
                room_cfg = session.query(RoomCFG).filter_by(id=_id).first()
                for k, v in kwargs.items():
                    if hasattr(room_cfg, k):
                        room_cfg.__setattr__(k, v)
                    else:
                        print("RoomCFG update_room_cfg not has %s" % k)
                session.commit()


from app.extensions.globalobject import GlobalObject


GlobalObject().room_cfg_list = RoomCFG.get_cfg_all()


