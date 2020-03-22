# coding=utf-8
"""
author = jamon
"""

import traceback

from obespoir.base.ob_handler import BaseHandler as ObBasehandler, RegisterEvent as ObRegisterEvent
from obespoir.share.ob_log import logger

from service.room.handlers.basehandler import RegisterEvent, BaseHandler, ValidatorError
from share.errorcode import *
from share.message_ids import *


@ObRegisterEvent(0, need_return=True)
class DefaultHandler(ObBasehandler):

    async def execute(self, *args, **kwargs):
        logger.info("default: {}, {}, {}".format(args, kwargs, self.params))

        user_id = self.params.get("user_id", -1)
        if -1 == user_id and self.command_id not in [USER_OFFLINE]:
            return

        class_obj = RegisterEvent.events.get(self.command_id)
        if not class_obj:
            return BaseHandler.error_response(COMMAND_NOT_FOUND)
        self.params.update({"session_id": self.session_id})
        event_ins = class_obj(self.params, self.command_id, self.session_id)

        try:
            ret = event_ins.execute()
            print("cccccccc3333:", self.params, ret, [ret.get("need_push", 1)])
            if not ret.get("need_push", 1):   # 不需要推送
                print("ddafafafas", [ret.get("need_push", 1)])
                return
            return success_response(ret)
        except ValidatorError as e:
            print("eeeeeeeeeeeee:", e)
            return error_response(e.error_code)
        except Exception as e:
            print("fffffffff:", traceback.format_exc())
            return error_response(INVALID_REQUEST)






