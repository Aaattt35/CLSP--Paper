"""
Run optimization experiment for a given instance.
Connects to the CLSP optimization models.
"""
#import cplex
import random
import time
from pyomo.environ import * 
import numpy as np
from timeit import default_timer as timer 
import itertools
def uniform_int(low, high):  
    return random.randint(low, high)
import sys
import os
import time
from pyomo.environ import SolverFactory, value, TerminationCondition
from Read_input_txt_file import Read_input  # new: import the solver function
from build_AGG_model import build_m_Agg
from build_FAL_model import build_Fal
from build_SHP_model import build_Shp
from build_TPM_m_model import build_TPM_m
from build_TPM_model import build_Tpm
from build_dp_solver import DP_CLSP
from build_envl_model import build_Agg_envl
from build_weakenvl_model import build_Agg_weakenvl
from build_weakl_model import build_Agg_weakl
from ALCP_Algorithm import _ALCP_sgg_m

from pyomo.environ import value

def clean_value(x):
    try:
        v = value(x)      # اگر Pyomo variable باشد، مقدارش را می‌گیرد
        if v is None:
            return float('nan')
        return float(v)
    except:
        return float('nan')

def read_instance(path):
    data = {}
    with open(path, "r") as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=")
                data[key.strip()] = value.strip()
    return data


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_experiment.py instance_file")
        sys.exit(1)

    instance_file = sys.argv[1]
    instance_path = os.path.abspath(instance_file)

# ============================================Reading Input and Assigning Instance Values to Parameters===============================================
    Parameters = Read_input(instance_path)

    # To get the planning horizon 'T':
    T = Parameters.get("T")
    d = Parameters.get("d")
    p = Parameters.get("p")
    cap = Parameters.get("cap")
    s = Parameters.get("s")
    h = Parameters.get("h")

    cap = {int(k): v for k, v in cap.items()}
    d   = {int(k): v for k, v in d.items()}
    s   = {int(k): v for k, v in s.items()}
    p   = {int(k): v for k, v in p.items()}
    h   = {int(k): v for k, v in h.items()}
    
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
 
#-----------------------------------------------------------------------------------------------------------------------------------------------------

# =======================================================Defining Solve and Report Functions==========================================================
def solve_and_report(DP_t, model, label, time_L, solver_type='highs'):
    
    time_limit = time_L
    # Determine status
    status = "Unknown"    
    
    if(label == "weakl"):
        solver = SolverFactory(solver_type)
        solver.options['timelimit'] = time_limit - DP_t
        start = time.time()
        res = solver.solve(model, tee=False)
        end = time.time()
        cal_time = end - start + DP_t #the third part include DP time and other function process time
    
    elif(label == "TPM_m"):
        solver = SolverFactory(solver_type)
        solver.options['timelimit'] = time_limit - find_m_cap_based_al_S.Time
        start = time.time()
        res = solver.solve(model, tee=False)
        end = time.time()
        cal_time = end - start + find_m_cap_based_al_S.Time 
    
    elif(label == "envl"):
        solver = SolverFactory(solver_type)
        solver.options['timelimit'] = time_limit - DP_t
        start = time.time()
        res = solver.solve(model, tee=False)
        end = time.time()
        cal_time = end - start + build_Agg_envl.Time + DP_t
        
    elif(label == "weakenvl"):
        solver = SolverFactory(solver_type)
        solver.options['timelimit'] = time_limit - DP_t
        start = time.time()
        res = solver.solve(model, tee=False)
        end = time.time()
        cal_time = end - start + build_Agg_envl.Time + DP_t 
        
    else:   
        solver = SolverFactory(solver_type)
        solver.options['timelimit'] = time_limit
        start = time.time()
        res = solver.solve(model, tee=False)
        end = time.time()
        cal_time = end - start 
    

    solver_info = res.solver
    sys_time = getattr(solver_info, 'time', None)
    if sys_time is None:
        for candidate in ['user_time', 'wallclock_time', 'system_time', 'cpu_time']:
            sys_time = getattr(solver_info, candidate, None)
            if sys_time is not None:
                break

    if sys_time is None:
        print(f"time of {label} reported by sys: <not provided by solver>")
        sys_time = cal_time
    else:
        print(f"time of {label} reported by sys: {sys_time}")

    #print(f"--- {label} ---")
    try:
        opt_val = value(model.obj())
        #print(f"Optimal objective value: {opt_val}")

    except Exception:
        #print("Optimal objective value: not available")
        pass


    try:
        status = str(res.solver.termination_condition)
    except Exception:
        pass

    # Best effort to get objective
    try:
        opt_val = value(model.obj())
    except Exception:
        opt_val = None
        
    c = clean_value(c)
    s = clean_value(s)
    f = clean_value(f)
    o_f = clean_value(o_f)
    sys_time = clean_value(sys_time)
    opt_val = clean_value(opt_val)
    status = clean_value(status)
    line = (f"{label}, {T},  {c},  {f},  "
            f"{cal_time:.3f}, {sys_time:.3f},  "
            f"{opt_val}, {status}")
    #line = f"{label}: Time_handy={cal_time:.3f}s Time_sys={sys_time:.3f}s Objective={opt_val} Status={status}"
        
    print(line)    
    
    return cal_time, sys_time, opt_val, status
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# ===============================================Main body of Running optimization experiments over all models=======================================

