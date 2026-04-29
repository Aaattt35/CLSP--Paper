from timeit import default_timer as timer 

###ALCP algorithm  

def _ALCP_sgg_m(T, cap, d, c):

    start = timer()
    m_hat = {t: T - t + 1 for t in range(1, T+1)}
    m_hat_sen_2 = {t: T - t + 1 for t in range(1, T+1)}
    q_r_star = {t: T for t in range(1,T+1)}
    r_star = {t: T for t in range(1,T+1)}
    q_tplas1_t = {t: T for t in range(1,T+1)}

    
    def d_cum(a,b):
        if b > T:
            b = T
        c = sum(d[k] for k in range(a, b))
        return c


    
    def q_Operator(period, R_cap, start_point, jump_step, time_h):
        t = period
        s_p = start_point #s_p: start point = q_tplas1 +1 
        j_s = jump_step
        T = time_h
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
        if (q_r_t < T and q_rplus1_r < T):
            delta = sum(a[(t, k)] for k in range(r, q_r_t + 1)) + int(((cap[t] - d[t] - d_cum(r, q_r_t + 1))/d[q_r_t + 1]) * a[t, q_r_t + 1]) - sum(a[(r, k)] for k in range(r + 1, q_rplus1_r))
            return delta
        else:
            return 1

    ##### computig r_star(t) and q_r_star(t) = q_Operator(t, cap[t] - d[t], r_star(t), c, T)    
    for t in reversed(range(1, T - c)):
        print(f"....................................t = {t}")
        max_r = min(T - 2, T - c + 3)  
        for r in range(t + 2,  max_r):
            print(f".............r = {r}")
            print("Checking cap for t:", t)
            print("cap keys:", list(cap.keys())[:10], "...", list(cap.keys())[-10:])
            q_r_t = q_Operator(t, cap[t] - d[t], r, c, T)
            q_rplus1_r = q_Operator(r, cap[r] - d[r], r + 1, c, T)
            print(f"q_r_t = {q_r_t}")
            print(f"q_rplus1_r = {q_rplus1_r}")
            if (q_r_t == T or q_rplus1_r == T or r >= q_r_t):
                break
            if (_Delta_(t, r, q_r_t, q_rplus1_r) < 0):
                q_r_star[t] = q_r_t
                r_star[t] = r
                m_hat_sen_2[t] = q_r_t - t #m_hat from second senario
                break
    
        print(f"r_star[{t}] = {r_star[t]}")
        print(f"q_r_star[{t}] = {q_r_star[t]}")
        max_r_star_s = T
        if r_star[t] < q_r_star[t]:
            r_star_set = {k: r_star[k] for k in range(r_star[t], q_r_star[t]+1)}
            Cap_set = {k: cap[k] for k in range(r_star[t], q_r_star[t]+1)}
            e = max(reversed(r_star_set), key=r_star_set.get)
            max_r_star_s = r_star_set[e]
            print(f"r_star_set = {r_star_set}")
        if (max_r_star_s < T):
            R_cap = cap[t] - d[t] + d[e] 
            R_cap_0= cap[t] - d[t] + d[e]
            del Cap_set[e] 
            print(f"R_cap = cap[{t}] - d[{t}] + d[{e}] = {R_cap}")
            J_m = m_hat_sen_2[t] # jump using m_har of second senario
            ml = q_Operator(t, R_cap, t + 1, J_m, T)# ml(0,0)
            mm = 0
            print(f"ml0= {ml} < max = r_star_set[{i}] = {max_r_star_s}")
            while ml < r_star_set[e] and Cap_set:    #adding cap[i] to (5), we can use ml < max_q_r_star_s
                print(f"capset = {Cap_set}")
                print(f"ml= {ml} < max = r_star_set[{e}] = {r_star_set[e]}")
                m_j =  min(Cap_set, key = Cap_set.get)
                cap_min_j = Cap_set[m_j]
                print(f"m_j= {m_j} and cap_{m_j} = {cap_min_j}")
                print(f"m_j = {m_j} < e = {e}")
                if(m_j < e):        #early periods should allocate their productions earlier()
                    print(f"m_j = {m_j} < e = {e}")
                    R_cap = R_cap + cap[m_j] 
                    R_cap_0= R_cap_0 + d[m_j]
                    del Cap_set[m_j]
                    J_m = J_m + m_hat_sen_2[j]
                    ml = q_Operator(t, R_cap, t, J_m, T)
                    print(f"mile ston == {ml}")
                    mm = mm + 1
                else:
                    del Cap_set[m_j]
    
            ml_0 = q_Operator(t, R_cap_0, t + 1, m_hat_sen_2[t], T)
            print(f"ffffffffffffffffffffff mile ston 0 == {ml_0}")
            ap = ml_0 - q_Operator(t, cap[t] - d[t], t + 1, c, T)      
            m_hat[t] = m_hat_sen_2[t] + ap  #= m_hat[t] + mm + 1                
            print(f"mmmmmmmmmmmmmmmm    mmmmmmmmmmmmmmmmmm   mmmmmmmmmmmmm   m_hat {t} == {m_hat[t]}")
    dur = timer() - start
    _ALCP_sgg_m.Time = dur
    return m_hat
    
