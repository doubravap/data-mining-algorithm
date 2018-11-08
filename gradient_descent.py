#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 22:23:58 2018

@author: junewang
"""

import math
w0=1
w1=1
w2=1
w3=1
def f(x,w0,w1,w2,w3):
    w=w0+x[0]*w1+x[1]*w2+x[2]*w3
    res=1/(1+pow(math.e,-1*w))
    return res
x=[[0,0,0],[0,1,0],[1,0,0],[1,1,1]]
y=[1,0,0,1]
y_pre=[0]*4
y_pre1=[0]*4
for i in range(10000):
    for j in range(4):
        y_pre[j]=f(x[j],w0,w1,w2,w3)
        if y_pre[j]>=0.5:
            y_pre1[j]=1
        else:
            y_pre1[j]=0        
    e=[pow((y[k]-y_pre1[k]),2) for k in range(4)]
    error=sum(e)/4
    if error<0.001:
        print("w0=",'%.2f' % w0)
        print("w1=",'%.2f' %w1)
        print("w2=",'%.2f' %w2)
        print("w3=",'%.2f' %w3)
        print("error=",error)
        break
    w1=w1+sum([(y[i]-y_pre[i])*x[i][0] for i in range(4)])
    w2=w2+sum([(y[i]-y_pre[i])*x[i][1] for i in range(4)])
    w3=w3+sum([(y[i]-y_pre[i])*x[i][2] for i in range(4)])


import math
w0=1
w1=-1.5
w2=-1.5
def f(x,w0,w1,w2):
    w=w0+x[0]*w1+x[1]*w2
    res=1/(1+pow(math.e,-1*w))
    return res
x=[[0,0],[0,1],[1,0],[1,1]]
y=[1,0,0,1]
y_pre=[0]*4
y_pre1=[0]*4
for i in range(10000):
    for j in range(4):
        y_pre[j]=f(x[j],w0,w1,w2)
        if y_pre[j]>0.5:
            y_pre1[j]=1
        else:
            y_pre1[j]=0        
    e=[pow((y[k]-y_pre1[k]),2) for k in range(4)]
    if error-sum(e)/4<0.001:
        print("w0=",'%.2f' % w0)
        print("w1=",'%.2f' %w1)
        print("w2=",'%.2f' %w2)
        print("error=",error)
        break
    error=sum(e)/4
    w1=w1+sum([(y[i]-y_pre[i])*x[i][0] for i in range(4)])
    w2=w2+sum([(y[i]-y_pre[i])*x[i][1] for i in range(4)])
    