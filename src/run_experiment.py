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

    # ---- Run the optimization model ----
    status, objective, x_values = Read_input(instance_path)

    # ---- Print results ----
    print("\n=== Optimization Results ===")
    print("Status:", status)
    for i, val in enumerate(x_values, start=1):
        print(f"x{i} = {val:.4f}")
    print("Objective value (Z):", objective)
