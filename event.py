#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 09:51:38 2019

@author: linjunqi
"""

##event class: parent class
##market event class: marker data update
##strategy object
##signal event class: include long or short, symbol, time aso
##portfolio
##order event class: order information
##executionhandler
##fillevent



class Event(object):
    pass


class MarketEvent(Event):
    #Handles the event of receiving a new market update with corresponding bars.
    def __init__(self):
        self.type = "MARKET"
        
class SignalEvent(Event):
    #Handles the event of sending a Signal from a Strategy object.
    #This is received by a Portfolio object and acted upon.
    def __init__(self, symbol, datetime, signal_type,strength, price):
        self.type = "SIGNAL"
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type
        self.strength = strength
        self.price = price
    def print_signal(self):
        print (" Symbol=%s, Price=%s, Datetime=%s"%(self.symbol, self.price,self.datetime))
       
        
class OrderEvent(Event):
    #Handles the event of sending an Order to an execution system.
    #The order contains a symbol (e.g. GOOG), a type (market or limit),
    #quantity and a direction.
    def __init__(self, symbol, order_type, quantity, direction,price,datetime):
        self.type = "ORDER"
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction
        self.price = price
        self.datetime =datetime
        
    def print_order(self):
        print ("Order : Symbol=%s, Type=%s, Quantity=%s, Direction=%s, Price=%s, Datetime=%s"%(self.symbol, self.order_type, self.quantity, self.direction, self.price,self.datetime))
       
class FillEvent(Event):
    """
    
    """

    def __init__(self, timeindex, symbol, exchange, quantity, 
                 direction, fill_cost, price, commission=None):
        """
        
        """
        
        self.type = 'FILL'
        self.timeindex = timeindex
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost
        self.price = price

        # Calculate commission
        if commission is None:
            self.commission = self.calculate_ib_commission()
        else:
            self.commission = commission

    def calculate_ib_commission(self):
        """
        
        """
        
        full_cost = 1.3
        if self.quantity <= 500:
            full_cost = max(1.3, 0.013 * self.quantity)
        else: # Greater than 500
            full_cost = max(1.3, 0.008 * self.quantity)
        full_cost = min(full_cost, (0.5 / 100.0 )* self.quantity * self.fill_cost)
        return full_cost
        
    