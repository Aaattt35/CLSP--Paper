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
    planning_horizon = Parameters.get("T")
    if planning_horizon is not None:
        print("Planning Horizon (T):", planning_horizon)
    else:
        print("Planning horizon ('T') not found in parameters.")
   
    # To get the demand dictionary 'd':
    demand_data = Parameters.get("d")
    if demand_data:
        print("Demand data:", demand_data)
        # If you need demand for a specific time period, e.g., period '2':
        demand_period_2 = demand_data.get("2")
        if demand_period_2 is not None:
            print("Demand for period 2:", demand_period_2)
    else:
        print("Demand data ('d') not found in parameters.")
    
    # To get the production cost dictionary 'p':
    production_cost_data = Parameters.get("p")
    if production_cost_data:
        print("Production cost data:", production_cost_data)
        # If you need production cost for a specific time period, e.g., period '1':
        production_cost_period_1 = production_cost_data.get("1")
        if production_cost_period_1 is not None:
            print("Production cost for period 1:", production_cost_period_1)
    else:
        print("Production cost data ('p') not found in parameters.")
