# -*- coding: utf-8 -*-

__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.1"

import re


class CQ:
    """
    use 'in' to check CQ in message
    msg mustn't be json
    """
    # 答辩玩意懒得写了 属实不会正则表达式
    obj_at = re.compile(r".*?\[CQ:at,qq=(.*?)]")
    obj_face = re.compile(r".*?\[CQ:face,id=(.*?)]")
    obj_record = re.compile(r".*?\[CQ:record,file=(.*?)]")
    SHARE = "[CQ:share,"
    IMAGE = "[CQ:image,"
    REPLY = "[CQ:reply,"
    REDBAG = "[CQ:redbag,"
    FORWARD = "[CQ:forward,"
    XML = "[CQ:xml,"
    JSON = "[CQ:json,"


def get_at(txt):
    return CQ.obj_at.findall(txt)


__all__ = ("CQ", "get_at")
