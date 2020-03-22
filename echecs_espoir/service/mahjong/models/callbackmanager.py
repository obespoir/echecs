# coding=utf-8

__author__ = 'jamon'


from service.mahjong.controls.gamemanager import game_manager
from service.mahjong.constants.gamedefine import Act, SystemActType
from obespoir.share.ob_log import logger


class CallbackFuncType(object):
    NOTHING = 0
    FUNC_AUTO_PLAYER_ACT = 1          # 玩家超时后自动操作
    FUNC_PLAYER_ACT = 2               # 玩家操作

    FUNC_DRAW_CARD = 100          # 摸牌
    FUNC_CHECK_AGAINST = 101      # 检查其他玩家可以进行的

    FUNC_NOTIFY_PLAYER_ACT = 200  # 通知玩家进行操作　


class CallbackManager(object):
    """
    该类主要用来解决模块循环调用问题
    """
    instances = {}

    def __init__(self, desk_id, game_data=None):
        self.desk_id = desk_id
        self.game_data = game_data
        self.handler = {
            CallbackFuncType.NOTHING: self.call_nothing,
            CallbackFuncType.FUNC_AUTO_PLAYER_ACT: self.call_auto_player_act,
            CallbackFuncType.FUNC_PLAYER_ACT: self.call_player_act,

            CallbackFuncType.FUNC_DRAW_CARD: self.call_draw_card,
            CallbackFuncType.FUNC_CHECK_AGAINST: self.call_check_against,

            CallbackFuncType.FUNC_NOTIFY_PLAYER_ACT: self.call_notify_player_act
        }

    @classmethod
    def get_instance(cls, desk_id):
        if desk_id not in cls.instances.keys():
            game_desk = game_manager.get_game_desk(desk_id)
            cls.instances[desk_id] = CallbackManager(desk_id, game_desk.game_data)
        return cls.instances[desk_id]

    def call_auto_player_act(self, call_params={}):
        from service.mahjong.models.playeract.player_act_manager import PlayerActManager
        seat_id = call_params.get("seat_id")
        act_info = call_params.get("act_info", {})
        if not act_info or -1 == seat_id:
            logger.debug(u"call_auto_player_act: error:%s", str(call_params))
            return
        acts = act_info.keys()
        tmp = list(set(acts).intersection(self.game_data.game_config.auto_act_list))
        if tmp:
            # 自动执行的操作
            tmp.sort(reverse=True)
            a = tmp[0]
            b = act_info.get(tmp[0])
            print("auto_player_act:", seat_id, a, b)
            return PlayerActManager.get_instance(self.desk_id).player_act(seat_id, tmp[0],
                                                                          act_params=act_info.get(tmp[0]))
        # else:
        #     return PlayerActManager.get_instance(self.desk_id).player_act(seat_id, Act.GUO, act_params=)

    def call_player_act(self, call_params={}):
        from service.mahjong.models.playeract.player_act_manager import PlayerActManager
        seat_id = call_params.get("seat_id")
        act_type = call_params.get("act_type")
        act_params = call_params.get("act_params")
        if -1 == seat_id:
            logger.debug(u"call_player_act: error:%s", str(call_params))
            return
        return PlayerActManager.get_instance(self.desk_id).execute_player_act(seat_id, act_type, act_params=act_params)

    def execute(self, call_func_type=CallbackFuncType.NOTHING, call_params={}):
        if call_func_type not in self.handler.keys():
            logger.debug(u"CallbackManager error: %s", str([call_func_type, call_params]))
            return
        return self.handler.get(call_func_type)(call_params)

    def call_nothing(self, call_params={}):
        pass

    def call_draw_card(self, call_params={}):
        from service.mahjong.models.systemact.system_act_manager import SystemActManager
        seat_id = call_params.get("seat_id")
        card_num = call_params.get("card_num", 1)
        is_last = call_params.get("is_last", False)
        SystemActManager.get_instance(self.desk_id).system_act(act_type=SystemActType.DRAW_CARD, act_params={
            "seat_id": seat_id, "card_num": card_num, "is_last": is_last})

    def call_check_against(self, call_params={}):
        pass

    def call_notify_player_act(self, call_params={}):
        print("call_notify_player_act:", call_params)
        from service.mahjong.models.utils.notify_playeract import notify_player_ins
        seat_id = call_params.get("seat_id")
        act_info = call_params.get("act_info")
        interval = call_params.get("interval")
        for t, p in act_info.items():
            self.game_data.add_player_to_act(seat_id, t, p)
        notify_player_ins.notify_player(self.desk_id, seat_id, act_info=act_info, interval=interval)