# coding=utf-8

__author__ = 'jamon'


class SessionGateRel(object):
    def __init__(self):
        self.session_gate_dict = {}

    def get_gate(self, session_id):
        return self.session_gate_dict.get(session_id, "")

    def update_rel(self, session_id, gate_name):
        print("cccccccccc")
        if session_id and gate_name:
            self.session_gate_dict[session_id] = gate_name

    def del_rel(self, session_id):
        if session_id and session_id in self.session_gate_dict.keys():
            self.session_gate_dict.pop(session_id)


session_gate_ins = SessionGateRel()
