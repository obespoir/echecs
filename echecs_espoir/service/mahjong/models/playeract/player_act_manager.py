# coding=utf-8

from service.mahjong.controls.gamemanager import game_manager
from service.mahjong.constants.gamedefine import Act
from service.mahjong.models.playeract.player_act_hook import PlayerActHook
from obespoir.share.ob_log import logger
from service.mahjong.models.utils.notify_playeract import notify_player_ins
from share.errorcode import CUR_USER_CANT_SPEAK
from service.mahjong.models.state_machine import GameingStatus
from service.mahjong.controls.notifybridge import notify_single_user
from share.message_ids import PUSH_CALL_CARD

class PlayerActManager(object):
    """
    玩家动作管理类
    """
    instances = {}

    def __init__(self, game_data):
        self.acts = {}
        self.game_data = game_data
        self.hook = PlayerActHook(self.game_data)
        self.handler = {
            Act.GUO: self.act_guo,
            Act.CHU: self.act_chu,
            Act.CHI: self.act_chi,
            Act.PENG: self.act_peng,
            Act.DIAN_GANG: self.act_dian_gang,
            Act.BU_GANG: self.act_bu_gang,
            Act.AN_GANG: self.act_an_gang,
            Act.TING: self.act_ting,
            Act.DIAN_HU: self.act_dian_hu,
            Act.ZI_MO: self.act_zi_mo,
            Act.WAITE_ANSWER: self.waite_answer,

        }

    @classmethod
    def get_instance(cls, desk_id):
        if desk_id not in cls.instances.keys():
            game_desk = game_manager.get_game_desk(desk_id)
            cls.instances[desk_id] = PlayerActManager(game_desk.game_data)
        return cls.instances[desk_id]

    def cache_act(self, seat_id, act_type, act_params):
        """
        缓存动作,用于判断动作优先级
        :param seat_id:
        :param act_type:
        :param act_params:
        :return:
        """

        if not self.game_data.cur_players_to_act.get(seat_id, []):
            notify_single_user(self.game_data.desk_id, seat_id,
                               command_id=PUSH_CALL_CARD,
                               data={"desc": "current user can't do anything"},
                               code=CUR_USER_CANT_SPEAK)
            return
        if act_type not in self.game_data.cur_players_to_act[seat_id]:
            return
        act_params.update(self.game_data.cur_players_acted[seat_id][act_type])   # 待执行动作结果中可能存储了部分局部信息
        self.game_data.del_player_to_act(seat_id)
        self.game_data.add_player_acted(seat_id, act_type, act_params)
        logger.debug(u"cache__act: %s", str([self.game_data.cur_players_to_act, self.game_data.cur_players_acted]))
        return 1

    def player_act(self, seat_id, act_type, act_params={}):
        """
        玩家发送过来的操作只有在所有玩家的操作都达到后，才会真正决定是否执行
        :return:
        """
        # 如果是 watie_answer直接执行
        if act_type == Act.WAITE_ANSWER:
            if not self.game_data.state_machine.is_waite_answer:
                self.game_data.state_machine.change_state(GameingStatus.REV_FIRST_ANSWER)
                self.handler[act_type]()
            return
        # 保存玩家回馈的动作参数变动
        self.game_data.add_player_acted(seat_id, act_type, act_params)
        print("player_act:", seat_id, act_type, act_params)
        if act_type not in self.handler.keys() or not self.cache_act(seat_id, act_type, act_params):
            logger.debug(u"player_act error:act_type=%s", str(act_type))
            return
        if 0 == len(self.game_data.cur_players_to_act):
            # 所有玩家都已进行过操作, 开始执行缓存中的操作, 只执行优先级最高的
            max_priority_act = Act.GUO
            need_run_act = {"act_type": max_priority_act, "detail":{}}

                # {"act_type": Act.GUO, "detail":{seat_id: act_params, ...}}
            for tmp_seatid, info in self.game_data.cur_players_acted.items():
                acted_type = list(info.keys())[0]
                print("aaaaaa:", [info])
                # if info[acted_type] >= need_run_act["act_type"]:
                if acted_type >= need_run_act["act_type"]:
                    need_run_act["act_type"] = info[acted_type]
                    need_run_act["detail"][tmp_seatid] = info[acted_type]
            self.game_data.cur_players_acted = {}

            # 钩子是否截获行为判断
            if not self.hook.hook(seat_id, act_type, act_params):
                return 2
            return self.handler[act_type](need_run_act["detail"])
        else:
            # 動作暫時緩存，等待其他玩家操作
            if act_type == self.get_cur_player_max_act():
                logger.debug(u"获得最高优先级动作, 立刻出发执行效果! 最高优先级动作=%s"%act_type)
                ret = self.handler[act_type](self.game_data.cur_players_acted[seat_id][act_type])
            # 動作暫時緩存，等待其他玩家操作
            return 2

    def execute_player_act(self, seat_id, act_type, act_params):
        return self.handler[act_type]({seat_id: act_params})

    def act_chu(self, act_params={}):
        # 出操作处理
        logger.info("### act_chu act_params=", act_params)
        from service.mahjong.models.playeract.chu import Chu
        if not self.acts.get("chu", None):
            self.acts['chu'] = Chu(game_data=self.game_data)
        return self.acts["chu"].execute(act_params=act_params)

    def act_chi(self, act_params={}):
        # 吃操作处理
        from service.mahjong.models.playeract.chi import Chi
        if not self.acts.get("chi", None):
            self.acts['chi'] = Chi(game_data=self.game_data)
        return self.acts["chi"].execute(act_params=act_params)

    def act_peng(self, act_params={}):
        # 碰操作处理
        from service.mahjong.models.playeract.peng import Peng
        if not self.acts.get("peng", None):
            self.acts['peng'] = Peng(game_data=self.game_data)
        return self.acts["peng"].execute(act_params=act_params)

    def act_dian_gang(self, act_params={}):
        # 点杠操作处理
        from service.mahjong.models.playeract.diangang import DianGang
        if not self.acts.get("dian_gang", None):
            self.acts['dian_gang'] = DianGang(game_data=self.game_data)
        return self.acts["dian_gang"].execute(act_params=act_params)

    def act_bu_gang(self, act_params={}):
        # 补杠操作处理
        from service.mahjong.models.playeract.bugang import BuGang
        if not self.acts.get("bu_gang", None):
            self.acts['bu_gang'] = BuGang(game_data=self.game_data)
        return self.acts["bu_gang"].execute(act_params=act_params)

    def act_an_gang(self, act_params={}):
        # 暗杠操作处理
        from service.mahjong.models.playeract.angang import AnGang
        if not self.acts.get("an_gang", None):
            self.acts['an_gang'] = AnGang(game_data=self.game_data)
        return self.acts["an_gang"].execute(act_params=act_params)

    def act_ting(self, act_params={}):
        # 听牌操作处理
        from service.mahjong.models.playeract.ting import Ting
        if not self.acts.get("ting", None):
            self.acts['ting'] = Ting(game_data=self.game_data)
        return self.acts["ting"].execute(act_params=act_params)

    def act_dian_hu(self, act_params={}):
        # 点炮胡操作处理
        from service.mahjong.models.playeract.dianhu import DianHu
        if not self.acts.get("dian_hu", None):
            self.acts['dian_hu'] = DianHu(game_data=self.game_data)
        return self.acts["dian_hu"].execute(act_params=act_params)

    def act_zi_mo(self, act_params={}):
        # 自摸操作处理
        from service.mahjong.models.playeract.zimo import ZiMo
        if not self.acts.get("zi_mo", None):
            self.acts['zi_mo'] = ZiMo(game_data=self.game_data)
        return self.acts["zi_mo"].execute(act_params=act_params)

    def act_guo(self, act_params={}):
        # 过操作处理
        from service.mahjong.models.playeract.guo import Guo
        if not self.acts.get("guo", None):
            self.acts['guo'] = Guo(game_data=self.game_data)
        return self.acts["guo"].execute(act_params=act_params)

    def test_act(self, seat_id, act, card_list):
        from service.mahjong.models.playeract.test_act import TestAct
        if not self.acts.get("test_act", None):
            self.acts["test_act"] = TestAct(game_data=self.game_data)
        return self.acts["test_act"].execute(seat_id, act, card_list)

    def waite_answer(self, act_params={}):
        from service.mahjong.models.playeract.waite_answer import WaiteAnswer
        if not self.acts.get("waite_answer", None):
            self.acts['waite_answer'] = WaiteAnswer(game_data=self.game_data)
        return self.acts["waite_answer"].execute()

    def get_cur_player_max_act(self):
        """
        获取当前所有玩家待进行的操作中最高优先级的动作, 当此动作到达,则不需要等待其他动作的回复
        :return:
        """
        # 初始化当前所有玩家待进行的操作中最高优先级的动作
        cur_player_to_act_max = Act.GUO
        for seat_id in self.game_data.cur_players_to_act.keys():
            for act_type in self.game_data.cur_players_to_act[seat_id].keys():
                # 此处未处理通炮
                if cur_player_to_act_max <= act_type:
                    cur_player_to_act_max = act_type
        return cur_player_to_act_max