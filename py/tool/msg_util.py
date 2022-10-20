# -*- coding: utf-8 -*-

import tool.axsbe_base as axsbe_base
from tool.axsbe_exe import axsbe_exe
from tool.axsbe_order import axsbe_order
from tool.axsbe_snap import axsbe_snap, price_level


def str_to_dict(s:str):
    if s[:2] != "//":
        return None
    s = s[2:].split()
    s = [x.split("=") for x in s if x[-1]!='=']
    md = dict((x[0], int(x[1])) for x in s)
    return md


def dict_to_axsbe(s:dict):
    if s['MsgType']==axsbe_base.MsgType_order:   #order
        order = axsbe_order()
        order.load_dict(s)
        return order
    elif s['MsgType']==axsbe_base.MsgType_exe:   #execute
        execute = axsbe_exe()
        execute.load_dict(s)
        return execute
    elif s['MsgType']==axsbe_base.MsgType_snap:   #snap
        snap = axsbe_snap()
        snap.load_dict(s)
        return snap
    else:
        return None


def axsbe_file(fileName):
    with open(fileName, "r") as f:
        while True:
            l = f.readline()
            if not l:
                break
            if l.find("//") >= 0:
                msg = dict_to_axsbe(str_to_dict(l.lstrip()))
                if msg is not None:
                    yield msg


