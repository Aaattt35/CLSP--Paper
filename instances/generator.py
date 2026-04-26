"""
Instance generator for the Single-Item CLSP test problems.

This script generates the benchmark instances used in the paper.
Parameters follow the experimental design described in the manuscript.
"""

import random
import time
from pyomo.environ import * 
import numpy as np
from timeit import default_timer as timer 
import itertools

def uniform_int(low, high):  
    return random.randint(low, high)


def model_parameters(T, c, f_min, f_max):  
    random.seed()  # reproducible; remove for true randomness  

    T_set = {t for t in range(1, T+1)}
    

    # Fixed constant cost  
    h_const = 40     
    
    # Data generation for demand and capacity in a way that:
    # in every period D(t)=sum_{i=1 to t}(d(i)) <= C(t)=D(t)=sum_{i=1 to t}(cap(i))
    beta = True
    while beta: #while beta is True 
        d = {t: uniform_int(111, 191) for t in T_set}  
        avr_d = sum(d[t] for t in T_set) / (len(T_set))  
        cap = {t: uniform_int(int(0.75*c*avr_d), int(1.25*c*avr_d)) for t in T_set}
        Rcap = {t: cap[t]-d[t] for t in T_set}
        alfa = True
        s_Rcap = 0 
        for t in T_set:
            s_Rcap += Rcap[t]
            if s_Rcap < 0:
                alfa = False
                break
        if alfa == True:
            beta = False
            break
     
    s = {t: uniform_int(int(h_const*f_min), int(h_const*f_max)) for t in T_set}  
    p = {t: uniform_int(81, 119) for t in T_set}
    # h(t) values (constant 10 as you specified)  
    h = {t: h_const for t in T_set}
    
    # h_{tj} = sum_{t=k}^{p-1} h_t for k < p  
    h_tj = {}  
    for t in T_set:  
        for j in T_set:  
            if t < j:  
                h_tj[(t, j)] = sum(h[k] for k in range(t, j))
    
    # a(tj) for t<j (j is the orgin period in LFL solution)  
    a = {}
    a_ratio = {}
    # a(tj) = s(j) - (h(tj) - p(j) + p(t)) * d(j)  for t<j, j=2..T  
    for t in T_set:  
        for j in T_set:  
            if t < j:  
                a[(t, j)] = s[j] - (h_tj[(t, j)] - p[j] + p[t]) * d[j]
                a_ratio[(t,j)] = (s[j] + p[j]*d[j])/((h_tj[(t, j)] + p[t]) * d[j])
 
    return d,p,cap,s,h,a,a_ratio
