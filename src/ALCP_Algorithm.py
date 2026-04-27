from timeit import default_timer as timer 

def d_cum(a,b):
    if b > T:
        b = T
    c = sum(d[k] for k in range(a, b))
    return c



def q_Operator(period, start_point, jump_step, time_h):
    t = period
    s_p = start_point #s_p = q_tplas1 +1 
    j_s = jump_step
    T = time_h
    e_p = T
    r_cap = cap[t] - d[t]
    
    if r_cap - d_cum(s_p, s_p + j_s) < 0 and s_p + j_s < T + 2:
        while j_s >= 1 and (r_cap - d_cum(s_p, s_p + j_s - 1) < 0):
            j_s -= 1
        e_p = s_p + j_s - 1

    if r_cap - d_cum(s_p, s_p + j_s) >= 0 and s_p + j_s < T + 2:
        while j_s < T - s_p and (r_cap - d_cum(s_p, s_p + j_s + 1) > 0):
            j_s += 1
        e_p = s_p + j_s 
    return e_p

def q_C_k_Opr(period, R_cap, start_point, jump_step, time_h):
    t = period
    s_p = start_point #s_p = q_tplas1 +1 
    j_s = jump_step
    T = time_h
    e_p = T
    r_cap = R_cap
    if r_cap - d_cum(s_p, s_p + j_s) < 0 and s_p + j_s < T + 2:
        while j_s >= 1 and (r_cap - d_cum(s_p, s_p + j_s - 1) < 0):
            j_s -= 1
        e_p = s_p + j_s - 1

    if r_cap - d_cum(s_p, s_p + j_s) >= 0 and s_p + j_s < T + 2:
        while j_s < T - s_p and (r_cap - d_cum(s_p, s_p + j_s + 1) > 0):
            j_s += 1
        e_p = s_p + j_s 
    return e_p


#### upper bound m suggested by ALSP algorithm 
def ALCP_sgg_m(T, cap, d, c):      #ALCP suggestion for m 
    start = timer()
    
    m_hat = {t: T - t + 1 for t in range(1, T+1)}
    q_r_star = {t: T for t in range(1,T+1)}
    r_star = {t: t for t in range(1,T+1)}
    q_tplas1 = {t: T for t in range(1,T+1)}
    
    for t in reversed(range(1, T - c)):
        print(f".....................................................t = {t}")
        q_tplas1[t] = q_Operator(t, t+1, c, T)
        print(f"..q_tplas1_[{t}] = {q_tplas1[t]}")
        q_r_t = q_tplas1[t]
        print(f"r_cap({t})-D[{t+1}, {q_r_t +1}) = [{cap[t] - d[t] - d_cum(t+1, q_r_t +1)}")
        max_r = min(T - 2, T - c + 3)
        for r in range(t + 2,  max_r):
            print(f"----------r = {r}--and--q_r_t = {q_r_t}")
            jj = 0
            print(f"cap_rim[{r}, {q_r_t}) = [{cap[t] - d[t] - d_cum(r, q_r_t)}")
            while jj < T - q_r_t and cap[t] - d[t] - d_cum(r, q_r_t + jj) > 0 :
                jj += 1
                print(f"In while :: cap_rim[{r}, {q_r_t + jj}] = [{cap[t] - d[t] - d_cum(r, q_r_t + jj)}")
            q_r_t = q_r_t + jj
            print(f"          cap_rim[{r}, {q_r_t+1}) = {cap[t] - d[t] - d_cum(r, q_r_t)}")
            q_rplus1_r = q_Operator(r, r + 1, c, T)
            if (q_r_t < T-1 and q_rplus1_r < T-1):
                
                print(f"..q_rplus1_{r} = {q_rplus1_r}")
                                
                prof = sum(a[(t, k)] for k in range(r + 1, q_r_t + 2)) + int(((cap[t] - d_o[t] - d_cum(r + 1, q_r_t + 2))/d_o[r]) * a[t, r])
                compon1 = cap[r] - d_o[r] - d_cum(r + 2, min(q_rplus1_r + 2, T+1))
                compon2 = a[r, q_rplus1_r + 1] / d_o[q_rplus1_r + 1]
                max_t_benef = sum(a[(r, k)] for k in range(r + 2, min(q_rplus1_r + 2, T+1))) + int(compon1 * compon2)
                    
                print(f"..prof:{prof} < max_t_benef:{max_t_benef}")
                if prof < max_t_benef:
                    q_r_star[t] = q_r_t
                    r_star[t] = r
                    m_hat[t] = q_r_t - t
                    print(f"max profit of producing in period{t} to be used in range[{r}, {q_r_t  + 1}) = {prof}")
                    print(f"Max profit of producing in period{r} to be used in range[{r + 1}, {q_rplus1_r+1}] = {max_t_benef}")
                    break
    dur = timer() - start
    Func_q_r_star.Time = dur
    
    
    
    return m_hat, r_star, q_r_star

