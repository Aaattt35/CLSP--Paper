import ast
import json
import pulp


def solve_model(file_path):
    """
    Solve the Capacitated Lot Sizing Problem (CLSP)

    Supports two input formats:
      1. Simple text format (key = value)
      2. Python/JSON array or dictionary with keys (d, p, cap, s, h, T, etc.)
    """

    # -----------------------------------------------------------------------------
    # STEP 1: READ AND PARSE INPUT FILE
    # -----------------------------------------------------------------------------
    data = None

    with open(file_path, "r") as f:
        content = f.read().strip()

    # Try to parse as JSON or Python literal structure
    try:
        data = json.loads(content)
    except Exception:
        try:
            data = ast.literal_eval(content)
        except Exception:
            data = None

    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
        # Case: an array of instances [{'ins': 1, ...}, ...]
        instance = data[0]
        print("🧩 Parsed structured instance data successfully.")
    elif isinstance(data, dict):
        # Case: direct dict
        instance = data
        print("🧩 Parsed single dictionary instance successfully.")
    else:
        # Fall back to simple line-based parsing
        print("⚙️ Falling back to line-based parsing...")
        instance = {}
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=")
            key = key.strip()
            value = value.strip().replace("[", "").replace("]", "")
            if "," in value:
                instance[key] = [float(v.strip()) for v in value.split(",") if v.strip()]
            else:
                try:
                    instance[key] = float(value)
                except ValueError:
                    pass

    # -----------------------------------------------------------------------------
    # STEP 2: EXTRACT PARAMETERS
    # -----------------------------------------------------------------------------
    # Obtain total periods T
    T = int(instance.get("T", len(instance.get("d", []))))

    # Handle fields depending on available naming
    # Normalized keys (these cover both your structure and classical CLSP)
    demand_dict = instance.get("d", instance.get("demand", {}))
    production_dict = instance.get("p", instance.get("production_cost", {}))
    setup_dict = instance.get("s", instance.get("setup_cost", {}))
    hold_dict = instance.get("h", instance.get("holding_cost", {}))
    capacity_dict = instance.get("cap", instance.get("capacity", {}))

    initial_inventory = instance.get("i_n", instance.get("initial_inventory", 0))

    # Convert dictionary values to ordered lists sorted by period
    if isinstance(demand_dict, dict):
        demand = [demand_dict[i] for i in sorted(demand_dict.keys())]
    else:
        demand = list(demand_dict)

    if isinstance(production_dict, dict):
        production_cost = [production_dict[i] for i in sorted(production_dict.keys())]
    else:
        production_cost = list(production_dict)

    if isinstance(setup_dict, dict):
        setup_cost = [setup_dict[i] for i in sorted(setup_dict.keys())]
    else:
        setup_cost = list(setup_dict) or [0] * T

    if isinstance(hold_dict, dict):
        holding_cost = [hold_dict[i] for i in sorted(hold_dict.keys())]
    else:
        holding_cost = list(hold_dict) or [0] * T

    if isinstance(capacity_dict, dict):
        capacity = [capacity_dict[i] for i in sorted(capacity_dict.keys())]
    else:
        capacity = list(capacity_dict)

    # Sanity print
    print(f"Read instance: T={T}, init_inv={initial_inventory}")
    print(f"- demand: first={demand[:3]} ...")
    print(f"- production cost: first={production_cost[:3]} ...")
    print(f"- capacity: first={capacity[:3]} ...")

    # -----------------------------------------------------------------------------
    # STEP 3: BUILD OPTIMIZATION MODEL
    # -----------------------------------------------------------------------------
    model = pulp.LpProblem("CLSP", pulp.LpMinimize)

    x = pulp.LpVariable.dicts("x", range(1, T + 1), lowBound=0)
    y = pulp.LpVariable.dicts("y", range(1, T + 1), cat=pulp.LpBinary)
    I = pulp.LpVariable.dicts("I", range(1, T + 1), lowBound=0)

    model += (
        pulp.lpSum(setup_cost[t - 1] * y[t] for t in range(1, T + 1))
        + pulp.lpSum(production_cost[t - 1] * x[t] for t in range(1, T + 1))
        + pulp.lpSum(holding_cost[t - 1] * I[t] for t in range(1, T + 1))
    )

    # Inventory balance
    for t in range(1, T + 1):
        if t == 1:
            model += I[t] == initial_inventory + x[t] - demand[t - 1]
        else:
            model += I[t] == I[t - 1] + x[t] - demand[t - 1]
        model += x[t] <= capacity[t - 1] * y[t]

    # -----------------------------------------------------------------------------
    # STEP 4: SOLVE
    # -----------------------------------------------------------------------------
    model.solve(pulp.PULP_CBC_CMD(msg=False))

    status = pulp.LpStatus[model.status]
    objective = pulp.value(model.objective)
    x_values = [pulp.value(x[t]) for t in range(1, T + 1)]

    print(f"\n✅ Status: {status}")
    print(f"🎯 Objective: {objective}")
    print(f"📊 Production plan sample: {x_values[:10]}")

    return status, objective, x_values
