# coding=utf-8

from tornado.web import URLSpec

"""
系统蓝图
"""


class Blueprint(object):
    def __init__(self, name, url_prefix=''):
        self.name = name
        self.url_prefix = url_prefix
        self.ROUTES = []

    def route(self, route, host=".*$", name=None, initialize={}):
        def decorator(handler):
            _name = name or handler.__name__
            spec = URLSpec(self.url_prefix + route, handler, initialize, name='%s.%s' % (self.name, _name))
            self.ROUTES.append({'host': host, 'spec': spec, 'name': _name})
            return handler
        return decorator

    def register_route(self, app):
        for route in self.ROUTES:
            # print "register_route ROUTES=", self.ROUTES
            app.add_handlers(route['host'], [route['spec']])
