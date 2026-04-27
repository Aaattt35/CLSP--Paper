# m_agg : modified agg model
def build_m_Agg(T, s, p, h, d, cap): 
    """
    Builds and returns the aggregated CLSP optimization model (m_agg).

    Args:
        T (int): planning horizon.
        s, p, h, d, cap (dict[int, float]): setup cost, production cost,
            holding cost, demand, and capacity per period.

    Returns:
        ConcreteModel: a Pyomo model object ready to be solved.
    """
    m_agg = ConcreteModel()  

    m_agg.T = Set(initialize=list(range(1, T+1)))  

    # Decision variables
    m_agg.X = Var(m_agg.T, within=NonNegativeReals)   
    m_agg.y = Var(m_agg.T, within=Binary)            
    m_agg.I = Var(m_agg.T, within=NonNegativeReals) 


    # Objective function: Minimize sum_j [p(j)*X(j) + s(j)*y(j) + h(j)*I(j)] 
    def obj_expr(m_agg):      
        return sum((p[t] * m_agg.X[t]) + (s[t] * m_agg.y[t]) + (h[t] * m_agg.I[t]) for t in m_agg.T)   
    m_agg.obj = Objective(rule=obj_expr, sense='minimize')

    # Subject to: 
    # G1: Inventory Constraint  
    def g1_rule(m_agg, t):  
        if t == m_agg.T.first():  # there is no inventory at the begining of the first period.
            return m_agg.X[t] == m_agg.I[t] + d[t]
        if t == m_agg.T.last():
            return m_agg.I[t-1] + m_agg.X[t] == d[t]
        return m_agg.I[t-1] + m_agg.X[t] == m_agg.I[t] + d[t]  
    m_agg.G1 = Constraint(m_agg.T, rule=g1_rule)

    # G2: Capacity constraint X(t) <= cap(t).y(t)
    def g2_rule(m_agg,t):
            return m_agg.X[t] <= cap[t] * m_agg.y[t] 
    m_agg.G2 = Constraint(m_agg.T, rule=g2_rule)
    return m_agg
