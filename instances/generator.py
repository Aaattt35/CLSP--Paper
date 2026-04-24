"""
Instance generator for the Single-Item CLSP test problems.

This script generates the benchmark instances used in the paper.
Parameters follow the experimental design described in the manuscript.
"""

import random


def generate_instance(T=12):
    demand = [random.randint(10, 100) for _ in range(T)]
    setup_cost = random.randint(100, 500)
    holding_cost = random.uniform(0.5, 5)

    return demand, setup_cost, holding_cost


if __name__ == "__main__":
    d, s, h = generate_instance()
    print("Demand:", d)
    print("Setup cost:", s)
    print("Holding cost:", h)
