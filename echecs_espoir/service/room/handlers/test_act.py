# coding=utf-8

from service.room.handlers.basehandler import BaseHandler, RegisterEvent
from service.room.validators.test_act import TestActValidator
from share.message_ids import *
from service.room.notifybridge import user_test_act
from config.globalconfig import GlobalConfig


@RegisterEvent(USER_TEST_ACT)
class TestActHandler(BaseHandler):

    def execute(self, *args, **kwargs):
        """
        测试接口
        :param args:
        :param kwargs:
        :return:
        """
        validator = TestActValidator(handler=self)

        if validator.test_type.data == 4:
            cards = validator.test_params.data.get("target_card")
            if not GlobalConfig().test_sure_next_cards.get(validator.desk.desk_id):
                GlobalConfig().test_sure_next_cards[validator.desk.desk_id] = [[],[],[],[]]
            GlobalConfig().test_sure_next_cards[validator.desk.desk_id][validator.user.seat_id] = cards
            return {"need_push":1, "init_cards": cards, "test_type": 4}
        else:
            user_test_act(validator.desk.desk_id, validator.user.seat_id
                          , validator.test_type.data, validator.test_params.data)



        return {"need_push": 0}
