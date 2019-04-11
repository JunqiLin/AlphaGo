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
        
        
class DownBuyStrategy(Strategy):
    def __init__(self, bars, events):
        """
        """
        self.bars = bars
        self.symbol_list = self.bars.symbol_list
        self.events = events
        self.bought = self._calculate_initial_bought()
        self.index_ = 0
        
    def _calculate_initial_bought(self):
        """
        """
        bought={}
        for s in self.symbol_list:
            bought[s]=False
        return bought
    
    def calculate_signals(self,event):
        """
        """
        if event.type == 'MARKET':
            for s in self.symbol_list:
#                bars = self.bars.get_latest_bars(s,N=1)
                bars = self.bars.get_bar_byN(s,self.index_)
                #print("%s + %s +%s +%s "%(bars['symbol'],bars['date'],bars['close'],self.index_))
                if bars is not None and bars !=[]:
                    if bars['close'] < 8:
                        
                        signal = SignalEvent(bars['symbol'],bars['date'],'LONG',1,bars['close'])
                        self.events.put(signal)
                else:
                    print("bars is none")
            self.index_+=1
        
class DownAndBuyStrategyTest():
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
        if event.type == 'MARKET':
            for s in self.symbol_list:
                if(self.index_ < self.symbol_len[s]):
                    #type: dict
                    nth_bar = self.bars.get_n_bars(s, self.index_)
#                    date = self.bars.get_n_bars(s, self.index_)
                    if nth_bar:
                        if nth_bar['open']< 120:
                            signal = SignalEvent(s,nth_bar['date'],'LONG',1,nth_bar['close'])
                            signal.print_signal()
                            self.events.put(signal)
                    else:
                        print("nth bar is none")
                else:
                    return
                    
            self.index_+=1
        else:
            print("not")
                        
                
                
                
               
      
        
        
        
class BuyAndHoldStrategy(Strategy):
    def __init__(self, bars, events):
        """
        
        """
        self.bars = bars
        self.symbol_list = self.bars.symbol_list
        self.events = events
        # Once buy & hold signal is given, these are set to True
        self.bought = self._calculate_initial_bought()
        
    def _calculate_initial_bought(self):
        """
        
        """
        bought={}
        for s in self.symbol_list:
            bought[s] = False
        return bought
    
    def calculate_signals(self,event):
        """
        
        """
        if event.type =="MARKET":
            for s in self.symbol_list:
                bars = self.bars.get_latest_bars(s, N=1)
                #b = next(bars[0])
                b = bars[0]
                print(b)
#                for item in bars[0]:
#                    print item
                if bars is not None and bars !=[]:
                    if self.bought[s] == False:
                        signal = SignalEvent(b['symbol'],b['date'],'LONG',strength = 1)
                        
                        self.events.put(signal)
                        self.bought[s]=True