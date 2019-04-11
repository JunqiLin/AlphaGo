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
import quandl
from datetime import date
quandl.ApiConfig.api_key = "nJisbyjbJ9ghcE9jsz6r"


class DataHandler(object):
    """
    
    """
    __metaclass__ = ABCMeta
    @abstractmethod
    
    def get_latest_bars(self, symbol, N=1):
        """
        
        """
        raise NotImplementedError("Should implement get_latest_bars()")

    @abstractmethod
    
    def update_bars(self):
        """
        Pushes the latest bar to the latest symbol structure
        for all symbols in the symbol list.
        """
        raise NotImplementedError("Should implement update_bars()")
    

        
class HistoricCsvDataHandler():
    """
    get symbol_list data from file
    """
    def __init__(self, events,file_dir, symbol_list):
        self.events = events
        self.file_dir = file_dir
        self.symbol_list = symbol_list      
        self.total_symbol_data={}
        self.symbol_latest_data={}
        self.continue_backtest = True
        self._get_data_from_files()
#        self.get_bars()
        
    def _get_data_from_files(self):
        """
        open file and transfer data to dataframe
        """
        for symbol in self.symbol_list:
            self.total_symbol_data[symbol]=pd.read_csv(os.path.join(self.file_dir,'%s.csv'%symbol), header = 0,index_col = 0, names=['datetime', 
                                  'open', 'low', 'high', 'close','volume','oi'])
                
            self.symbol_latest_data[symbol]=[]
            
    def update_bars(self):
        """
        put MarketEvent to event queue
        """
        self.events.put(MarketEvent())
        
    def get_latest_bars(self, symbol,n):
        """
        get the latest N days data
        """
        bars_list=[]
        ##dataframe
        df = self.total_symbol_data[symbol].tail(n)
        for i in range(n):
            item = {'symbol':symbol, 'date':str(df.index[i]),
                    'open':df[['open']].iat[i,0],
                    'low':df[['low']].iat[i,0],
                    'high':df[['high']].iat[i,0],
                    'close':df[['close']].iat[i,0],
                    'volume':df[['volume']].iat[i,0]}
            bars_list.append(item)
        return bars_list
    
    def get_n_bars(self, symbol, n):
        """
        get N-th day bar (index from 0)
        """
        if n<len(self.total_symbol_data[symbol]):
            df = self.total_symbol_data[symbol].iloc[n,:]
            item = {'symbol':symbol, 'date':str(df.name),
                    'open':df['open'],
                    'low':df['low'],
                    'high':df['high'],
                    'close':df['close'],
                    'volume':df['volume']}
            return item
        else:
            print('N-th bar is out of range')
            return
        


class HistoricWebDataHandler(DataHandler):
    """
    get symbol_list data from Web
    """
    def __init__(self, events, symbol_list, start, end):
        self.events = events
        self.symbol_list = symbol_list
        self.start = start
        self.end = end
        
        """
        total_symbol_data:   dict{'symbol':'dataframe data'}
        """
        self.total_symbol_data= {}
        self.symbol_latest_data={}
        self.continue_backtest = True
        
        self._get_data_from_web()

        
    def _get_data_from_web(self):
        """
        use quandl to get historical data from web
        """
        for symbol in self.symbol_list:
            symbol_data = quandl.get(symbol, start_date=self.start, end_date=self.end)
            self.total_symbol_data[symbol] = symbol_data
            
            
    def update_bars(self):
        """
        put MarketEvent to event queue
        """
        self.events.put(MarketEvent())
        
    
    """
    get bars return by the format type==dict, key:symbol,open,low,high,close,volume
    """
    
    
    def get_latest_bars(self, symbol,n):
        """
        get the latest N days data
        """
        bars_list=[]
        ##dataframe
        df = self.total_symbol_data[symbol].tail(n)
        for i in range(n):
            item = {'symbol':symbol, 'date':str(df.index[i]),
                    'open':df[['Open']].iat[i,0],
                    'low':df[['Low']].iat[i,0],
                    'high':df[['High']].iat[i,0],
                    'close':df[['Close']].iat[i,0],
                    'volume':df[['Volume']].iat[i,0]}
            bars_list.append(item)
        return bars_list
        
    
    def get_n_bars(self, symbol, n):
        """
        get N-th day bar (index from 0)
        """
        df = self.total_symbol_data[symbol].iloc[n,:]
        item = {'symbol':symbol, 'date':str(df.name),
                    'open':df['Open'],
                    'low':df['Low'],
                    'high':df['High'],
                    'close':df['Close'],
                    'volume':df['Volume']}
        return item
    

#trainStartDate = date(2015,1,1)
#trainEndDate = date(2017,6,1)
#bars = HistoricWebDataHandler('marker',['WIKI/AAPL'],trainStartDate,trainEndDate)   
##print(bars.get_latest_bars('WIKI/AAPL',5))
#
#print(bars.get_n_bars('WIKI/AAPL',1))
     