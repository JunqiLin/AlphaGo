#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 12:43:26 2019

@author: linjunqi
"""
from datetime import datetime


class BarData(object):
    """
    Candlestick bar data of a certain trading period.
    """

    def __init__(self):
        """"""
        self.symbol = 0
#    exchange: Exchange
        self.datetime=0

        self.interval= None
        self.volume= 0
        self.open = 0
        self.high = 0
        self.low = 0
        self.close = 0
        self.vt_symbol = 0
        