# coding=utf-8
import os
import sys
import logging

import tornado.log
import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.options import options


from app.extensions.globalobject import GlobalObject
from app.extensions.config_parser import ConfigParser

from .views import er_mj, main_route
from .views import mj_hall
from .views import er_mj, main_route, admin
import json


class Application(tornado.web.Application):
    def __init__(self, cfg):
        settings = ConfigParser(cfg)
        super(Application, self).__init__(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            autoreload=settings.get('DEBUG'),
            cookie_secret=settings.get('SECRET_KEY'),
            compiled_template_cache=not settings.get('DEBUG'),
            gzip=True,
            **settings
        )
        self.redis_db = None
        self.db = None
        self.init_db()
        self.register_blueprint()
        self.game_config = self.load_game_config()

    def init_db(self):
        self.redis_db = GlobalObject().redis_db

    def register_blueprint(self):
        er_mj.register_route(self)
        main_route.register_route(self)
        mj_hall.register_route(self)
        admin.register_route(self)

    def load_game_config(self):
        with open('app/config/game_config.json', 'r') as f:
            config = json.load(f)
        return config

    def setup_logging_to_stream(self, stream, log_level):
        logger = logging.getLogger()
        channel = logging.StreamHandler(stream)
        channel.setLevel(log_level)
        channel.setFormatter(tornado.log.LogFormatter())
        logger.addHandler(channel)

    def setup_logging(self, log_level=None):
        if log_level is None:
            log_level = getattr(logging, options.logging.upper())

        logger = logging.getLogger()
        logger.setLevel(log_level)

        self.setup_logging_to_stream(stream=sys.stdout, log_level=log_level)
        self.setup_logging_to_stream(stream=sys.stderr, log_level=logging.ERROR)

    def run(self, address='127.0.0.1', port=8888):
        self.setup_logging()
        tornado.log.enable_pretty_logging()
        http_server = tornado.httpserver.HTTPServer(self, xheaders=True)
        http_server.listen(port, address=address)
        self._print_starting_info(address, port)
        tornado.ioloop.IOLoop.current().start()

    def _print_starting_info(self, address, port):
        print(' * Running on http://{HOST}:{PORT}/ (Press CTRL+C to quit)'.format(
            HOST=self.settings.get('HOST', address),
            PORT=self.settings.get('PORT', port),
        ))
