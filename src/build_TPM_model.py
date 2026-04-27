# build_tpm_model.py
# TPM: Transforming PPs into Non-PPs with Modification (TPM)
def build_Tpm(T, s, p, d, cap, h):
    """
    TPM: Transferring Present Demand to Previous Manufacturing Periods.

    This model implements the TPM reformulation of the CLSP.
    It assumes:
        - all demands d[t] are satisfied in their original periods,
        - production can be moved to earlier periods, subject to capacity,
        - the objective is expressed as:
              sum_j (s_j + p_j d_j) - sum_{t<j} a_{t j} z_{t j}

    Args:
        T   (int): number of periods
        s   (dict[int,float]): setup cost s[t]
        p   (dict[int,float]): production cost p[t]
        d   (dict[int,float]): demand d[t]
        cap (dict[int,float]): capacity cap[t]
        h   (dict[int,float]): inventory holding cost h[t]

    Returns:
        tpm (ConcreteModel)
    """   
    
    tpm = ConcreteModel()  
    tpm.T   = Set(initialize=list(range(1, T+1))) 
    # -----------------------------------------------------------
    # Precomputed coefficients h_tj, a_tj
    # -----------------------------------------------------------
    # h_tj = sum_{k=t}^{j-1} h[k], for t < j  
    h_tj = {}  
    for t in tpm.T:  
        for j in tpm.T:  
            if t < j:  
                h_tj[(t, j)] = sum(h[k] for k in range(t, j))
              
    # a_tj = s[j] - (h_tj - p[j] + p[t]) * d[j], for t < j
    # a(tj) for t<j (j is the orgin period in LFL solution)  
    a_tj = {}   
    for t in tpm.T:  
        for j in tpm.T:  
            if t < j:  
                a_tj[(t, j)] = s[j] - (h_tj[(t, j)] - p[j] + p[t]) * d[j] 
  
    tpm.O = Var(tpm.T, bounds=[0, 1])   #satisfy constraint(): 0 <= O(t) <= 1   for t=2,...,T-1    
    tpm.O_b = Var(tpm.T, within=Binary)            #satisfy constraint(): O(t) = {0,1}   for t=T    
    tpm.q  = Var((t for t in range(2, T)), within=Binary)  #satisfy constraint(): q(t) = {0,1}   for t=2,...,T-1
    
    # z_{t j} for t<j  
    tpm.z = Var(((t, j) for t in range(1, T) for j in range(t+1, T+1)), within=NonNegativeReals)  #satisfy constraint(): z(t,j)>=0   for t=1,2,...,T-1  and  t<j

    # -----------------------------------------------------------
    # Objective
    #   Minimize sum_j (s_j + p_j d_j) - sum_{t<j} a_tj z_tj
    # -----------------------------------------------------------
    def obj_expr(tpm):
        sa = sum(s[k] for k in tpm.T) + sum(p[k]*d[k] for k in tpm.T)
        z_term = sum(a_tj[(t, j)] * tpm.z[(t, j)] for (t, j) in tpm.z.keys())  
        return sa - z_term  
    tpm.obj = Objective(rule=obj_expr, sense='minimize')
    
    # Subject to: 
    # -----------------------------------------------------------
    # C1: Capacity
    #   For t = 1,...,T-1:
    #       sum_{j>t} z[t,j] * d[j] ≤ cap[t] - d[t]
    #   (no constraint for the last period T)
    # -----------------------------------------------------------  
    def c1_rule(tpm, t):  
        if t == tpm.T.last():  # no constraint for last period, or adapt to T-1 as in GAMS  
            return Constraint.Skip  
        return sum(tpm.z[(t, j)] * d[j] for j in tpm.T if t < j) <= cap[t] - d[t]  
    tpm.C1 = Constraint(tpm.T, rule=c1_rule)
     
    # Define an index set of all (t, j) with t < j
    tpm.J = Set(dimen=2, initialize=lambda tpm: [(t, j) for t in tpm.T for j in tpm.T if t < j])

    # -----------------------------------------------------------
    # C2: z(t,j) + O(t) ≤ 1 for all t<j, except last period
    #   Uses O[t] (continuous) for t < T
    # -----------------------------------------------------------
    def c2_rule(tpm, t, j):
        if t == tpm.T.last():
            return Constraint.Skip
        return tpm.z[(t, j)] + tpm.O[t] <= 1
    tpm.C2 = Constraint(tpm.J, rule=c2_rule)
    
    # -----------------------------------------------------------
    # C3: Flow definition of O
    #   - j = 1 : O[1] = 0
    #   - 2 ≤ j ≤ T-1 : O[j] = sum_{t<j} z[t,j]
    #   - j = T : O_b[T] = sum_{t<T} z[t,T]
    # -----------------------------------------------------------
    def c3_rule(tpm, j):  
        if j == tpm.T.first():  
            return tpm.O[j] == 0  # Since O(1)=0 
        if j == tpm.T.last():
            return tpm.O_b[j] == sum(tpm.z[(t, j)] for t in tpm.T if t < j)
        return tpm.O[j] == sum(tpm.z[(t, j)] for t in tpm.T if t < j)  
    tpm.C3 = Constraint(tpm.T, rule=c3_rule)
    
    # -----------------------------------------------------------
    # C4: O(t) ≤ q(t), for t=2,...,T-1
    # -----------------------------------------------------------
    def c4_rule(tpm, t):  
        if tpm.T.first() < t < tpm.T.last():  
            return tpm.O[t] <= tpm.q[t]  
        else:
            return Constraint.Skip 
    tpm.C4 = Constraint(tpm.T, rule=c4_rule)
    
    # -----------------------------------------------------------
    # C5: z(t,j) ≤ 1 - q(t), for t=2,...,T-1, t<j
    #   (rewritten as z(t,j) + q(t) ≤ 1)
    # -----------------------------------------------------------
    def c5_rule(tpm, t, j):  
        if tpm.T.first() < t < tpm.T.last(): 
            return tpm.z[t,j] + tpm.q[t] <= 1   
        else:
            return Constraint.Skip 
    tpm.C5 = Constraint(tpm.J, rule=c5_rule)
    
    # -----------------------------------------------------------
    # C6: (1 - q(j)) * cap[j] + sum_{1 < t < j-1} z(t,j) * d[j] ≥ d[j]
    #   for j=2,...,T-1
    #   (in code, t<j ensures t ≤ j-1, and t>1 ensures 1 < t)
    # -----------------------------------------------------------
    def c6_rule(tpm, j):
        if tpm.T.first() < j < tpm.T.last():
            return (1-tpm.q[j])*cap[j] + sum(tpm.z[(t, j)] * d[j] for t in tpm.T if t < j) >= d[j]
        else:
            return Constraint.Skip 
    tpm.C6 = Constraint(tpm.T, rule=c6_rule)
    
    return tpm 
