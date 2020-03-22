# coding=utf-8
"""
author = jamon
"""

import asyncio

from obespoir.share.ob_log import logger
from obespoir.base.common_define import NodeType
from obespoir.base.global_object import GlobalObject

from obespoir.rpcserver.push_lib import push_message
from share.errorcode import *


def push_msg(message_id, data, session_list, code=200):
    """
    主动向客户端推送消息
    :param message_id:
    :param data: json串
    :param session_list:
    :return:
    """
    for session in session_list:
        to, _ = session.split("_")
        if code == 200:
            msg = success_response(data)
        else:
            print("push_msg data=", data)
            raise Exception()
            msg = error_response(USER_LOGIN_OTHER_DEVICE)

        asyncio.ensure_future(push_message(NodeType.PROXY, message_id, msg, session, to), loop=GlobalObject().loop)
