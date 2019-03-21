#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 21:22:46 2019

@author: linjunqi
"""
import os 
import pandas as pd
import numpy as np
#class Student(object):
#    def __init__(self,name):
#        self.__name = name
#        
#    def _test_one(self):
#        print("test one")
#        
#    def __test_two(self):
#        print("test two")
#        
#    def test_three(self):
#        self.__test_two()
#        
#s = Student("David")
#print(s._Student__name)
#s._test_one()
#s.test_three()
#print(os.path.dirname)

#symbol_data={}
#symbol_data[1]=pd.read_csv("/Users/linjunqi/Onelocal/OnePy_Old-master/000001.csv", header = 0,
#                        index_col = 0, names=['datetime', 'open', 'low', 'high', 'close','volume','oi']
#                            )
#symbol_data[2]=pd.read_csv("/Users/linjunqi/Onelocal/OnePy_Old-master/000001.csv", header = 0,
#                        index_col = 0, names=['datetime', 'open', 'low', 'high', 'close','volume','oi']
#                            )
#indexone = symbol_data[1].index
#indextwo = symbol_data[2].index
#
#
#print(indexone.union(indextwo))
#data={'1':[1,2,3,4],'2':[2,3,4,5]}
#df=pd.DataFrame(data).T
#dataone = {'2':[2,3,4,5],'3':[4,5,6,7]}
#dfone=pd.DataFrame(dataone).T
#indexrow = df.index.union(dfone.index)
#indexrow = ['2','1']


        
        
#df = df.reindex(index=indexrow,method='pad').iterrows()
#print(df)

#for s in symbol_list:
#    for (k,v) in [(s,0)]:
#        print(k,v)
    #print(s)
    
#
#symbol_list=["000001","000002","000003"]    
##a=[[1,2],[3,4],[5,6]]
##b=[j for i in a for j in i]
##print(b)
#
#
#ds = dict((k,v) for k,v in [(s,0) for s in symbol_list])
#d = dict( (k,v) for k, v in [(s, 0) for s in symbol_list])
#
#print([d])
#print([ds])
#import time
#while True:
#    # Update the bars (specific backtest code, as opposed to live trading)
#    print('out loop')
#    
#    # Handle the events
#    while True:
#        print('inner loop')
#        break
#    time.sleep(0.1*60)

    # 10-Minute heartbeat
    
    
array = [6,7.5,8,0,1]
ndarray = np.array(array)
print(ndarray)
print(type(ndarray))


