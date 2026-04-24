"""
Run optimization experiment for a given instance.
"""

import sys


def read_instance(path):
    data = {}
    with open(path, "r") as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=")
                data[key.strip()] = value.strip()
    return data


def solve_instance(instance):
    # placeholder for the optimization model
    result = {
        "objective_value": 1234,
        "status": "optimal"
    }
    return result


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python run_experiment.py instance_file")
        sys.exit(1)

    instance_file = sys.argv[1]

    instance = read_instance(instance_file)

    result = solve_instance(instance)

    print("Status:", result["status"])
    print("Objective value:", result["objective_value"])
