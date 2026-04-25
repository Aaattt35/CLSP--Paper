import ast
import json
import os


def solve_model(file_path):
    """
    Load instance file, extract relevant CLSP parameters,
    print them, and save them into output/extracted_params.json
    """

    # ---------------------------------------------------------
    # STEP 1 — Read raw content
    # ---------------------------------------------------------
    with open(file_path, "r") as f:
        content = f.read().strip()

    # ---------------------------------------------------------
    # STEP 2 — Try to parse as JSON / Python literal
    # ---------------------------------------------------------
    data = None
    try:
        data = json.loads(content)
    except Exception:
        try:
            data = ast.literal_eval(content)
        except Exception:
            data = None

    # ---------------------------------------------------------
    # STEP 3 — Normalize to a single instance dictionary
    # ---------------------------------------------------------
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
        instance = data[0]    # e.g., [{...}]
    elif isinstance(data, dict):
        instance = data       # e.g., {...}
    else:
        raise ValueError("Could not parse instance file into a usable format.")

    # ---------------------------------------------------------
    # STEP 4 — Extract parameters with flexible naming
    # ---------------------------------------------------------
    T = int(instance.get("T", 0))
    initial_inventory = instance.get("i_n", instance.get("initial_inventory", 0))

    demand_dict = instance.get("d", instance.get("demand", {}))
    production_dict = instance.get("p", instance.get("production_cost", {}))
    setup_dict = instance.get("s", instance.get("setup_cost", {}))
    hold_dict = instance.get("h", instance.get("holding_cost", {}))
    capacity_dict = instance.get("cap", instance.get("capacity", {}))

    # Convert dictionary → ordered list by sorting keys numerically
    def to_list(d):
        if isinstance(d, dict):
            return [d[k] for k in sorted(d.keys(), key=lambda x: int(x))]
        return list(d)

    demand = to_list(demand_dict)
    production_cost = to_list(production_dict)
    setup_cost = to_list(setup_dict)
    holding_cost = to_list(hold_dict)
    capacity = to_list(capacity_dict)

    # ---------------------------------------------------------
    # STEP 5 — Prepare output structure
    # ---------------------------------------------------------
    extracted = {
        "T": T,
        "initial_inventory": initial_inventory,
        "demand": demand,
        "production_cost": production_cost,
        "setup_cost": setup_cost,
        "holding_cost": holding_cost,
        "capacity": capacity,
    }

    # ---------------------------------------------------------
    # STEP 6 — Print extracted values
    # ---------------------------------------------------------
    print("\n===== Extracted Parameters =====")
    print(json.dumps(extracted, indent=4))
    print("================================\n")

    # ---------------------------------------------------------
    # STEP 7 — Save to output file
    # ---------------------------------------------------------
    os.makedirs("output", exist_ok=True)
    with open("output/extracted_params.json", "w") as f:
        json.dump(extracted, f, indent=4)

    print("Saved extracted parameters to: output/extracted_params.json")

    # Return them (no optimization)
    return extracted
