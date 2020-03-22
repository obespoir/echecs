# coding=utf-8
"""
author = jamon
"""

import asyncio
import ujson

from websockets.exceptions import ConnectionClosed

from obespoir.share.singleton import Singleton
from obespoir.share.ob_log import logger
from obespoir.base.common_define import NodeType
from obespoir.base.ob_protocol import DataException
from obespoir.base.global_object import GlobalObject
from obespoir.websocketserver.route import webSocketRouteHandle
from obespoir.rpcserver.push_lib import push_message


@webSocketRouteHandle
async def forward_0(command_id, data, session_id):
    """
    消息转发
    :param command_id: int
    :param data: json
    :param session_id: string
    :return: None
    """
    print("forward_0", command_id, data, type(data), data, session_id)
    if not isinstance(data, dict):
        try:
            data = ujson.loads(data)
            print("data type :", type(data))
        except Exception:
            logger.warn("param data parse error {}".format(data))
            return {}
    data.update({"message_id": command_id})
    await push_message(NodeType.ROUTE, command_id, data, session_id=session_id, to=None)

