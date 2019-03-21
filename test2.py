#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 14:07:36 2019

@author: linjunqi
"""
symbol_list=['001','002']


def get_new_bar(s):
    df = symbol_list.index(s)
    for i in range(2):
        yield ({'symbol':s, 'date':'20140101',
                    'open':i,
                    'low':1122,
                    'high':1122,
                    'close':1122,
                    'volume':1122 })
    
    
    
#a = symbol_list[0]
##print(type(a))
#bar = get_new_bar(int(a))
#print(type(bar))
#for item in bar:
#    print(item)
#    
    

latest_symbol_data={}
for s in symbol_list:
    latest_symbol_data[s] = []

for s in symbol_list:
    
    bar = get_new_bar(s)
    
    latest_symbol_data[s].append(bar)
    
#print(len(latest_symbol_data))
bar_list = latest_symbol_data['002']

b = bar_list
v = bar_list[0:]


    
print(type(b[0]))

print(next(v[0]))

#print(type(bar))
#for item in bar:
#    print item
#print(bar[0:1])

#a=[1,2,3,4,5]
#print(a[-1:])
#    
