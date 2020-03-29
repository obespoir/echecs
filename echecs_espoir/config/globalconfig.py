# coding=utf-8
import requests
import ujson

# from obespoir.share.ob_log import logger
from obespoir.share.parse_json import ParseJson


class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kw)
        return cls._instance


class GlobalConfig(object, metaclass=Singleton):

    # __metaclass__ = Singleton   #注意：本套代码是在单进程下运行，否则会引发线程安全问题

    def __init__(self):
        # logger.info("Config init...")
        print("GlobalConfig init...")
        # 操作时间
        self.auto_op_wait_time = 1
        self.manual_op_wait_time = 10
        self.waite_answer_time = 10
        self.ting_auto_chu_time = 2
        self.manual_op_against_act_time = 10
        self.dissolve_time = 15
        self.bu_hua_show_time = 1
        self.room_cfg_list = []  # 房间场配置 [0:初级场,1:中级场,2:]
        self.web_server_url = "http://127.0.0.1:8889/mj/get_hall_room_info2"
        self.update_config()
        self.update_room_cfg()
        self.test_sure_next_cards = {}  # 用于储存测试确定接下来牌的信息
                                        # detail: {desk_id:[[],[],[],[]]. desk_id2:[[],[],[],[]]}

    def update_config(self):
        desk_json = ParseJson.loads("../game_config.json")
        # logger.info("update_config:%s", str(desk_json))
        self.auto_op_wait_time = desk_json.get("auto_op_wait_time")
        self.manual_op_wait_time = desk_json.get("manual_op_wait_time")
        self.waite_answer_time = desk_json.get("waite_answer_time")
        self.ting_auto_chu_time = desk_json.get("ting_auto_chu_time")
        self.manual_op_against_act_time = desk_json.get("manual_op_against_act_time")

        self.dissolve_time = desk_json.get("dissolve_wait_time")

        self.bu_hua_show_time = desk_json.get("bu_hua_show_time")
        self.web_server_url = desk_json.get("web_server_url")

    def update_room_cfg(self):
        # default_json = EspoirJson.loads("game_setting/default.json")
        r = requests.get(self.web_server_url, {})
        data = ujson.loads(r.text).get("data")
        print("globalObject data=", data)
        self.room_cfg_list = data.get("room_cfg_info")

    def reset_test_data(self):
        self.test_sure_next_cards = {}  # 用于储存测试确定接下来牌的信息
        # detail: {desk_id:[[],[],[],[]]. desk_id2:[[],[],[],[]]}


if __name__ == "__main__":
    print(GlobalConfig().auto_op_wait_time)