T_h = [90]     #, 100, 120, 150, 200, 300, 500, 1000, 2000,  
C =[2]        #36, 26, 18, 12, 8, 5 , 3 , 2   
F= [ (400, 1200) ]   #, (2400, 2800), (5600, 6400), (12800, 19200)
noi = [1] #, 2, 3, 4 #number of Instance 
T_L = 1800  #Time limit for running each model

Result_form = np.dtype([
    ('Prob_N', np.int32),
    ('Model_N', 'U16'),   # Unicode string, up to 16 characters
    ('F', np.int32, (2,)),
    ('c', np.int32),
    ('T', np.int32),
    ('Sample', np.int32),
    ('Obj_F', np.float64),
    ('Solv_T', np.float64),
    ('SYS_Rep_T', np.float64),    #system reported time
    ('Solv_Status', 'U16'),  # Unicode string
    ('T_stage', np.int32),
])

Result_run = np.empty(0, dtype=Result_form)

ins = 1

for f in F:
    for c in C:
        Bre_Con = 0 # the break condition if all models could not solve stop generating samples in that t
        for T in T_h:
            print('number of T which no model could solve')
            print(Bre_Con)
            if Bre_Con >=4:
                break
            for i_n in noi:
                T_stage = min(int(T*0.3), 30)
                f_min = f[0]
                f_max = f[1]
                #d, p, cap, s, h, a, ar = model_parameters(T, c, f_min, f_max)
                m = _ALCP_sgg_m(T, cap, d, c)
                
                # Defining parial DP to be used in envl and weakl
                DP_r = DP_CLSP(T_stage, s, p, h, d, cap) #Dp partial results
                T_stage = max(t for (t, _) in DP_r.keys())

                
                DP_r_t_s = DP_CLSP.Time
                print(f"time of Par_DP reported by sys: {DP_r_t_s}")
                print(f"T_stages: {T_stage}")
                # Define a list of model builders and their arguments
                models_to_solve = [
                    ("M_Agg", lambda: build_m_Agg(T, s, p, h, d, cap)),
                    ("TPM", lambda: build_Tpm(T, s, p, d, cap, h)),
                    ("TPM_m", lambda: build_TPM_m(m, T, s, p, d, cap, h)),
                    ("FAL", lambda: build_Fal(T, s, p, d, cap, h)), 
                    ("SHP", lambda: build_Shp(T, s, p, h, d, cap)),
                    ("weakl", lambda: build_Agg_weakl(DP_r, T, s, p, h, d, cap)),
                    ("envl", lambda: build_Agg_envl(DP_r, T_stage, T, s, p, h, d, cap)),
                    ("weakenvl", lambda: build_Agg_weakenvl(DP_r, T, s, p, h, d, cap))
                ]
                
                StaT = []
                # Run in a loop
                for label, builder in models_to_solve:
                    mdl = builder()  # build the Pyomo model
                    c_t, s_t, o_f, stat = solve_and_report(DP_r_t_s, mdl, label, T_L, solver_type='highs')
                    new_rec = (ins, label, f, c, T, i_n, o_f, c_t, s_t, stat, T_stage)
                    Result_run = np.append(Result_run, np.array(new_rec, dtype=Result_form))
                    StaT.append(stat)
                
                ###if solving with pure DP is required add the determined section here
                ###if solving with pure DP is required add the determined section here
                
                if not any(i == 'optimal' for i in StaT):    # no 'optimal' present in StaT
                    print(f"Break condition= {Bre_Con}")
                    Bre_Con = Bre_Con + 1     #Break_condition   
                
                ins += 1
                    
