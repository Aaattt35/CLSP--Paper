from timeit import default_timer as timer 

###usable version

def d_cum(a,b):
    if b > T:
        b = T
    c = sum(d[k] for k in range(a, b))
    return c



def q_Operator(period, R_cap, start_point, jump_step, time_h):
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


#### upper bound m suggested by ALCP algorithm 
def ALCP_sgg_m(T, cap, d):      #ALCP suggestion for m 
    start = timer()
    
    m_hat = {t: T - t + 1 for t in range(1, T+1)}
    q_r_star = {t: T for t in range(1,T+1)}
    r_star = {t: t for t in range(1,T+1)}
    q_tplas1 = {t: T for t in range(1,T+1)}
    
    for t in reversed(range(1, T - c)):
        
        q_tplas1[t] = q_Operator(t, cap[t] - d[t], t+1, c, T)
        q_r_t = q_tplas1[t]
        max_r = min(T - 2, T - c + 3)
        
        for r in range(t + 2,  max_r):
            jj = 0
            while jj < T - q_r_t and cap[t] - d[t] - d_cum(r, q_r_t + jj) > 0 :
                jj += 1

            q_r_t = q_r_t + jj
            q_rplus1_r = q_Operator(r, cap[r] - d[r], r + 1, c, T)
            
            if (q_r_t < T-1 and q_rplus1_r < T-1):
                                                
                prof = sum(a[(t, k)] for k in range(r + 1, q_r_t + 2)) + int(((cap[t] - d_o[t] - d_cum(r + 1, q_r_t + 2))/d_o[r]) * a[t, r])
                compon1 = cap[r] - d_o[r] - d_cum(r + 2, min(q_rplus1_r + 2, T+1))
                compon2 = a[r, q_rplus1_r + 1] / d_o[q_rplus1_r + 1]
                max_t_benef = sum(a[(r, k)] for k in range(r + 2, min(q_rplus1_r + 2, T+1))) + int(compon1 * compon2)
    
                if prof < max_t_benef:
                    q_r_star[t] = q_r_t
                    r_star[t] = r
                    m_hat[t] = q_r_t - t
                    break
                    
        
        r_star_s = [(r_star[k], k) for k in range(r_star[t], q_r_star[t]+1)]
        
        max_r_star_s, i = max(r_star_s)
        
        Cap_set = [(cap[j], j) for j in range(r_star[t], q_r_star[t]+1)]
        
        R_cap = cap[t] - d[t] + d[i]     #(5)
        R_cap_0 = cap[t] - d[t] + d[i]
        
        J_m = m_hat[t] # jump using m
        
        ml = q_Operator(t, R_cap, r_star[t], J_m, T)# ml0
        mm = 0
        
        while ml < r_star[i]:    #adding cap[i] to (5), we can use ml < max_q_r_star_s
            cap_j, j = min(Cap_set)
            
            if(j < i):        #early periods allocate their productions earlier
                R_cap = R_cap + cap[j] 
                R_cap_0= R_cap_0 + d[j]
                Cap_set.remove((cap_j, j))
                J_m = J_m + m_hat[j]
                ml = q_Operator(t, R_cap, r_star[t], J_m, T)
                mm = mm + 1
                
        ml_0 = q_Operator(t, R_cap_0, r_star[t], J_m, T) 
        ap = ml_0 - q_r_star[t]       
        m_hat[t] = m_hat[t] + ap  #= m_hat[t] + mm + 1                
    
    
    
    dur = timer() - start
    ALCP_sgg_m.Time = dur
    
    
    return m_hat
