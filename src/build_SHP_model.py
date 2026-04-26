def build_Shp(T, s, p, h, d, cap):   
   """
    Build the Shp (short-horizon partitioning) CLSP model.

    This formulation partitions the demand horizon using variables Z_(t,j),
    representing the fraction of demand from interval t..j-1 that is assigned
    to production period t.

    Args:
        T   (int): number of periods
        s   (dict[int,float]): setup cost
        p   (dict[int,float]): production cost
        h   (dict[int,float]): inventory holding cost
        d   (dict[int,float]): demand
        cap (dict[int,float]): capacity

    Returns:
        shp (ConcreteModel)
    """

    shp = ConcreteModel()  

    shp.T   = Set(initialize=list(range(1, T+2)))
    shp.J   = Set(initialize=list(range(1, T+1)))
    
    # defining the decision variables
    shp.Z = Var(((t, j) for t in range(1, T+1) for j in range(t+1, T+2)), within=NonNegativeReals)
    shp.y = Var((t for t in range(1, T+1)), within=Binary)            

    h_tj = {}  # h_{tj} = sum_{t=k}^{p-1} h_t for k < p  
    for t in shp.T:  
        for j in shp.T:
            if t < j:  
                h_tj[(t, j)] = sum(h[k] for k in range(t, j))

    d_tj = {}  
    for t in shp.T:  
        for j in shp.T:
            if t < j:  
                d_tj[(t, j)] = sum(d[k] for k in range(t, j))

    v_tj = {}  
    for t in shp.T:  
        for j in shp.T:
            if t < j:  
                v_tj[(t, j)] = sum(h_tj[(t, i)] * d[i] for i in range(t+1, j)) + d_tj[(t, j)]*p[t]



    # ===========================================================
    # Objective Function
    # Minimize: Σ_{t} A_t y_t + Σ_{t<j} v_tj Z_tj
    # ===========================================================
    def obj_expr(shp):      
        return sum(v_tj[(t, j)] * shp.Z[(t, j)] for (t, j) in shp.Z.keys()) + sum(s[t] * shp.y[t] for t in shp.J)   
    shp.obj = Objective(rule=obj_expr, sense='minimize')

    # Subject to: 
    # ===========================================================
    # SH1: Capacity constraint
    #     Σ_{j>t} d_tj * Z_tj ≤ cap[t]
    # ===========================================================
    def sh1_rule(shp, t):  
        return sum(shp.Z[(t, j)] * d_tj[(t, j)] for j in shp.T if t < j) <= cap[t]  
    shp.SH1 = Constraint(shp.J, rule=sh1_rule)
    # ===========================================================
    # SH2: Partitioning constraints
    #  For t = 1: Σ_{j>1} Z(1,j) = 1
    #  For t > 1: Σ_{j < t} Z(j,t) = Σ_{k > t} Z(t,k)
    #
    #  This ensures the Z variables form a proper interval partition.
    # ===========================================================
    def sh2_rule(shp, t):
        if t==1:
            return sum(shp.Z[(t, j)] for j in shp.T if t < j) == 1
        else:
            return sum(shp.Z[(j, t)] for j in shp.T if j < t) == sum(shp.Z[(t, k)] for k in shp.T if t < k)
    shp.SH2 = Constraint(shp.J, rule=sh2_rule)
    # ===========================================================
    # SH3: Linking constraint
    #     Σ_{j>t} Z(t,j) ≤ y_t
    #
    #  Ensures production period t must be opened (y_t=1) if used.
    # ===========================================================
    def sh3_rule(shp,t):
        return sum(shp.Z[(t, j)] for j in shp.T if t < j) <= shp.y[t]
    shp.SH3 = Constraint(shp.J, rule=sh3_rule)
    
    return shp
