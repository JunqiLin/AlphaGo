#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 11:24:34 2019

@author: linjunqi
"""
import datetime
import os, os.path
import pandas as pd
from abc import ABCMeta, abstractmethod
from event import MarketEvent

class DataHandler(object):
    """
    DataHandler is an abstract base class providing an interface for
    all subsequent (inherited) data handlers (both live and historic).

    The goal of a (derived) DataHandler object is to output a generated
    set of bars (OLHCVI) for each symbol requested. 

    This will replicate how a live strategy would function as current
    market data would be sent "down the pipe". Thus a historic and live
    system will be treated identically by the rest of the backtesting suite.
    """
    __metaclass__ = ABCMeta
    @abstractmethod
    
    def get_latest_bars(self, symbol, N=1):
        """
        Returns the last N bars from the latest_symbol list,
        or fewer if less bars are available.
        """
        raise NotImplementedError("Should implement get_latest_bars()")

    @abstractmethod
    
    def update_bars(self):
        """
        Pushes the latest bar to the latest symbol structure
        for all symbols in the symbol list.
        """
        raise NotImplementedError("Should implement update_bars()")
    
class HistoricCSVDataHandler(DataHandler):
    def __init__(self, events, csv_dir, symbol_list):
        self.events = events
        self.csv_dir = csv_dir
        self.symbol_list = symbol_list
        
        self.symbol_data={}
        self.latest_symbol_data={}
        self.continue_backtest = True
        self._open_convert_csv_files()
        self.get_bars()
        
    def _open_convert_csv_files(self):
        comb_index = None
        for s in self.symbol_list:
            
            self.symbol_data[s]=pd.read_csv(os.path.join(self.csv_dir,'%s.csv'%s), header = 0,
                        index_col = 0, names=['datetime', 'open', 'low', 'high', 'close','volume','oi']
                            )
            # Combine the index to pad forward values
            #make each value size equals
            if comb_index is None:
                comb_index = self.symbol_data[s].index
            else:
                comb_index.union(self.symbol_data[s].index)
                
            self.latest_symbol_data[s]=[]
            # Reindex the dataframes
#        for s in self.symbol_list:
#            self.symbol_data[s] = self.symbol_data[s].reindex(index=comb_index, method='pad')
        
        
    def _get_new_bar(self, symbol):
        """
        Return the lastest bar from the data feed as a tuple of 
        (symbol,datetime,open, hign ,low ,close,volume)
        """
        
        df = self.symbol_data[symbol]
        
        lenth = len(df)
        
        for i in range(lenth):
            yield ({'symbol':symbol, 'date':str(df.index[i]),
                    'open':df[['open']].iat[i,0],
                    'low':df[['low']].iat[i,0],
                    'high':df[['high']].iat[i,0],
                    'close':df[['close']].iat[i,0],
                    'volume':df[['volume']].iat[i,0]})
    
    
    def get_latest_bars(self,symbol,N=1):
        try:
            bars_list = self.latest_symbol_data[symbol]
            
        except KeyError:
            print("The symbol is not available in the historiacal data")
        else:
            return bars_list[-N:]
        
    def get_bar_byN(self, symbol, N):
        if N<len(self.latest_symbol_data[symbol]):
            bar = self.latest_symbol_data[symbol][N]
            print("******")
            print(bar)
            print("******")
            return bar
        else:
            print("backtest over ")
            return None
#        try:
#            bar = self.latest_symbol_data[symbol][N]
#        except KeyError:
#            print('backtest over')
#        else:
#            return bar
        
    def get_bars(self):
        for s in self.symbol_list:
            for item in self._get_new_bar(s):
                self.latest_symbol_data[s].append(item)
                
    def update_bars(self):
        """
        push the latest bar to the latest_symbol_data structure
        for all symbols in the symbol list.
        """
#        for s in self.symbol_list:
#            try:
#                bar = self._get_new_bar(s).next()
#            except StopIteration:
#                print("Stop")
#                self.continue_backtest = False
#            else:
#                
#                if bar is not None:
#                    self.latest_symbol_data[s].append(bar)
        
#        #use
#        for s in self.symbol_list:
#            for item in self._get_new_bar(s):
#                self.latest_symbol_data[s].append(item)
                    
                
        self.events.put(MarketEvent())
        
#    def test(self):
#        result = self._get_new_bar(self.symbol_list[0])
#        print(result.next())
        
#a = HistoricCSVDataHandler('MARKET','/Users/linjunqi/Downloads/OnePy_Old-master',["000001"])
#a.test()
        
        