#TPM-m: Transferring Present Demand to Previous Manufacturing Periods Within an m-Period Window

from pyomo.environ import *

def build_TPM_m(m, T, s, p, d, cap, h):
    
    tpm_m = ConcreteModel()  
    tpm_m.T   = Set(initialize=list(range(1, T+1)))

    # h_{tj} = sum_{t=k}^{p-1} h_t for k < p  
    h_tj = {}  
    for t in tpm_m.T:  
        for j in tpm_m.T:  
            if t < j:  
                h_tj[(t, j)] = sum(h[k] for k in range(t, j))

    # a(tj) for t<j (j is the orgin period in LFL solution)  
    a_tj = {}  
    # a(tj) = s(j) - (h(tj) - p(j) + p(t)) * d(j)  for t<j, j=2..T  
    for t in tpm_m.T:  
        for j in tpm_m.T:  
            if t < j:  
                a_tj[(t, j)] = s[j] - (h_tj[(t, j)] - p[j] + p[t]) * d[j]

    #variable definition
    tpm_m.O = Var(tpm_m.T, bounds=[0, 1])   #satisfy constraint(): 0 <= O(t) <= 1   for t=2,...,T-1
    tpm_m.O_b = Var(tpm_m.T, within=Binary)            #satisfy constraint(): O(t) = {0,1}   for t=T
    tpm_m.q  = Var(tpm_m.T, within=Binary)  #satisfy (t for t in range(2, T)) : constraint(): q(t) = {0,1}   for t=2,...,T-1
    # z_{t j} for t<j  
    tpm_m.z = Var(((t, j) for t in range(1, T) for j in range (t+1, min(t+m[t]+1, T+1))), within=NonNegativeReals)  #satisfy constraint(): z(t,j)>=0   for t=1,2,...,T-1  and  t<j

    # ----------------------------------------------------------------------------------------------------------------------
    # Objective: Minimize sum_j (A_j + p_j*d_j) - sum_{t<j} a_{t j} * z_{t j}  
    # ----------------------------------------------------------------------------------------------------------------------
    def obj_expr(tpm_m):
        sa = sum(s[k] for k in tpm_m.T) + sum(p[k]*d[k] for k in tpm_m.T)
        z_term = sum(a_tj[(t, j)] * tpm_m.z[(t, j)] for t in tpm_m.T for j in tpm_m.T if t < j < min(T+1, t+m[t]+1))  
        return sa - z_term  
    tpm_m.obj = Objective(rule=obj_expr, sense='minimize')

    # Subject to: 

    # ----------------------------------------------------------------------------------------------------------------------
    # Cm1: Capacity
    # Σ_j z[t,j]*d[j] ≤ cap[t] – d[t]
    # for all t<T<t+m[t]+1
    # ---------------------------------------------------------------------------------------------------------------------- 
    def cm1_rule(tpm_m, t):  
        if t == tpm_m.T.last():  # no constraint for last period, or adapt to T-1 as in GAMS  
            return Constraint.Skip  
        return sum(tpm_m.z[(t, j)] * d[j] for j in tpm_m.T if t < j < min(T+1, t+m[t]+1) )<= cap[t] - d[t]  
    tpm_m.Cm1 = Constraint(tpm_m.T, rule=cm1_rule)
    # ----------------------------------------------------------------------------------------------------------------------
    # Cm2: z(t,j) + O(t) <= 1 
    # for t < j < t+m[t]+1, using O_b only when t is last
    # ----------------------------------------------------------------------------------------------------------------------
    def cm2_rule(tpm_m, t, j):   
        if (tpm_m.T.first() < t < tpm_m.T.last()):
            if(t < j < t+m[t]+1):
                return tpm_m.z[(t, j)] + tpm_m.O[t] <= 1
        return Constraint.Skip
    tpm_m.Cm2 = Constraint(tpm_m.T,tpm_m.T, rule=cm2_rule)
    # ----------------------------------------------------------------------------------------------------------------------
    # Cm3: O(j) = sum_{j-m[t]-1<t<j} z(t j})  
    # ----------------------------------------------------------------------------------------------------------------------
    def cm3_rule(tpm_m, j):  
        if j == tpm_m.T.first():  
            return tpm_m.O[j] == 0  # Since O(1)=0
        if j == tpm_m.T.last():
            return tpm_m.O_b[j] == sum(tpm_m.z[(t, j)] for t in tpm_m.T if max(0, j-m[t]-1) < t < j)
        return tpm_m.O[j] == sum(tpm_m.z[(t, j)] for t in tpm_m.T if max(0, j-m[t]-1) < t < j)  
    tpm_m.Cm3 = Constraint(tpm_m.T, rule=cm3_rule)
    # ----------------------------------------------------------------------------------------------------------------------
    # C4: O(t) <= q(t)  
    #for t=2, ... ,T-1
    # ----------------------------------------------------------------------------------------------------------------------
    def c4_rule(tpm_m, t):  
        if tpm_m.T.first() < t < tpm_m.T.last():  
            return tpm_m.O[t] <= tpm_m.q[t]  
        else:
            return Constraint.Skip 
    tpm_m.C4 = Constraint(tpm_m.T, rule=c4_rule)
    # ----------------------------------------------------------------------------------------------------------------------
    # C5: z(t,j) <= (1-q(t))  
    #for t=2,...,T-1  and  t < j < t+m[t]+1
    # ----------------------------------------------------------------------------------------------------------------------
    def c5_rule(tpm_m, t, j):  
        if (tpm_m.T.first() < t < tpm_m.T.last()):
            if (t < j < t+m[t]+1):
                return tpm_m.z[t,j] + tpm_m.q[t] <= 1   
        return Constraint.Skip 
    tpm_m.C5 = Constraint(tpm_m.T, tpm_m.T, rule=c5_rule)
    # ----------------------------------------------------------------------------------------------------------------------
    # C6: (1-q(j))*cap(j)+ sum_{1<t<j-1}z(t j)*d(j)≥d(j) 
    #for j=2,...,T-1
    # ----------------------------------------------------------------------------------------------------------------------
    def c6_rule(tpm_m, j):
        if tpm_m.T.first() < j < tpm_m.T.last():
            return (1-tpm_m.q[j])*cap[j] + sum(tpm_m.z[(t, j)] * d[j] for t in tpm_m.T if max(0, j-m[t]-1) < t < j) >= d[j]
        else:
            return Constraint.Skip 
    tpm_m.C6 = Constraint(tpm_m.T, rule=c6_rule)
    
    return tpm_m
