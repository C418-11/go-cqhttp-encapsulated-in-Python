# -*- coding: utf-8 -*-

import collections
import time
import random
import unicodedata


class MessageDelayLikeHuman:
    DEFAULT_DELAY = (550, 1150)
    NUMBER_DELAY = (160, 700)  # 数字
    SYMBOL_DELAY = (230, 560)  # 符号
    Ll_DELAY = (300, 600)  # 小写字母
    Lu_DELAY = (350, 900)  # 大写字母
    Lo_DELAY = (800, 1550)  # 其他字母

    ONCE_MAX_DELAY = 9000
    ONCE_MIN_DELAY = 100

    MAX_DELAY = 70000
    MIN_DELAY = 4000

    TOTAL_LIMIT_LENGTH = 400

    @staticmethod
    def easy_delay(length, one_char_range=DEFAULT_DELAY):
        """
        :param length: 字符串长度
        :param one_char_range: 以毫秒为单位
        """

        for _ in range(length):
            time.sleep(random.randint(*one_char_range) / 1000)

    @classmethod
    def _get_delay_range(cls, char):

        type_ = unicodedata.category(char)

        delay_range = cls.DEFAULT_DELAY

        if 'N' in type_:
            delay_range = cls.NUMBER_DELAY
        if ('P' in type_) or ('S' in type_):
            delay_range = cls.SYMBOL_DELAY

        match type_:
            case "Lo":
                delay_range = cls.Lo_DELAY
            case "Ll":
                delay_range = cls.Ll_DELAY
            case "Lu":
                delay_range = cls.Lu_DELAY

        return delay_range

    @classmethod
    def _calculate_magnification(cls, count):
        magnification = 1.2
        return max(magnification-(count/100), 0.58)

    @classmethod
    def delay_by_count(cls, text):
        """
        :param text: 字符串
        """

        if len(text) > cls.TOTAL_LIMIT_LENGTH:
            raise ValueError(f"Exceeding length limit (limit: {cls.TOTAL_LIMIT_LENGTH})")

        count = collections.Counter(text)

        total_delay_time = 0

        for char in count:

            char: str

            delay_range = cls._get_delay_range(char)  # 获取延时区间

            base_delay = 0
            for _ in range(count[char]):  # 为每一个字符生成一次随机数
                base_delay += random.randint(*delay_range)

            base_delay *= cls._calculate_magnification(count[char])  # 乘以倍率

            once_delay_time = min(max(base_delay, cls.ONCE_MIN_DELAY), cls.ONCE_MAX_DELAY)

            total_delay_time += once_delay_time

        delay_time = min(max(total_delay_time, cls.MIN_DELAY), cls.MAX_DELAY)

        time.sleep(delay_time/1000)


__all__ = ("MessageDelayLikeHuman", )
