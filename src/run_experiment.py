"""
Run optimization experiment for a given instance.
Connects to the CLSP optimization model.
"""

import sys
import os
from Read_input_txt_file import Read_input  # new: import the solver function

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

    # ---- Run reading form input ----
    Parameters = Read_input(instance_path)

    # To get the planning horizon 'T':
    T = Parameters.get("T")
    d = Parameters.get("d")
    p = Parameters.get("p")
    cap = Parameters.get("cap")
    s = Parameters.get("s")
    h = Parameters.get("h")
    a = Parameters.get("a")
    a_ratio = Parameters.get("a_ratio")
    if demand_data:
        print("Demand data:", d)
        # If you need demand for a specific time period, e.g., period '2':
        demand_period_2 = d.get("2")
        if demand_period_2 is not None:
            print("Demand for period 2:", demand_period_2)
    else:
        print("Demand data ('d') not found in parameters.")
    
    # To get the production cost dictionary 'p':
    p = Parameters.get("p")
    if production_cost_data:
        print("Production cost data:", p)
        # If you need production cost for a specific time period, e.g., period '1':
        production_cost_period_1 = p.get("1")
        if production_cost_period_1 is not None:
            print("Production cost for period 1:", production_cost_period_1)
    else:
        print("Production cost data ('p') not found in parameters.")
