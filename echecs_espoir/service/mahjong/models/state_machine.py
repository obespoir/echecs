# coding=utf-8
class GameingStatus(object):
    """游戏状态"""
    REV_FIRST_ANSWER = 5  # 发牌后等待客户端执行,
    WAITE_PLAYER_ACT = 6  # 等待玩家执行动作


class StateMachine(object):
    def __init__(self, game_data):
        self.status_handlers = {
            GameingStatus.REV_FIRST_ANSWER: self.rev_waite_answer,  # 发牌后等待客户端执行
        }
        self.game_data = game_data
        self.status = -1
        self.is_waite_answer = 0  # 是否接收到任何玩家的应答信息

    @property
    def to_dict(self):
        return {
            "status": self.status,
            "is_waite_answer": self.is_waite_answer,
        }

    def rev_waite_answer(self):
        """
        接到第一个游戏内客户端主动请求
        :return:
        """
        self.is_waite_answer = 1

    def change_state(self, state):
        self.status_handlers[state]()

    def get_cur_gameing_status(self):
        return self.to_dict

    @property
    def players(self):
        return self.game_data.players

    def reset_data(self):
        self.status = -1
        self.is_waite_answer = 0  # 是否接收到任何玩家的应答信息