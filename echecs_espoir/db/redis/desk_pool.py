# coding=utf-8

import redisco
import random
from redisco import containers
from obespoir.share.parse_json import ParseJson


redis_json = ParseJson.loads("../game_config.json").get("db").get("redis")
redis_config = redis_json.get(redis_json.get("use_env"))
redisco.connection_setup(host=redis_config.get("host"), port=redis_config.get("port")
                         , db=redis_config.get("db"), password=redis_config.get("password"))


class DeskPool(object):
    """
    桌子id池
    """
    POOL_KEY = 'DESK_POOL'

    _instance = {}

    def __init__(self, db=0):
        self.desk_pool = containers.Set(self.POOL_KEY, db=db)

    @classmethod
    def get_instance(cls, db=0):
        if not cls._instance.get(db, None):
            cls._instance[db] = DeskPool()
        return cls._instance[db]

    @classmethod
    def init_pool(cls):
        pool = cls.get_instance()
        if not pool.desk_pool.db.exists(pool.POOL_KEY):
            data = range(100000, 110000)
            pool.desk_pool.db.sadd(pool.POOL_KEY, *data)

    @classmethod
    def pop(cls):
        """
        返回一个随机桌子ID
        :return:
        """
        # pool = cls.get_instance()
        # return pool.desk_pool.db.spop(pool.POOL_KEY)
        # 测试用,暂时固定返回100000
        code_list = [i for i in range(100000, 110000)]
        return random.choice(code_list)

    @classmethod
    def add(cls, desk_id):
        """
        将桌子id重新放回池中
        :param desk_id:
        :return:
        """
        pool = cls.get_instance()
        pool.desk_pool.db.sadd(pool.POOL_KEY, desk_id)


if __name__ == "__main__":
    DeskPool().init_pool()

