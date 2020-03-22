#coding:utf8

import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import object_session
import sqlalchemy as SA

from ..espoirjson import EspoirJson
from ..globalobject import GlobalObject


class Config(object):
    def __init__(self):
        self.mysql_url = None
        self.update()

    def update(self):
        self.mysql_url = GlobalObject().settings.get("SQLALCHEMY_DATABASE_URI")


class tBase(object):
    session = property(lambda self: object_session(self))
    created_date = SA.Column(SA.DateTime, default = datetime.datetime.now, index=True)
    modified_date = SA.Column(SA.DateTime, default = datetime.datetime.now, onupdate=SA.text('current_timestamp'))


config = Config()


Base = declarative_base(cls=tBase)
metadata = Base.metadata

#: 是否在标准输出流打印sql语句(sqlalchemy)
echo = True
mysql_db = SA.create_engine(
        config.mysql_url,
        echo=echo,
        pool_recycle=3600,
        pool_size=15
    )

mysql_db.execute("SET NAMES utf8mb4;")   #默认开启utf8mb4，用于存储emoji表情