# dp_solver.py
import time
from functools import lru_cache
from pyomo.environ import SolverFactory, value
from time import time as now_time

def compute_bounds(T, d, cap):
    """
    Compute lower bounds (L) and upper bounds (U) for inventory levels at each period.
    
    Args:
        T (int): planning horizon.
        d (dict[int, float]): demand per period.
        cap (dict[int, float]): capacity per period.

    Returns:
        L (dict[int, float]), U (dict[int, float]) :
        - L: minimum inventory in each period.
        - U: maximum inventory in each period.
    """
    # DP approach: Computing_bounds_function
    T_set = {t for t in range(1, T+1)}
    #computing L(t)
    dc = {t: d[t] - cap[t] for t in T_set}
    L = {t: 0 for t in T_set}
    for t in range(1, T):
        max_between = 0
        curr = 0
        for j in range(t+1, T+1):
                curr += dc[j]
                if curr > max_between:
                    max_between = curr
        L[t] = max(0, max_between)

    #Computing U(t)
    future_d = {t: 0 for t in T_set}
    for j in reversed(range(1, T+1)):
        if j == T:
            future_d[j] = 0
        else:
            future_d[j] = future_d[j+1] + d[j+1]

    U = {t: 0 for t in T_set}
    C = {t: 0 for t in T_set}
    D = {t: 0 for t in T_set}

    sC = 0
    sD = 0
    for t in T_set:
        sC += cap[t]
        sD += d[t]
        C[t] = sC
        D[t] = sD
        if t == T:
            U[t] = 0
        else:
            U[t] = min((C[t] - D[t]), future_d[t])
    return L, U



    def DP_CLSP(T, s, p, h, d, cap, timelimit=100):
    print("Dp is stating.............................................................")
    print(f"DP timelimit: {timelimit:.3f} seconds")
    dur = 0
    start = timer()
    T_set = {t for t in range(1, T+1)}
    L, U = compute_bounds(T, d, cap)
    
    F_t_s = {}
    
    for t in T_set:
        if t==1:
            for I_t in range(L[t], U[t]+1):
                            
                x_min = max(0, (I_t + d[t]))
                x_max = min(cap[t], (I_t + d[t]))
                rund_1 = False
                
                min_F_1_s = p[t]*x_min + s[t] + h[t]*I_t
                for x_1 in range(x_min, x_max+1):
                    F_1_s_x = p[t]*x_1 + s[t] + h[t]*I_t
                    
                    if F_1_s_x < min_F_1_s :
                        min_F_1_s = F_1_s_x
                            
                F_t_s[t, I_t] = min_F_1_s                

        else:
            for I_t in range(L[t], U[t]+1):
                x_min = min(cap[t], max(0, (I_t + d[t] - U[t-1])))
                x_max = min(cap[t], (I_t + d[t] - L[t-1]))
                rund_1 = False
                for x_t in range(x_min, x_max+1):
                    prev_I = I_t + d[t] - x_t
                    if prev_I in range(L[t-1], U[t-1]+1):
                        if x_t > 0:
                            y_t = 1
                        else:
                            y_t = 0
                        if rund_1 == True:
                            F_t_s_x = p[t]*x_t + s[t]*y_t + h[t]*I_t + F_t_s[(t-1), prev_I]
                            if F_t_s_x < min_F_t_s :
                                min_F_t_s = F_t_s_x
                        else:
                            min_F_t_s = p[t]*x_t + s[t]*y_t + h[t]*I_t + F_t_s[(t-1), prev_I]
                            rund_1 = True

                F_t_s[t, I_t] = min_F_t_s
                
        dur = timer() - start        
        if(dur >= timelimit):
            print(f"DP Solv_t: {dur:.3f} seconds")
            break
    
    
    DP_CLSP.Time = dur        
    return F_t_s
