#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 11:21:06 2019

@author: linjunqi
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 22:38:46 2019

@author: linjunqi
"""
import datetime
import Queue

from abc import ABCMeta, abstractmethod

from event import FillEvent, OrderEvent


class ExecutionHandler(object):
    """
    
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def execute_order(self, event):
        """
        
        """
        raise NotImplementedError("Should implement execute_order()")
        
class SimulatedExecutionHandler(ExecutionHandler):
    """
    
    """
    def __init__(self, events):
        self.event = events
        
    
    def execute_order(self, event):
        """
        
        """
        
        if event.type =='ORDER':
            #event.print_order()
            fill_event = FillEvent(datetime.datetime.utcnow(), event.symbol,
                                   'ARCA', event.quantity, event.direction,event.quantity*6.8, event.price, None)
            
            self.event.put(fill_event)
        
        
        
        
        
        
        
        
        