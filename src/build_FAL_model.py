# build_fal_model.py
def build_Fal(T, s, p, d, cap, h): 
    """
    Build the 'Fal' aggregated CLSP model (Wagner-Whitin type formulation).

    Args:
        T   (int): number of periods (planning horizon length)
        s   (dict[int, float]): setup cost per period t
        p   (dict[int, float]): unit production cost per period t
        d   (dict[int, float]): demand in period t
        cap (dict[int, float]): production capacity in period t
        h   (dict[int, float]): inventory holding cost per unit per period t

    Returns:
        fal (ConcreteModel): Pyomo model instance of the Fal formulation.
    """
    
    fal = ConcreteModel()  
    
    # Defining the decision Variables
    fal.T = Set(initialize=list(range(1, T+1))) 
    fal.X = Var(((t, j) for t in range(1, T+1) for j in range(t, T+1)), within=NonNegativeReals)
    fal.y = Var(fal.T, within=Binary)            #satisfy constraint(): O(t) = {0,1}   for t=T

    # h_{tj} = sum_{t=k}^{p-1} h_t for k < p  
    h_tj = {}  
    for t in fal.T:  
        for j in fal.T:
            if t == j:
                h_tj[(t, j)] = 0
            if t < j:  
                h_tj[(t, j)] = sum(h[k] for k in range(t, j))

    # Objective: Minimize sum_j [p(j)*X(j) + s(j)*y(j) + h(j)*I(j)] 
    def obj_expr(fal):      
        return sum((h_tj[(t, j)] + p[t]) * fal.X[(t, j)] for (t, j) in fal.X.keys()) + sum(s[t] * fal.y[t] for t in fal.T)   
    fal.obj = Objective(rule=obj_expr, sense='minimize')

    # Subject to: 
    # F1: Capacity Constraint  
    def f1_rule(fal, t):  
        return sum(fal.X[(t, j)] for j in fal.T if t <= j) <= cap[t]  
    fal.f1 = Constraint(fal.T, rule=f1_rule)

    # F2: sum_{t<=j} X(t j}) == d(j)
    def f2_rule(fal, j):    
        return sum(fal.X[(t, j)] for t in fal.T if t <= j) == d[j] 
    fal.F2 = Constraint(fal.T, rule=f2_rule)

    # F3: X(t,j) <= d(j)*y(t) : Capacity constraint
    def f3_rule(fal,t,j):
        if j >= t:
            return fal.X[t,j] <= d[j]*fal.y[t]
        else:
            return Constraint.Skip
    fal.F3 = Constraint(fal.T,fal.T, rule=f3_rule)
    
    return fal
