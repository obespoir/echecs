# coding=utf-8

from app.extensions.blueprint import Blueprint
from tornado import web

from app.views.base_handler import BaseHandler

main_route = Blueprint('main_route')


@main_route.route('/', name="test_route")
class TestHandler(web.RequestHandler):
    def get(self):
        print("testHandler self=", self)
        self.render("index.html",name="admin")

@main_route.route('/table', name="test_route")
class Test1Handler(web.RequestHandler):
    def get(self):
        print("testHandler self=", self)
        self.render("table.html",name="admin")

@main_route.route('/body_right', name="sidebar_left")
class Test2Handler(web.RequestHandler):
    def get(self):
        print("testHandler self=", self)
        self.render("sub_page/body_right.html", name="admin")


@main_route.route("/connect_help", name='connect_help')
class ConnectHelp(BaseHandler):
    def get(self, *args, **kwargs):
        self.render("sub_page/connect_help.html", name=u"链接说明")


@main_route.route('/test2', name="test2_route")
class Test3Handler(web.RequestHandler):
    def get(self):
        print("testHandler self=", self)
        return self.write('test222_route')

    def post(self, *args, **kwargs):
        print("*argsL: ", args)
        print("*kwargs: ", kwargs)
        print(self.get_argument('a'))
        pass
        print(self.application.redis_db)
        return self.write('test2_ post!!')
