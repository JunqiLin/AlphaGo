#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 18:48:43 2019

@author: linjunqi
"""
from data import HistoricCsvDataHandler,HistoricWebDataHandler
import event as ev
from Portfolio import NaivePortfolio
from Strategy import DownAndBuyStrategy
from execution import SimulatedExecutionHandler
import Queue
import time
from datetime import date
import os

events = Queue.Queue()


trainStartDate = date(2015,1,1)
trainEndDate = date(2017,6,1)
#bars = HistoricCsvDataHandler(events,os.getcwd()+'/data',["000001","000002"])

bars = HistoricWebDataHandler(events,['WIKI/AAPL','WIKI/MSFT'],trainStartDate,trainEndDate)   
strategy = DownAndBuyStrategy(bars,events)
port = NaivePortfolio(bars, events,'2015/1/1', initial_capital = 100000.0)
broker = SimulatedExecutionHandler(events)

timelen= 0
for i in bars.symbol_list:
    if len(bars.total_symbol_data[i])> timelen:
        timelen = len(bars.total_symbol_data[i])
        





iter_ = 0
while True:
    print("main loop is %s"%(iter_))
    iter_ = iter_+1
    if(iter_>=timelen):
#        port.calculate_portfolio_returns()
        port.draw_curve()
        break
    # Update the bars (specific backtest code, as opposed to live trading)
    if bars.continue_backtest == True:
        bars.update_bars()
    else:
        print("break")
        break

    while True:
        
        try:
            event = events.get(False)
        except Queue.Empty:
            break
        else:
            if event is not None:
                if event.type == 'MARKET':
                    
                    strategy.calculate_signals(event)
                    port.update_timeindex(event)

                elif event.type == 'SIGNAL':
                    port.update_signal(event)

                elif event.type == 'ORDER':
                    
                    broker.execute_order(event)

                elif event.type == 'FILL':
                    port.update_fill(event)
    
    
