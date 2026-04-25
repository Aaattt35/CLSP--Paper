def solve_model(instance_path):
    import pulp

    # read instance file
    data = {}
    with open(instance_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"): 
                continue
            key, value = [x.strip() for x in line.split("=", 1)]
            if "," in value:
                data[key] = [float(v.strip()) for v in value.split(",")]
            else:
                data[key] = float(value)
            print(f"Reading line: {key} = {value}")

    T = int(data["T"])
    a_t = data["a_t"]
    c_t = data["c_t"]
    cap = data["cap"]

    model = pulp.LpProblem("CLSP_Model", pulp.LpMaximize)
    x = [pulp.LpVariable(f"x{t+1}", lowBound=0) for t in range(T)]

    model += pulp.lpSum(c_t[t] * x[t] for t in range(T))
    model += pulp.lpSum(a_t[t] * x[t] for t in range(T)) <= cap

    model.solve(pulp.PULP_CBC_CMD(msg=0))
    status = pulp.LpStatus[model.status]
    values = [x[t].value() for t in range(T)]
    Z = pulp.value(model.objective)

    return status, Z, values
