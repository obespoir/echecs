# coding=utf-8

from service.bridgecontroller import bridge_controller_ins


def start_game(desk_id, custom_config):
    return bridge_controller_ins.start_game(desk_id, custom_config)


def user_act(desk_id, seat_id, act_type, act_params):
    return bridge_controller_ins.player_act(desk_id, seat_id, act_type, act_params)


def get_reconnect_desk_info(desk_id, seat_id):
    return bridge_controller_ins.get_reconnect_desk_info(desk_id, seat_id)


def user_test_act(desk_id, seat_id, act, card_list):
    return bridge_controller_ins.user_test_act(desk_id, seat_id, act, card_list)
