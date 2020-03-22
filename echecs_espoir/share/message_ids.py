# coding=utf-8
"""
author = jamon
"""

HEART_BEAT = 10000
USER_LOGIN = 100002                 # 登录
USER_RECONNECT = 100010             # 断线重连
USER_READY = 100100                 # 玩家准备
CREATE_FRIEND_DESK = 100101         # 创建好友房
JOIN_FRIEND_DESK = 100102           # 加入好友房
USER_EXIT_DESK = 100103             # 玩家退出桌子
JOIN_MATCH_DESK = 100104            # 加入匹配桌
JOIN_MATCH_DESK_BY_TYPE = 100105    # 加入指定匹配场
DISSOLVE_FRIEND_DESK = 100110       # 解散房间
DISSOLVE_DESK_ANSWER = 100111       # 解散房间应答
DISSOLVE_MATCH_DESK = 100112        # 解散匹配房间

USER_SET_CONFIG = 100120            # 自定义配置
USER_OFFLINE = 100130               # 玩家断线

USER_ACT = 100140                   # 玩家叫牌

USER_TEST_ACT = 100999              # 测试接口

PUSH_CALL_CARD = 101001         # 推送玩家叫牌
PUSH_DRAW_CARD = 101002         # 推送玩家摸牌
PUSH_GAME_OVER = 101003         # 推送游戏结束
PUSH_GEN_BANK  = 101004         # 推送定庄信息
PUSH_DEAL_CARD = 101005         # 推送发牌信息
PUSH_GAME_SETTLE = 101006       # 推送游戏结算
PUSH_GAME_BU_HUA = 101007       # 推送游戏补花
PUSH_GAME_DEAL_BU_HUA = 101008  # 推送发牌补花
PUSH_CALL_CARD_RESULT = 101009  # 推送某玩家叫牌结果
PUSH_GAME_LAI_ZI_DEFINE = 101010  # 推送确定癞子的信息


PUSH_USER_POINT = 101100                # 推送玩家点数发生变化
PUSH_USER_OTHER_LOGIN = 101101          # 推送玩家在其他地方登录
PUSH_DESK_DISSOLVE_RESULT = 101102      # 推送桌子解散结果
PUSH_DESK_DISSOLVE = 101103             # 推送有玩家请求解散桌子
PUSH_DESK_DISSOLVE_ANSWER = 101104      # 推送玩家对解散桌子的响应
PUSH_USER_EXIT = 101105                 # 推送玩家退出桌子
PUSH_USER_READY = 101106                # 推送玩家准备/取消准备
PUSH_USER_JOIN_DESK = 101107            # 推送玩家加入房间
PUSH_USER_SET_CONFIG = 101108           # 推送玩家更改了配置
PUSH_USER_RECONNECT = 101109            # 推送玩家断线重连
PUSH_USER_STATUS = 101110               # 推送玩家连接状态
PUSH_MATCH_DESK_DISSOLVE_RESULT = 101111      # 推送匹配桌子解散结果
PUSH_OTHER_PLAYER_CALL_CARD = 101112    # 推送其他玩家叫牌
