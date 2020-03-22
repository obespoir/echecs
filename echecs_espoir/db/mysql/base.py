#coding:utf8

from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as SA
import datetime
from sqlalchemy.orm import object_session
from obespoir.share.parse_json import ParseJson


class Config(object):
    def __init__(self):
        self.mysql_user = None
        self.mysql_passwd = None
        self.mysql_host = None
        self.mysql_port = None
        self.mysql_db = None

        self.update()

    def update(self):
        mysql_json = ParseJson.loads("../game_config.json").get("db").get("mysql")
        mysql_config = mysql_json.get(mysql_json.get("use_env"))
        self.mysql_user = mysql_config.get("user")
        self.mysql_passwd = mysql_config.get("passwd")
        self.mysql_host = mysql_config.get("host")
        self.mysql_port = mysql_config.get("port")
        self.mysql_db = mysql_config.get("db")


class tBase(object):
    session = property(lambda self: object_session(self))
    # created_date = SA.Column(SA.DateTime, default = datetime.datetime.now, index=True)
    # modified_date = SA.Column(SA.DateTime, default = datetime.datetime.now, onupdate=SA.text('current_timestamp'))


config = Config()


Base = declarative_base(cls=tBase)
metadata = Base.metadata

#: 是否在标准输出流打印sql语句(sqlalchemy)
echo = False
mysql_db = SA.create_engine(
        'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (config.mysql_user, config.mysql_passwd, config.mysql_host, config.mysql_port, config.mysql_db),
        echo=echo,
        pool_recycle=3600,
        pool_size=15
    )

mysql_db.execute("SET NAMES utf8mb4;")   #默认开启utf8mb4，用于存储emoji表情