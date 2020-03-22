# coding=utf-8

from service.bridgecontroller import bridge_controller_ins


def notify_all_desk_player(desk_id, command_id, data):
    bridge_controller_ins.notify_desk(desk_id, command_id, data)


def notify_desk_game_over(desk_id):
    bridge_controller_ins.notify_desk_game_over(desk_id)


def notify_single_user(desk_id, seat_id, command_id, data, code=200):
    bridge_controller_ins.notify_player(desk_id, seat_id, command_id, data, code)


def notify_settle_data(desk_id, settle_data):
    bridge_controller_ins.notify_settle_data(desk_id, settle_data)