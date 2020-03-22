# coding=utf-8

NORMAL = 200     # 消息处理正常


USER_ID_REQUIRED = 900
COMMAND_NOT_FOUND = 901
USER_NOT_FOUND_ON_DESK = 902
DESK_NOT_EXIST = 903
USER_IN_OTHER_DESK = 904
DESK_IS_FULL = 905
DESK_IS_PLAYING = 906
DESK_CONFIG_ERROR = 907
USER_LOGIN_OTHER_DEVICE = 908
ROOM_TYPE_ERROR = 909

ROOM_CARD_NOT_ENOUGH = 910
ROOM_POINT_NOT_ENOUGH = 911

USER_PASSWD_ERROR = 912

NEED_S_CARD_T_CARD = 990
CANT_USE_TEST_GAME_STATUS_UN_AGREE = 991
CANT_USE_TEST = 992
TEST_PARAMS_ERROR = 993
CARD_NOT_IN_HAND_CARD = 994
CUR_USER_CANT_SPEAK = 995
PARAMS_ERROR = 996
SESSION_NOT_EXIST = 997
REPEAT_REQUEST = 998
INVALID_REQUEST = 999

ERROR_CODE_DESC = {
    USER_ID_REQUIRED: u"缺少userid",
    COMMAND_NOT_FOUND: u"消息未注册",
    USER_NOT_FOUND_ON_DESK: u"桌子中没有该用户",
    DESK_NOT_EXIST: u"桌子不存在",
    USER_IN_OTHER_DESK: u"用户在其他桌子中",
    DESK_IS_FULL: u"桌子已满",
    DESK_IS_PLAYING: u"桌子处于游戏中",
    DESK_CONFIG_ERROR: u"桌子自定义配置错误",
    USER_LOGIN_OTHER_DEVICE: u"用户在其他设备登录",
    ROOM_TYPE_ERROR: u"传入房间类型错误",

    ROOM_CARD_NOT_ENOUGH: u'房卡不够',
    ROOM_POINT_NOT_ENOUGH: u'金币不够',
    USER_PASSWD_ERROR: u'用户密码错误',

    CANT_USE_TEST_GAME_STATUS_UN_AGREE: u"游戏已经发过来或者已经结束了,还怎么初始化手牌!",
    CANT_USE_TEST: u"无法使用上帝模式!",
    TEST_PARAMS_ERROR: u"测试动作参数错误?",
    CARD_NOT_IN_HAND_CARD: u"你手中没有这张牌你拿啥跟我换?",
    CUR_USER_CANT_SPEAK: u"当前玩家无法操作",
    PARAMS_ERROR: u"参数错误",
    SESSION_NOT_EXIST: u"会话不存在",
    REPEAT_REQUEST: u"重复请求",
    INVALID_REQUEST: u"非法请求"
}


def error_response(code):
    result = {"code": code, "info": ERROR_CODE_DESC.get(code)}
    return result


def success_response(data):
    result = {"code": 200, "info": data}
    return result