#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 17:28:34 2019

@author: linjunqi
"""

import datetime
import numpy as np
import pandas as pd
import Queue
from event import *
from abc import ABCMeta, abstractmethod


class Strategy(object):
    """
    
    """
    
    __metaclass__ = ABCMeta
    @abstractmethod
    def calculate_signals(self):
        """
        Provides the mechanisms to calculate the list of signals.
        """
        raise NotImplementedError("Should Implement calculate_signals()")
        
              
class DownAndBuyStrategy():
    def __init__(self,bars,events):
        self.bars = bars
        self.symbol_list = self.bars.symbol_list
        self.events = events
        self.symbol_len = {}
        self._cal_len()
        self.index_ = 0
    
    def _cal_len(self):
        for symbol in self.symbol_list:
            self.symbol_len[symbol] = len(self.bars.total_symbol_data[symbol])
            
        
    def calculate_signals(self, event):
        print("cal_signals index is %s"%(self.index_))
        if event.type == 'MARKET':
            for s in self.symbol_list:
                if(self.index_ < self.symbol_len[s]):
                    #type: dict
                    nth_bar = self.bars.get_n_bars(s, self.index_)
#                    date = self.bars.get_n_bars(s, self.index_)
                    if nth_bar:
                        if nth_bar['open']< 120  and nth_bar['open']!=0 :
                            signal = SignalEvent(s,nth_bar['date'],'LONG',1,nth_bar['close'])
                            signal.print_signal()
                            self.events.put(signal)
                    else:
                        print("nth bar is none")
#                else:
#                    self.index_+=1
#                    return        
            self.index_+=1
        else:
            print("not")
                        
                
                
