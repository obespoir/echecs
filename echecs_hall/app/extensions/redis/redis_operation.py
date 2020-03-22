# coding=utf-8
from .redis_utils import redis_db


def set_single_hash_in_redis(data):
    k = data.keys()[0]
    if redis_db.hmset(k, data[k]):
        return True
    else:
        return False


'''
data = {'backpack:9123':[
                        {1:{'id':..}},
                        {2:{'id':...}}
                        ]}
'''


def set_multi_hash_in_redis(data):
    k = data.keys()[0]
    for v in data[k]:
        for k0, v0 in v.iteritems():
            redis_db.hmset(k + ':' + str(k0), v0)


'''
data = {'hu:9123':{'id':...}}
'''


def update_single_hash_in_redis(data):
    k = data.keys()[0]
    for v in data[k]:
        redis_db.hset(k, v, data[k][v])
    return True


def get_all_in_redis(data):
    k = redis_db.keys(data)
    new_data = []
    for v in k:
        new_data.append(redis_db.hgetall(v))
    return new_data


def get_one_in_redis(key):
    return redis_db.hgetall(key)


def get_single_field_in_redis(data):
    if isinstance(data, dict):
        k = data.keys()[0]
        v = data.values()[0]
        if isinstance(v, str):
            return redis_db.hget(k, v)
        else:
            return 'format is error'
    else:
        return 'format is error'


def get_multi_field_in_redis(data):
    if isinstance(data, dict):
        k = data.keys()[0]
        v = data.values()[0]
        if isinstance(v, list):
            return redis_db.hmget(k, v)
        else:
            return 'format is error'
    else:
        return 'format is error'

