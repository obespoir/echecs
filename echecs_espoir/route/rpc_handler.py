# coding=utf-8
"""
author = jamon
"""

from obespoir.base.common_define import NodeType
from obespoir.base.ob_handler import BaseHandler, RegisterEvent
from obespoir.rpcserver.push_lib import push_message
from obespoir.share.ob_log import logger

from db.message_route import route_ins
from share.message_ids import *
from share.errorcode import *


@RegisterEvent(USER_LOGIN)
class LoginHandler(BaseHandler):

    async def execute(self, *args, **kwargs):
        logger.info("login_handler:{}  {}".format(args, kwargs))
        user_id = self.params.get("user_id", -1)
        passwd = self.params.get("passwd", "")
        if -1 == user_id or not passwd:
            return {}
        login_result = route_ins.login(user_id=user_id, passwd=passwd, new_sessionid=self.session_id, data=self.params)
        print("login_result:", login_result)
        if 200 == login_result.get('code'):
            info = login_result.get("info")
            old_session = info.get("old_session")
            if old_session and self.session_id != old_session:
                # 踢掉之前用户
                to, _ = old_session.split("_")
                data = error_response(USER_LOGIN_OTHER_DEVICE)
                await push_message(NodeType.PROXY, USER_LOGIN_OTHER_DEVICE, data, old_session, to)
            return login_result
        else:
            logger.error("process_login: unknown error:%s", str(login_result))
            return login_result


@RegisterEvent(USER_OFFLINE, need_return=False)
class OfflineHandler(BaseHandler):

    async def execute(self, *args, **kwargs):
        logger.info("offline: {}, {}".format(args, kwargs))
        pass
        return {"code": NORMAL}


@RegisterEvent(HEART_BEAT, need_return=True)
class HeartBeatHandler(BaseHandler):

    async def execute(self, *args, **kwargs):
        logger.info("heartbeat: {}, {}".format(args, kwargs))
        pass
        return {"code": NORMAL}

