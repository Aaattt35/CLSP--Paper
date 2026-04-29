# ============================================
# File: agg_weakl.py
# agg_weakl : modified agg model + constraint(12)
# ============================================
from pyomo.environ import *

def build_Agg_weakl(DP_r, T, s, p, h, d, cap):
    """

    DP_r: dictionary {(i,j) -> v} results of DP recursion.
    T: full time horizon
    s,p,h,d,cap: parameter dictionaries keyed by t.
    """

    # --------------------------------------------
    # 1) Extract F_L_t values for stage 
    # --------------------------------------------
    DP_out = DP_r
    min_by_i = {}  # i -> (j, v)

    for (i, j), v in DP_out.items():
        if i not in min_by_i or j < min_by_i[i][0]:
            min_by_i[i] = (j, v)

    
    F_L_t = { i: v for i, (j, v) in min_by_i.items() }
    T_stage = len(F_L_t) #it has T_stage since DP has run with T_stage

    # --------------------------------------------
    # 2) Build model
    # --------------------------------------------
    agg_weakl = ConcreteModel()  

    agg_weakl.T   = Set(initialize=list(range(1, T+1)))  
    agg_weakl.T_s = Set(initialize=list(range(1, T_stage+1))) # T_s set of time horizon in stage in convexhall

    agg_weakl.X = Var(agg_weakl.T, within=NonNegativeReals)   

    agg_weakl.y = Var(agg_weakl.T, within=Binary)            

    agg_weakl.I = Var(agg_weakl.T, within=NonNegativeReals)  


    # Objective: Minimize sum_j [p(j)*X(j) + s(j)*y(j) + h(j)*I(j)] 
    def obj_expr(agg_weakl):      
        return sum((p[t] * agg_weakl.X[t]) + (s[t] * agg_weakl.y[t]) + (h[t] * agg_weakl.I[t]) for t in agg_weakl.T)   
    agg_weakl.obj = Objective(rule=obj_expr, sense='minimize')

    # Subject to: 
    # G1: Inventory Constraint  
    def g1_rule(agg_weakl, t):  
        if t == agg_weakl.T.first():  # there is no inventory at the begining of the first period.
            return agg_weakl.X[t] == agg_weakl.I[t] + d[t]
        if t == agg_weakl.T.last():
            return agg_weakl.I[t-1] + agg_weakl.X[t] == d[t]
        return agg_weakl.I[t-1] + agg_weakl.X[t] == agg_weakl.I[t] + d[t]  
    agg_weakl.G1 = Constraint(agg_weakl.T, rule=g1_rule)

    # G2: X(t) <= cap(t).y(t) : Capacity constraint
    def g2_rule(agg_weakl,t):
        return agg_weakl.X[t] <= cap[t] * agg_weakl.y[t] 
    agg_weakl.G2 = Constraint(agg_weakl.T, rule=g2_rule)

    # envl( agg + constraint(12))
    # sum_{j=1 to j=t}(p(j)x(j)+s(j)y(j)+h(j)I(j) >= m(t,q)I(t)+b(t,q) 
    # F_t(i(t)) >= m(t,q)I(t)+b(t,q)
    def g3_rule(agg_weakl,t):
        return sum((p[j] * agg_weakl.X[j]) + (s[j] * agg_weakl.y[j]) + (h[j] * agg_weakl.I[j]) for j in agg_weakl.T_s if j < t) + p[t] * agg_weakl.X[t] + s[t] * agg_weakl.y[t] >= F_L_t[t] - h[t] * agg_weakl.I[t]
    
    agg_weakl.G3 = Constraint(agg_weakl.T_s, rule=g3_rule)
    
    return agg_weakl
