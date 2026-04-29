# A Python3 program to find convex hull of a set of points. Refer 
# https://www.geeksforgeeks.org/dsa/convex-hull-using-graham-scan/

import time
import math
import numpy as np
from functools import cmp_to_key
from pyomo.environ import *
# -----------------------------------------------------
# Class to represent a point
# -----------------------------------------------------
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Method to check equality of two points
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
# -----------------------------------------------------
# Function to find orientation of the triplet (a, b, c)
# Returns -1 if clockwise, 1 if counter-clockwise, 0 if collinear
# -----------------------------------------------------
def orientation(a, b, c):
    val = (a.x * (b.y - c.y)) + \
          (b.x * (c.y - a.y)) + \
          (c.x * (a.y - b.y))
    if val < 0:
        return -1  # Clockwise
    elif val > 0:
        return 1   # Counter-clockwise
    return 0       # Collinear
# -----------------------------------------------------
# Function to calculate the squared distance between two points
# -----------------------------------------------------
def distSq(a, b):
    return (a.x - b.x)**2 + (a.y - b.y)**2

def line_from_points(P, Q):
    # Returns coefficients A, B, C for line in form Ax + By + C = 0
    # Through points P=(P.x, P.y), Q=(Q.x, Q,y)
    A = P.y - Q.y
    B = P.x - Q.x
    C = P.x*Q.y - Q.x*P.y
    return A, B, C

# Function to find the convex hull from a list of 2D points
def Graham_ConvexHull(points):
    
    start = time.time()
    n = len(points)
    
    # If there are two pints return the points
    if n == 2:
        return(points)
    # Convex hull is not possible if there are fewer than 3 points
    if n < 2:
        return [[-1]]

    # Convert list of coordinates to Point objects
    a = [Point(p[0], p[1]) for p in points]

    # Find the point with the lowest y-coordinate (and leftmost in case of tie)
    p0 = min(a, key=lambda p: (p.y, p.x))

    #remove the minimum point as the reference point
    a.pop(0)

    def compare(p1, p2):
        o = orientation(p0, p1, p2)
        if o == 0:
            return distSq(p0, p1) - distSq(p0, p2)
        return -1 if o < 0 else 1

    a_sorted = sorted(a, key=cmp_to_key(compare))
    a_sor = []
    a_sor.append(p0)
    
    # Remove collinear points (keep farthest)
    i=0
    while i < len(a_sorted) - 2:
        #print(f"i= {i}")
        for j in range(i+1, len(a_sorted)-1):
            #print(f"j= {j}")
            if(orientation(a_sorted[i], a_sorted[j], a_sorted[j+1]) != 0):
                a_sor.append(a_sorted[j])
                #print("finding breakpoint")
                #L_ind_p = j    #last index collinera point with point i
                break
        #print(f"last index collinera point with point i: {j}")
        i = j

    a_sor.append(a_sorted[-1])   

    m = len(a_sor) #number of remaining points without collinear points

    # Initialize stack with first two points
    st = [a_sor[0], a_sor[1]]

    # Process the remaining points
    for i in range(2, m):
        #print(f"-----point {i}th in the list without collinear points")
        while len(st) > 1 and \
              orientation(st[-2], st[-1], a_sor[i]) >= 0:
            #print(f"a clock wise orientation with new point so delete the last point")
            st.pop()
        st.append(a_sor[i])
        #print(f"a counter-clock wise orientation with new point so add the new point")


    # Final check for valid hull
    if len(st) < 2:
        return [[-1]]
    
    
    co_aa = []
    co_bb = []
    cons = [] 
    st.append(p0)

    #Calculating the corresponding Equations:
    for i in range (0, len(st)-1):
        aa, bb, cc = line_from_points(st[i], st[i+1])
        co_aa.append(aa)
        co_bb.append(bb)
        cons.append(cc)
    
    end = time.time()
    duration = end - start
    
    Graham_ConvexHull.Time = duration 
    Graham_ConvexHull.Equations = (co_aa, co_bb, cons)
    
    
    # Convert points back to list of [x, y]
    return [[int(p.x), int(p.y)] for p in st]

#def Graham_equation(points)


def convexhall_handy_design(DP_r,T_stage, s, p, h, d, cap):
    DP_out = DP_r
    a1 = []   # Co_i
    a2 = []   # (t , sign)
    c  = []   # RHS
    a3 = []   # inequality direction (+1 or -1)
  
    for t in range(1, T_stage+1):
        # Build a NumPy array of shape (N, 3)
        pts = np.array([[j, v] for (i, j), v in DP_out.items() if i==t], dtype=int)
        if pts.shape[0] >= 2:  # need at least 3 non-collinear points for 2D hull
            # Driver Code
            
            points = pts
            manual_hall = np.array(Graham_ConvexHull(points))
            c_a, c_b, c_c = np.array(Graham_ConvexHull.Equations)

            Co_F_i = c_b
            # Compute the absolute value of |Co_F_i|.

            Co_i = c_a / Co_F_i
            Co_F_sign = Co_F_i / np.abs(Co_F_i)
            Rhs_norm = c_c / Co_F_i


            #the inequality direction is >= or <=
            mean_conv = manual_hall.mean(axis=0)
            enqu_side = Co_i * mean_conv[0] + Co_F_sign * mean_conv[1]+ Rhs_norm
            enqu_side = np.sign(enqu_side).astype(int)  # yields -1, 0, 1

            T_new = Co_i.shape[0]
            for i in range(T_new):
                a1.append(Co_i[i]) 
                a2.append([t, Co_F_sign[i]])
                c.append(Rhs_norm[i])
                a3.append(enqu_side[i])
    
    CO_i_t = {t+1: a1[t] for t in range(len(a1))}
    CO_F_sign = {t+1: a2[t] for t in range(len(a2))}
    Const_v = {t+1: c[t] for t in range(len(c))}
    Dir_S = {t+1: a3[t] for t in range(len(a3))}  #Direction_Sign
    #+ Graham_ConvexHull.Time
    convexhall_handy_design.Time = Graham_ConvexHull.Time 
    return CO_i_t, CO_F_sign, Const_v, Dir_S
