from timeit import default_timer as timer 

###ALCP_algorithm_Final

def _ALCP_sgg_m(T, cap, d, c, h, p, s):
    
    start = timer()
    m_hat = {t: T - t + 1 for t in range(1, T+1)}
    m_hat_1 = {t: T - t + 1 for t in range(1, T+1)} #m_hat when all periods in range r_t_* to q_r_t_* have been converted to pp.
    m_hat_sen_2 = {t: T - t + 1 for t in range(1, T+1)}
    q_r_star = {t: T for t in range(1,T+1)}
    r_star = {t: T for t in range(1,T+1)}
    q_tplas1_t = {t: T for t in range(1,T+1)}

    T_set = {t for t in range(1, T+1)}
    # h_{tj} = sum_{t=k}^{p-1} h_t for k < p  
    h_tj = {}  
    for t in T_set:  
        for j in T_set:  
            if t < j:  
                h_tj[(t, j)] = sum(h[k] for k in range(t, j))
    
    # a(tj) for t<j (j is the orgin period in LFL solution)  
    a = {}
    a_ratio = {}
    # a(tj) = s(j) - (h(tj) - p(j) + p(t)) * d(j)  for t<j, j=2..T  
    for t in T_set:  
        for j in T_set:  
            if t < j:  
                a[(t, j)] = s[j] - (h_tj[(t, j)] - p[j] + p[t]) * d[j]
                a_ratio[(t,j)] = (s[j] + p[j]*d[j])/((h_tj[(t, j)] + p[t]) * d[j])

    
    def d_cum(a,b):
        if b > T:
            b = T
        c = sum(d[k] for k in range(a, b))
        return c


    def q_Operator(period, R_cap, start_point, jump_step):
        t = period
        s_p = start_point #s_p: start point = q_tplas1 +1 
        j_s = jump_step
        e_p = T + 1  # e_p: ending point
        r_cap = R_cap
        rim_cap = r_cap - d_cum(s_p, s_p + j_s) #remaind capacity if period t produced for its own and peirods in [s_p, s_p + j_s - 1]
        if rim_cap < 0 and s_p + j_s < T + 2:
            while j_s >= 1 and (r_cap - d_cum(s_p, s_p + j_s - 1) < 0):
                j_s -= 1
            e_p = s_p + j_s - 1

        if rim_cap >= 0 and s_p + j_s < T + 2:
            while j_s < T - s_p and (r_cap - d_cum(s_p, s_p + j_s + 1) > 0):
                j_s += 1
            e_p = s_p + j_s 
        return e_p - 1


    def _Delta_(period_a, period_b, period_c, period_d):
        t = period_a
        r = period_b
        q_r_t = period_c 
        q_rplus1_r = period_d
        t_profit = r_profit = 0
        if (q_r_t < T and q_rplus1_r < T):
            for k in range(r, q_r_t + 1):
                if a[t, k] > 0:
                    t_profit = t_profit + a[t, k]  #+ int(((cap[t] - d[t] - d_cum(r, q_r_t + 1))/d[q_r_t + 1]) * a[t, q_r_t + 1]) 

            for k in range(r + 1, q_rplus1_r + 1):
                if a[r, k] > 0:
                    r_profit = r_profit + a[r, k]
            delta = t_profit - r_profit
            return delta
        else:
            return 1

    def _r_star_(p_t, Available_cap, start_step = 1): #provides r_star[t] for point t with capcity equal to available_cap 
        t = p_t
        r_str = T
        for r in range(t + 1 + start_step,  T):
            q_r_t = q_Operator(t, Available_cap, r, c)
            q_rplus1_r = q_Operator(r, cap[r] - d[r], r + 1, c)
            if (q_r_t == T): #or q_rplus1_r == T
                r_str = T
                break
                
            if (r < q_rplus1_r):
                if (r <= q_r_t and _Delta_(t, r, q_r_t, q_rplus1_r) < 0 and q_Operator(t, Available_cap, r-1, c) >= r-1):
                    r_str = r - 1
                    break

        return r_str


    ##### computig r_star(t) and q_r_star[t]
    for t in reversed(range(1, T - c)):
        r_star[t] = _r_star_(t, cap[t] - d[t])
        q_r_star[t] = q_Operator(t, cap[t] - d[t], r_star[t], c)
        m_hat_sen_2[t] = q_r_star[t] - t #m_hat from second senario       
        ##### computing m_hat_1[t] for the situation when all periods in range r_star(t) to q_r_star[t]
        ##### has been converted to pp
        if r_star[t] < T:
            extra_cap = cap[t] - d[t] 
            for new_pp in range(r_star[t],  q_r_star[t]+1):
                extra_cap = extra_cap + cap[new_pp]

            r_pp_str = _r_star_(t, extra_cap) #### provides r^* when all periods in safty range was converted to pp
            q_r_pp_str = q_Operator(t, extra_cap, r_pp_str, c)
            if q_r_pp_str < T :
                m_hat_1[t] = q_r_pp_str - t  # m_hat_1[t] : this is useful just for c<5. 

        if q_r_star[t] - r_star[t] >= 1:
            r_star_set = {k: r_star[k] for k in range(r_star[t], q_r_star[t]+1)}
            Cap_set = {k: cap[k] for k in range(r_star[t], q_r_star[t]+1)}

            e = max(reversed(r_star_set), key=r_star_set.get)
            max_r_star_s = r_star_set[e]

            if (max_r_star_s < T):
                R_cap = cap[t] - d[t] + d[e] 
                R_cap_0= cap[t] - d[t] + d[e]
                del Cap_set[e] 
                J_m = m_hat_sen_2[t] # jump using m_har of second senario
                ml = q_Operator(t, R_cap, t + 1, J_m)# ml(0,0)
                mm = 0
                while ml < r_star_set[e] and Cap_set:    #adding cap[i] to (5), we can use ml < max_q_r_star_s
                    m_j =  min(Cap_set, key = Cap_set.get)
                    cap_min_j = Cap_set[m_j]
                    if(m_j < e):        #early periods should allocate their productions earlier()
                        R_cap = R_cap + cap[m_j] 
                        R_cap_0= R_cap_0 + d[m_j]
                        del Cap_set[m_j]
                        J_m = J_m + m_hat_sen_2[m_j]
                        ml = q_Operator(t, R_cap, t+1, J_m)
                        mm = mm + 1
                    else:
                        del Cap_set[m_j]

                if ml > r_star_set[e]:
                    ml_0 = q_Operator(t, R_cap_0, t + 1, m_hat_sen_2[t])
                    ap = ml_0 - q_Operator(t, cap[t] - d[t], t + 1, c)      
                    m_hat[t] = m_hat_sen_2[t] + ap  #= m_hat[t] + mm + 1                

        m_hat[t] = min(m_hat[t], m_hat_1[t])

    dur = timer() - start
    _ALCP_sgg_m.Time = dur

    return m_hat
    
