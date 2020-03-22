# coding=utf-8
"""
author = jamon
"""

import asyncio
import random
import struct
import ujson
import websockets

from obespoir.share.encodeutil import AesEncoder
from obespoir.share.parse_json import ParseJson
from obespoir.share.ob_log import logger


def random_weighted_choice(weights):
    rnd = random.random() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i


class RpcProtocol(object):
    """消息协议，包含消息处理"""

    def __init__(self):
        self.handfrt = "iii"  # (int, int, int)  -> (message_length, command_id, version)
        self.head_len = struct.calcsize(self.handfrt)
        self.identifier = 0

        self.encode_ins = AesEncoder()
        self.version = 0

        self._buffer = b""    # 数据缓冲buffer
        self._head = None     # 消息头, list,   [message_length, command_id, version]
        self.transport = None
        super().__init__()

    def pack(self, data, command_id):
        """
        打包消息， 用於傳輸
        :param data:  傳輸數據
        :param command_id:  消息ID
        :return: bytes
        """
        print(type(data))
        data = self.encode_ins.encode(data)
        # data = "%s" % data
        length = data.__len__() + self.head_len
        head = struct.pack(self.handfrt, length, command_id, self.version)
        print("type=", type(head), type(data), [head], head[0])
        print(struct.unpack(self.handfrt, head))
        return head + data

    def unpack(self, pack_data):
        head_len = self.head_len
        if head_len > len(pack_data):
            return None

        data_head = pack_data[0:head_len]
        list_head = struct.unpack(self.handfrt, data_head)
        data = pack_data[head_len:]
        result = self.encode_ins.decode(data)
        if not result:
            result = {}

        return {'result': True, 'command': list_head[1], 'data': result}


class Robot(object):

    def __init__(self, config_path):
        self.all_config = ParseJson.loads(config_path)
        self.response_seq = self.all_config.get("response_seq")
        self.encode_type = self.all_config.get("encode_type")
        self.user_id = self.all_config.get("user_id")
        self.user_name = self.all_config.get("user_name")
        # print "@"*88,"all_config=", self.all_config
        ip = self.all_config.get('ip')
        port = self.all_config.get('port')
        self.ws_url = "ws://{}:{}".format(ip, port)
        self.rpc = RpcProtocol()
        self.response_seq = self.all_config.get("response_seq")
        self.sendhandler = {
            1000: self.send_9999,
            100002: self.send_100002,
            100010: self.send_100010,
            100100: self.send_100100,
            100101: self.send_100101,
            100102: self.send_100102,
            100104: self.send_100104,
            100110: self.send_100110,
            100111: self.send_100111,
            100103: self.send_100103,
            100120: self.send_100120,
            9999: self.send_9999,
            10000: self.send_10000
        }

    async def connect_proxy(self):
        async with websockets.connect(self.ws_url) as websocket:
            name = "jamon"
            print("send server: ", name)
            # data_1000 = self.rpc.pack(ujson.dumps({"name": name}), 1000)
            # print("send_1000:", data_1000)
            # await websocket.send(data_1000)
            await self.send_100002(websocket)
            while True:
                data = await websocket.recv()
                unpack_data = self.rpc.unpack(data)
                if not unpack_data:
                    print("aaaaaaaaa:")
                    return

                command = unpack_data.get('command')
                rlength = unpack_data.get('length')
                data = unpack_data.get("data")
                n = random.randint(1, 3)

                # print "#"*88
                # print u"接收数据:", n, data, command
                # reactor.callLater(n, self.receivehandler, command, data)
                await self.receivehandler(websocket, command, data)

    async def receivehandler(self, ws, key, params):
        if params and isinstance(params, str):
            params = ujson.loads(params)
        global responseConfig
        print(u"接收处理:", key, [params])
        # print "@"*88,'str(key)=', str(key)
        rconfig = self.response_seq.get(str(key), None)
        if not rconfig:
            print("index(%s):Error: response config error! key=%s", 1, str(key))
            # print "@"*88, "rconfig is none"
            return

        if not rconfig.get("msg", None):
            # logger.warning("response has not receiver msg handler")F
            return
        # if key == 100002 and params.get("info"):
        #     return self.send_100801(ws, params)
        random_index = random_weighted_choice(rconfig.get("weight"))
        print("bbbbbbbb:", random_index, rconfig, params)
        # print "@"*20, random_index, key, params, rconfig.get("msg")
        return await self.sendhandler.get(rconfig.get("msg")[random_index])(ws, params)

    async def send_data(self, commandID, data, ws):
        print(u"*******发送数据*********：", commandID, data, ws, "||")
        if not isinstance(data, str):
            data = ujson.dumps(data)
        s = self.rpc.pack(data, commandID)
        print([s])
        await ws.send(s)

    async def send_100002(self, ws, params={}):
        '''  登录
        '''
        # print "@" * 33, 'this is %s' % inspect.stack()[1][3]
        passwd = self.all_config.get("password")
        data = {"user_id": self.user_id, "passwd": passwd}
        await self.send_data(100002, data, ws)

    async def send_100010(self, ws, params={}):
        """断线重连"""
        data = {"user_id": self.user_id}
        await self.send_data(100010, data, ws)

    async def send_100100(self, ws, params={}):
        """
        玩家准备
        """
        data = {"user_id": self.user_id, "ready": 1}
        await self.send_data(100100, data, ws)

    async def send_100101(self, ws, params={}):
        """创建好友桌"""
        data = {"user_id": self.user_id}
        await self.send_data(100101, data, ws)

    async def send_100102(self, ws, params={}):
        """加入好友桌"""
        data = {"user_id": self.user_id, "desk_id": 100000}
        await self.send_data(100102, data, ws)

    async def send_100103(self, ws, params={}):
        """玩家退出桌子"""
        data = {"user_id": self.user_id}
        await self.send_data(100103, data, ws)

    async def send_100104(self, ws, params={}):
        """玩家加入匹配场"""
        data = {"user_id": self.user_id}
        await self.send_data(100104, data, ws)

    async def send_100110(self, ws, params={}):
        """解散桌子"""
        data = {"user_id": self.user_id}
        await self.send_data(100110, data, ws)

    async def send_100111(self, ws, params={}):
        """解散房间应答"""
        data = {"user_id": self.user_id, "agree": 1}
        await self.send_data(100111, data, ws)

    async def send_100120(self, ws, params={}):
        """玩家自定义配置"""
        data = {"user_id": self.user_id, "custom_config": {}}
        await self.send_data(100120, data, ws)

    async def send_9999(self, ws, params={}):
        pass
        print("stop...")

    async def send_10000(self, ws, params={}):
        data = {"user_id": self.user_id}
        await self.send_data(10000, data, ws)

    def run(self):
        asyncio.get_event_loop().run_until_complete(self.connect_proxy())


if __name__ == "__main__":
    logger.init(module_name="test", log_dir="logs/", level="debug")
    robot = Robot("robot_2.json")
    robot.run()
    # asyncio.get_event_loop().run_until_complete(test_websocket_proxy())