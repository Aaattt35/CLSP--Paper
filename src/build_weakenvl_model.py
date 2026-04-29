# ============================================
# File: agg_weakenvl.py
# agg_weakenvl : modified agg model + constraint(12)
# Using convex hull linear cuts
# ============================================

from pyomo.environ import *
def build_Agg_weakenvl(DP_r, T, s, p, h, d, cap):
    
    DP_out = DP_r
    min_by_i = {}  # i -> (j, v)

    for (i, j), v in DP_out.items():
        if i not in min_by_i or j < min_by_i[i][0]:
            min_by_i[i] = (j, v)

    
    F_L_t = { i: v for i, (j, v) in min_by_i.items() }
    T_stage = len(F_L_t) #it has T_stage since DP has run with T_stage
    
    Cof_i_t, Cof_F_sign, C_v, Dir_s = convexhall_handy_design(DP_r, T_stage, s, p, h, d, cap)
    #Cof_i_t, Cof_F_sign, C_v = convexhall_design(T_stage, s, p, h, d, cap)    
    agg_weakenvl = ConcreteModel()  

    agg_weakenvl.T   = Set(initialize=list(range(1, T+1)))  
    agg_weakenvl.T_s = Set(initialize=list(range(1, T_stage+1))) # T_s set of time horizon in stage in convexhall
    agg_weakenvl.convex_L = Set(initialize=list(range(1, len(Cof_F_sign)+1)))

    agg_weakenvl.X = Var(agg_weakenvl.T, within=NonNegativeReals)   

    agg_weakenvl.y = Var(agg_weakenvl.T, within=Binary)            

    agg_weakenvl.I = Var(agg_weakenvl.T, within=NonNegativeReals)  


    # Objective: Minimize sum_j [p(j)*X(j) + s(j)*y(j) + h(j)*I(j)] 
    def obj_expr(agg_weakenvl):      
        return sum((p[t] * agg_weakenvl.X[t]) + (s[t] * agg_weakenvl.y[t]) + (h[t] * agg_weakenvl.I[t]) for t in agg_weakenvl.T)   
    agg_weakenvl.obj = Objective(rule=obj_expr, sense='minimize')

    # Subject to: 
    # G1: Inventory Constraint  
    def g1_rule(agg_weakenvl, t):  
        if t == agg_weakenvl.T.first():  # there is no inventory at the begining of the first period.
            return agg_weakenvl.X[t] == agg_weakenvl.I[t] + d[t]
        if t == agg_weakenvl.T.last():
            return agg_weakenvl.I[t-1] + agg_weakenvl.X[t] == d[t]
        return agg_weakenvl.I[t-1] + agg_weakenvl.X[t] == agg_weakenvl.I[t] + d[t]  
    agg_weakenvl.G1 = Constraint(agg_weakenvl.T, rule=g1_rule)

    # G2: X(t) <= cap(t).y(t) : Capacity constraint
    def g2_rule(agg_weakenvl,t):
        return agg_weakenvl.X[t] <= cap[t] * agg_weakenvl.y[t] 
    agg_weakenvl.G2 = Constraint(agg_weakenvl.T, rule=g2_rule)

    # weakenvl( agg + constraint(12))
    # sum_{j=1 to j=t}(p(j)x(j)+s(j)y(j)+h(j)I(j) >= m(t,q)I(t)+b(t,q) 
    # F_t(i(t)) >= m(t,q)I(t)+b(t,q)
    def g3_rule(agg_weakenvl,t,k):
        if Cof_F_sign[k][0]==t:
            if Cof_F_sign[k][1] < 0:
                return sum((p[j] * agg_weakenvl.X[j]) + (s[j] * agg_weakenvl.y[j]) + (h[j] * agg_weakenvl.I[j]) for j in agg_weakenvl.T_s if j <= t) >= -agg_weakenvl.I[t] * Cof_i_t[k] - C_v[k]
            else:
                return Constraint.Skip
        return Constraint.Skip
    agg_weakenvl.G3 = Constraint(agg_weakenvl.T_s, agg_weakenvl.convex_L, rule=g3_rule)
     
    
    # F_t(i(t)) >= m(t,q)I(t)+b(t,q)
    def g4_rule(agg_weakenvl,t):
        return sum((p[j] * agg_weakenvl.X[j]) + (s[j] * agg_weakenvl.y[j]) + (h[j] * agg_weakenvl.I[j]) for j in agg_weakenvl.T_s if j < t) + p[t] * agg_weakenvl.X[t] + s[t] * agg_weakenvl.y[t] >= F_L_t[t] - h[t] * agg_weakenvl.I[t]
    
    agg_weakenvl.G4 = Constraint(agg_weakenvl.T_s, rule=g4_rule)
    

    return agg_weakenvl
