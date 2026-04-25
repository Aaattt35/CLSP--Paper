# CLSP--Paper/src/model.py
# ----------------------------------------------------------
# Linear Programming Model
# Maximize: Z = sum(c_t * x_t)
# Subject to: sum(a_t * x_t) <= cap
# x_t >= 0
# ----------------------------------------------------------

import pulp
import os

# ---- Step 1: Read input data ----
input_path = r"C:\path\to\your\CLSP--Paper\instances\test_instance.txt"
data = {}

with open(input_path, "r") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, value = [x.strip() for x in line.split("=", 1)]
        if "," in value:
            data[key] = [float(v.strip()) for v in value.split(",")]
        else:
            data[key] = float(value)

# Extract parameters
T = int(data["T"])
a_t = data["a_t"]
c_t = data["c_t"]
cap = data["cap"]

# ---- Step 2: Define LP model ----
model = pulp.LpProblem("CLSP_Model", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x{t+1}", lowBound=0) for t in range(T)]

# Objective function
model += pulp.lpSum(c_t[t] * x[t] for t in range(T)), "Total_Profit"

# Single capacity constraint
model += pulp.lpSum(a_t[t] * x[t] for t in range(T)) <= cap, "Capacity"

# ---- Step 3: Solve ----
model.solve(pulp.PULP_CBC_CMD(msg=0))

# ---- Step 4: Prepare output ----
status = pulp.LpStatus[model.status]
values = [x[t].value() for t in range(T)]
Z = pulp.value(model.objective)

# ---- Step 5: Print to console ----
print("Status:", status)
for t in range(T):
    print(f"x{t+1} = {values[t]:.4f}")
print("Z =", Z)

# ---- Step 6: Save to file ----
output_path = os.path.join("..", "instances", "test_output.txt")
with open(output_path, "w") as out:
    out.write(f"Status: {status}\n")
    for t in range(T):
        out.write(f"x{t+1} = {values[t]:.4f}\n")
    out.write(f"Z = {Z:.4f}\n")

print(f"\n✅ نتایج علاوه بر چاپ در کنسول، در این فایل نیز ذخیره شد:")
print(output_path)
