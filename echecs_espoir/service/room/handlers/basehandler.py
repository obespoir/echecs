# coding=utf-8
# from twisted.internet import defer

from service.room.validators.basevalidator import ValidatorError
from service.room.models.user_manager import UserManager
from share.errorcode import ERROR_CODE_DESC


class BaseHandler(object):
    """
    基础命令处理类
    """
    def __init__(self, params, command_id, session_id):
        self.params = params
        self.command_id = command_id
        self.session_id = session_id
        self.validator = None

    @property
    def cur_user_from_manager(self):
        u = UserManager().get_user_by_sessionid(session_id=self.session_id)
        print("cur_user_from_manager:", u, UserManager()._session_user_dict)
        return u

    def cur_user_from_manager_by_id(self, user_id):
        return UserManager().get_user_by_id(user_id=user_id)

    # @defer.inlineCallbacks
    # def execute_event(self):
    #     try:
    #         result = yield self.execute()
    #         defer.returnValue(self.success_response(result))
    #     except ValidatorError as e:
    #         defer.returnValue(self.error_response(e.error_code))

    def after(self):
        pass

    def execute(self, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def success_response(cls, data):
        '''
        need_push 用来表明该请求消息是否需要直接返回, 默认需要直接返回
        :param data:
        :return:
        '''
        need_push = data.get("need_push", 1)
        result = {"code": 200, "info": data, "need_push": need_push}
        return result

    @classmethod
    def error_response(cls, code):
        result = {"code": code, "desc": ERROR_CODE_DESC.get(code)}
        return result


class RegisterEvent(object):
    """
    事件管理器，将命令码与handler进行绑定
    """
    events = dict()
    def __init__(self, command_id):
        self.command_id = command_id

    def __call__(self, handler):
        self.events[self.command_id] = handler
        return handler

