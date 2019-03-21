#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 21:03:45 2019

@author: linjunqi
"""

import pandas as pd
import numpy as np
import datetime
import Queue

from abc import ABCMeta, abstractmethod
from math import floor
from event import FillEvent, OrderEvent
from performance import create_sharpe_ratio, create_drawdowns
import matplotlib.pyplot as plt 
import matplotlib 
matplotlib.style.use('ggplot')
import plotly.offline as py
import plotly.graph_objs as go
#plotly.tools.set_credentials_file(username='JunqiLIN', api_key='lr1c37zw81')

class Portfolio(object):
    """
    The Portfolio class handles the positions and market
    value of all instruments at a resolution of a "bar",
    i.e. secondly, minutely, 5-min, 30-min, 60 min or EOD.
    """
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def update_signal(self,event):
        """
        Acts on a SignalEvent to generate new orders 
        based on the portfolio logic.
        """
        raise NotImplementedError("Should implement update_signal()")
    
    @abstractmethod
    def update_fill(self, event):
        """
        Updates the portfolio current positions and holdings 
        from a FillEvent.
        """
        raise NotImplementedError("Should implement update_fill()")
        

class NaivePortfolio(Portfolio):
     """
     The NaivePortfolio object is designed to send orders to
     a brokerage object with a constant quantity size blindly,
     i.e. without any risk management or position sizing. It is
     used to test simpler strategies such as BuyAndHoldStrategy.
     """
     def __init__(self, bars, events, start_date, initial_capital = 100000.0):
        """
        Initialises the portfolio with bars and an event queue. 
        Also includes a starting datetime index and initial capital 
        (USD unless otherwise stated).

        Parameters:
        bars - The DataHandler object with current market data.
        events - The Event Queue object.
        start_date - The start date (bar) of the portfolio.
        initial_capital - The starting capital in USD.
        """
        self.bars = bars
        self.events = events
        self.symbol_list = self.bars.symbol_list
        self.start_date = start_date
        self.initial_capital = initial_capital
        self.index_ = 0
        self.all_positions = self.construct_all_positions()
        self.current_positions = dict( (k,v) for k, v in [(s, 0) for s in self.symbol_list] )
        self.all_holdings = self.construct_all_holdings()
        self.current_holdings = self.construct_current_holdings()
        
     def construct_all_positions(self):
        """
        Constructs the positions list using the start_date
        to determine when the time index will begin.
        """
        d = dict((k,v) for k,v in [(s,0) for s in self.symbol_list])
        d['datetime']= self.start_date
        return [d]
    
     def construct_all_holdings(self):
        """
        Constructs the holdings list using the start_date
        to determine when the time index will begin.
        """
        d = dict((k,v) for k,v in [(s,0) for s in self.symbol_list])
        d['datetime']= self.start_date
        d['cash']= self.initial_capital
        d['commission']=0.0
        d['total']=self.initial_capital
        return [d]
     def construct_current_holdings(self):
        """
        This constructs the dictionary which will hold the instantaneous
        value of the portfolio across all symbols.
        """
        d = dict((k,v) for k,v in[(s,0) for s in self.symbol_list])
        d['cash'] = self.initial_capital
        d['commission']= 0.0
        d['total']=self.initial_capital
        return d
    
     def update_timeindex(self, event):
        """
        Adds a new record to the positions matrix for the current 
        market data bar. This reflects the PREVIOUS bar, i.e. all
        current market data at this stage is known (OLHCVI).

        Makes use of a MarketEvent from the events queue.
        """
        bars = {}
#        for sym in self.symbol_list:
#            bars[sym] = self.bars.get_latest_bars(sym, N=1)
        
        for sym in self.symbol_list:
            bars[sym] = self.bars.get_bar_byN(sym ,self.index_)
            
        self.index_ += 1
        #Update position
        dp = dict((k,v) for k,v in [(s,0) for s in self.symbol_list])
        dp['datetime'] = bars[self.symbol_list[0]]['date']
        
        for s in self.symbol_list:
            dp[s] = self.current_positions[s]
        
        self.all_positions.append(dp)
        
        #Update holdings
        dh = dict((k,v) for k,v in [(s,0) for s in self.symbol_list])
        dh['datetime'] = bars[self.symbol_list[0]]['date']
        dh['cash']= self.current_holdings['cash']
        dh['commission'] = self.current_holdings['commission']
        dh['total'] = self.current_holdings['cash']
        
        for s in self.symbol_list:
            #Approximation to the real value 
            market_value = self.current_positions[s]*bars[s]['close']
            dh[s] = market_value
            dh['total'] += market_value
            
        self.all_holdings.append(dh)
        
        """
        Creates a pandas DataFrame from the all_holdings
        list of dictionaries.
        """
        curve = pd.DataFrame(self.all_holdings)
        curve.set_index('datetime', inplace=True)
        curve['returns'] = curve['total'].pct_change()
        curve['equity_curve'] = (1.0+curve['returns']).cumprod()
        
        self.equity_curve = curve
        
     def update_positions_from_fill(self, fill):
        """
        Takes a FilltEvent object and updates the position matrix
        to reflect the new position.

        Parameters:
        fill - The FillEvent object to update the positions with.
        """
        # Check whether the fill is a buy or sell
        fill_dir = 0 
        if fill.direction == 'BUY':
            fill_dir= 1
        if fill.direction == 'SELL':
            fill_dir = -1
        # Update holdings list with new quantities
        self.current_positions[fill.symbol] += fill_dir*fill.quantity
        
     def update_holdings_from_fill(self, fill):
        """
        Take the fillevent object and update the holdings matrix 
        to reflect the holdings value
        """
        fill_dir = 0
        if fill.direction == 'BUY':
            fill_dir = 1
        if fill.direction == 'SELL':
            fill_dir = -1
        
        #update the holdings list with new quantities
        fill_cost = fill.price
        cost = fill_dir * fill_cost * fill.quantity
        self.current_holdings[fill.symbol]  += cost
        self.current_holdings['commission'] += fill.commission
        self.current_holdings['cash'] -= (cost + fill.commission)
        self.current_holdings['total'] -= (cost + fill.commission)
        
     def update_fill(self, event):
        """
        update the portfolio current position and holdings 
        from a fillEvent
        """
        if event.type == 'FILL':
            self.update_positions_from_fill(event)
            self.update_holdings_from_fill(event)
#        print(self.current_holdings)
#        print(self.current_positions)
#        print(self.all_holdings)
#        print(self.all_positions)
        
     def generate_down_order(self,signal):
        """
        Simply transacts an OrderEvent object as a constant quantity
        sizing of the signal object, without risk management or
        position sizing considerations.

        Parameters:
        signal - The SignalEvent signal information.
        """
        order = None
        
        symbol = signal.symbol
        direction = signal.signal_type
        strength = signal.strength
        
        mkt_quantity = floor(100 * strength)
        cur_quantity = self.current_positions[symbol]
        order_type = 'MKT'
        price = signal.price
        datetime = signal.datetime
        if direction == 'LONG':
            
            order = OrderEvent(symbol, order_type, mkt_quantity, 'BUY',price,datetime)
        if direction == 'SHORT':
            
            order = OrderEvent(symbol, order_type, mkt_quantity, 'SELL',price,datetime)
        if direction =='EXIT':
            
            order = OrderEvent(symbol, order_type, abs(cur_quantity),'SELL',price,datetime)
        if direction =='EXIT':
            
            order = OrderEvent(symbol, order_type, abs(cur_quantity),'BUY',price,datetime)
        
        return order
     def generate_naive_order(self, signal):
        """
        Simply transacts an OrderEvent object as a constant quantity
        sizing of the signal object, without risk management or
        position sizing considerations.

        Parameters:
        signal - The SignalEvent signal information.
        """
        order = None
        
        symbol = signal.symbol
        direction = signal.signal_type
        strength = signal.strength
        
        mkt_quantity = floor(100 * strength)
        cur_quantity = self.current_positions[symbol]
        order_type = 'MKT'
        price = signal.price
        datetime = signal.datetime
        if direction == 'LONG' and cur_quantity == 0 :
            
            order = OrderEvent(symbol, order_type, mkt_quantity, 'BUY',price,datetime)
        if direction == 'SHORT' and cur_quantity == 0:
            
            order = OrderEvent(symbol, order_type, mkt_quantity, 'SELL',price,datetime)
        if direction =='EXIT' and cur_quantity >0:
            
            order = OrderEvent(symbol, order_type, abs(cur_quantity),'SELL',price,datetime)
        if direction =='EXIT' and cur_quantity <0:
            
            order = OrderEvent(symbol, order_type, abs(cur_quantity),'BUY',price,datetime)
        
        return order

     def update_signal(self, event):
        """
        Acts on a SignalEvent to generate new orders 
        based on the portfolio logic.
        """
        if event.type == 'SIGNAL':
#            order_event = self.generate_naive_order(event)
            order_event = self.generate_down_order(event)
            self.events.put(order_event)
            
            
        
            
            
     def output_summary_stats(self):
        """
        Creates a list of summary statistics for the portfolio such
        as Sharpe Ratio and drawdown information.
        """
        total_return = self.equity_curve['equity_curve'][-1]
        returns = self.equity_curve['returns']
        pnl = self.equity_curve['equity_curve']
        
        sharpe_ratio = create_sharpe_ratio(returns)
        max_dd, dd_duration = create_drawdowns(pnl)
        
        stats = [("Total Return", "%0.2f%%" %((total_return - 1.0)*100.0)),
                 ("Sharpe Ratio","%0.2f"% sharpe_ratio),
                 ("Max DrawDown","%0.2f%%"%(max_dd*100.0)),
                 ("Drawdown Duration","%d"%dd_duration)]
        return stats
     
        
     def calculate_portfolio_returns(self):
#        print("current holding is:")
#        print(self.current_holdings)
#        print("current position is:")
#        print(self.current_positions)
#        print(self.symbol_list)
#        total_quantity = 0
#        for s in self.symbol_list:
#            total_quantity = total_quantity+self.current_positions[s]
#            
#        symbol_percent = dict((k,v) for k,v in [(s,0) for s in self.symbol_list])
##        symbol_percent['datetime'] = self.bars[self.symbol_list[0]][0]['date']
#        for s in self.symbol_list:
#            symbol_percent[s] = self.current_positions[s]/total_quantity
#            
#        
#        print(symbol_percent)
        print(self.all_holdings[-1:])
        print("**********")
        print(self.all_positions[-1:])
    
     def draw_curve(self):
         """
         """
         curve = self.equity_curve
##         print(curve['total'].plot())
#         
#         Total = go.Scatter(
#                 x = curve.index,
#                 y = curve['total']
#                 )
#         cash = go.Scatter(
#                 x0 = curve.index,
#                 y0 = curve['cash']
#                 )
#         commission = go.Scatter(
#                 x = curve.index,
#                 y = curve['commission']
#                 )
#         returns = go.Scatter(
#                 x = curve.index,
#                 y = curve['returns']
#                 )
#         equity_curve = go.Scatter(
#                 x = curve.index,
#                 y = curve['equity_curve']
#                 )
#         py.plot([Total,cash,commission,returns,equity_curve])
         
         trace0 = go.Scatter(
  x = curve.index,
  y = curve['total'],
  
)
         marketvone = go.Scatter(
                 x = curve.index,
                 y = curve['000001']
                 )
         marketvtwo = go.Scatter(
                 x = curve.index,
                 y = curve['000002']
                 )
         

         trace1 = go.Scatter(
  x = curve.index,
  y = curve['cash'],
  yaxis = "y2"
)


         trace4 = go.Scatter(
  x = curve.index,
  y = curve['commission'],
  
  yaxis = "y5"
)
         data = [trace0,marketvone,marketvtwo,trace1,trace4]

                 
#                 
         layout = go.Layout(
     width = 2000,
#    height = 600,
    title = "fixed-ratio axes",
    xaxis = dict(
      nticks = 10,
      domain = [0, 0.45],
      title = "shared X axis"
    ),
    yaxis = dict(
      scaleanchor = "x",
      domain = [0, 0.45],
      title = "1:1"
    ),
    yaxis2 = dict(
      scaleanchor = "x",
      scaleratio = 0.2,
      domain = [0.45,0.85],
      title = "1:5"
    ),
            yaxis5 = dict(
                    domain=[0.85,1],
                    scaleanchor = "x",
                    title="1:8"),

    showlegend= False
)
         fig = go.Figure(data=data, layout=layout)
         py.plot(fig, filename = "aspect-ratio")
        
        
    
        
        
        
        
        
    