# =====================================================================================================
# File: agg_weakenvl.py
# agg_weakenvl : modified agg model + constraint(12)
# Using convex hull linear cuts
# =====================================================================================================

def build_Agg_weakenvl(DP_r, T, s, p, h, d, cap):
    
    DP_out = DP_r
    min_by_i = {}  # i -> (j, v)

    for (i, j), v in DP_out.items():
        if i not in min_by_i or j < min_by_i[i][0]:
            min_by_i[i] = (j, v)

    
    F_L_t = { i: v for i, (j, v) in min_by_i.items() }
    T_stage = len(F_L_t) #it has T_stage since DP has run with T_stage
    
    Cof_i_t, Cof_F_sign, C_v, Dir_s = convexhall_handy_design(DP_r, T_stage, s, p, h, d, cap)
    #Cof_i_t, Cof_F_sign, C_v = convexhall_design(T_stage, s, p, h, d, cap)    
    agg_weakenvl = ConcreteModel()  

    agg_weakenvl.T   = Set(initialize=list(range(1, T+1)))  
    agg_weakenvl.T_s = Set(initialize=list(range(1, T_stage+1))) # T_s set of time horizon in stage in convexhall
    agg_weakenvl.convex_L = Set(initialize=list(range(1, len(Cof_F_sign)+1)))

    agg_weakenvl.X = Var(agg_weakenvl.T, within=NonNegativeReals)   

    agg_weakenvl.y = Var(agg_weakenvl.T, within=Binary)            

    agg_weakenvl.I = Var(agg_weakenvl.T, within=NonNegativeReals)  


    # Objective: Minimize sum_j [p(j)*X(j) + s(j)*y(j) + h(j)*I(j)] 
    def obj_expr(agg_weakenvl):      
        return sum((p[t] * agg_weakenvl.X[t]) + (s[t] * agg_weakenvl.y[t]) + (h[t] * agg_weakenvl.I[t]) for t in agg_weakenvl.T)   
    agg_weakenvl.obj = Objective(rule=obj_expr, sense='minimize')

    # Subject to: 
    # G1: Inventory Constraint  
    def g1_rule(agg_weakenvl, t):  
        if t == agg_weakenvl.T.first():  # there is no inventory at the begining of the first period.
            return agg_weakenvl.X[t] == agg_weakenvl.I[t] + d[t]
        if t == agg_weakenvl.T.last():
            return agg_weakenvl.I[t-1] + agg_weakenvl.X[t] == d[t]
        return agg_weakenvl.I[t-1] + agg_weakenvl.X[t] == agg_weakenvl.I[t] + d[t]  
    agg_weakenvl.G1 = Constraint(agg_weakenvl.T, rule=g1_rule)

    # G2: X(t) <= cap(t).y(t) : Capacity constraint
    def g2_rule(agg_weakenvl,t):
        return agg_weakenvl.X[t] <= cap[t] * agg_weakenvl.y[t] 
    agg_weakenvl.G2 = Constraint(agg_weakenvl.T, rule=g2_rule)

    # weakenvl( agg + constraint(12))
    # sum_{j=1 to j=t}(p(j)x(j)+s(j)y(j)+h(j)I(j) >= m(t,q)I(t)+b(t,q) 
    # F_t(i(t)) >= m(t,q)I(t)+b(t,q)
    def g3_rule(agg_weakenvl,t,k):
        if Cof_F_sign[k][0]==t:
            if Cof_F_sign[k][1] < 0:
                return sum((p[j] * agg_weakenvl.X[j]) + (s[j] * agg_weakenvl.y[j]) + (h[j] * agg_weakenvl.I[j]) for j in agg_weakenvl.T_s if j <= t) >= -agg_weakenvl.I[t] * Cof_i_t[k] - C_v[k]
            else:
                return Constraint.Skip
        return Constraint.Skip
    agg_weakenvl.G3 = Constraint(agg_weakenvl.T_s, agg_weakenvl.convex_L, rule=g3_rule)
     
    
    # F_t(i(t)) >= m(t,q)I(t)+b(t,q)
    def g4_rule(agg_weakenvl,t):
        return sum((p[j] * agg_weakenvl.X[j]) + (s[j] * agg_weakenvl.y[j]) + (h[j] * agg_weakenvl.I[j]) for j in agg_weakenvl.T_s if j < t) + p[t] * agg_weakenvl.X[t] + s[t] * agg_weakenvl.y[t] >= F_L_t[t] - h[t] * agg_weakenvl.I[t]
    
    agg_weakenvl.G4 = Constraint(agg_weakenvl.T_s, rule=g4_rule)
    

    return agg_weakenvl
