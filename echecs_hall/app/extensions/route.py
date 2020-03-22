# coding=utf-8
import re

from tornado.web import URLSpec

class Route(object):
    """
    视图类装饰器, 直接给视图类绑定路由
    用法:
        @Route('/')
        Class Handler(tornado.web.RequestHandler):
            pass

        @Route('/users/<string>')
        Class Handler(tornado.web.RequestHandler):
            def get(self, user_id):
                pass

        @Route('/users/<int>')
        Class Handler(tornado.web.RequestHandler):
            def get(self, user_id):
                pass
    """
    _routes = []
    _rule_re = re.compile(r'''
        (?P<static>[^<]*)
        <
        (?:
            (?P<converter>[a-zA-Z_][a-zA-Z0-9_]*)
        )
        >
    ''', re.VERBOSE)
    _converters = {
        'int': '(\d+)',
        'string': '([^/]+)'
    }

    def __init__(self, route, host=".*$", name=None, initialize={}):
        self.route = route
        self.host = host
        self.name = name
        self.initialize = initialize

    def __call__(self, handler):
        name = self.name or handler.__name__
        route = self.compile()
        spec = URLSpec(route, handler, self.initialize, name=name)
        self._routes.append({'host': self.host, 'spec': spec})
        return handler

    @classmethod
    def register_routes(cls, application=None):
        """
        将路由注册到application实例
        :param application: application实例
        """
        if application:
            for _route in cls._routes:
                application.add_handlers(_route['host'], [_route['spec']])
        else:
            return [_route['spec'] for _route in cls._routes]

    def get_converter(self, converter):
        return self._converters[converter]

    def parse_route(self):
        pos = 0
        end = len(self.route)

        result = []
        while pos < end:
            m = self._rule_re.match(self.route, pos)
            if not m:
                break
            data = m.groupdict()
            result.append(data)
            pos = m.end()
        return result

    def compile(self):
        _regex = re.sub(re.compile('<(.*?)>'), '%s', self.route)
        regex_parts = []
        for i in self.parse_route():
            regex_parts.append(self.get_converter(i['converter']))

        regex = _regex % tuple(regex_parts)
        return regex
