import pulp


def solve_model(file_path):
    """
    Solve the Capacitated Lot Sizing Problem (CLSP)
    Instance format (example):
        T = 4
        demand = 20, 35, 40, 30
        setup_cost = 50, 50, 50, 50
        holding_cost = 1, 1, 1, 1
        production_cost = 2, 2, 2, 2
        capacity = 60, 60, 60, 60
        initial_inventory = 10
    """

    # ---------------------------------------------
    # مرحله 1: خواندن فایل ورودی و ساخت دیکشنری داده‌ها
    # ---------------------------------------------
    data = {}

    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()

            # رد کردن خطوط خالی یا نظرها
            if not line or line.startswith("#"):
                continue

            # تقسیم خط به کلید و مقدار
            if "=" not in line:
                print(f"⚠️ خط نامعتبر در فایل ورودی: {line}")
                continue

            key, value = line.split("=")
            key = key.strip()
            value = value.strip()

            # چاپ اطلاعات خوانده‌شده (برای دیباگ)
            print(f"Reading line: {key} = {value}")

            # حذف براکت‌ها و فاصله‌های اضافی
            value = value.replace("[", "").replace("]", "")

            # تعیین نوع مقدار (لیست یا عدد)
            if "," in value:
                data[key] = [float(v.strip()) for v in value.split(",") if v.strip()]
            else:
                try:
                    data[key] = float(value)
                except ValueError:
                    print(f"⚠️ مقدار نامعتبر برای {key}: {value}")

    # ---------------------------------------------
    # مرحله 2: استخراج پارامترها از داده‌ها
    # ---------------------------------------------
    T = int(data.get("T", len(data.get("demand", []))))
    demand = data["demand"]
    setup_cost = data["setup_cost"]
    holding_cost = data["holding_cost"]
    production_cost = data["production_cost"]
    capacity = data["capacity"]
    initial_inventory = data.get("initial_inventory", 0.0)

    # ---------------------------------------------
    # مرحله 3: ساخت مدل بهینه‌سازی
    # ---------------------------------------------
    model = pulp.LpProblem("CLSP", pulp.LpMinimize)

    # متغیرها
    x = pulp.LpVariable.dicts("x", range(1, T + 1), lowBound=0)
    y = pulp.LpVariable.dicts("y", range(1, T + 1), cat=pulp.LpBinary)
    I = pulp.LpVariable.dicts("I", range(1, T + 1), lowBound=0)

    # تابع هدف
    model += (
        pulp.lpSum(setup_cost[t - 1] * y[t] for t in range(1, T + 1))
        + pulp.lpSum(production_cost[t - 1] * x[t] for t in range(1, T + 1))
        + pulp.lpSum(holding_cost[t - 1] * I[t] for t in range(1, T + 1))
    )

    # محدودیت‌ها
    # معادله موجودی
    for t in range(1, T + 1):
        if t == 1:
            model += I[t] == initial_inventory + x[t] - demand[t - 1]
        else:
            model += I[t] == I[t - 1] + x[t] - demand[t - 1]

    # محدودیت ظرفیت تولید
    for t in range(1, T + 1):
        model += x[t] <= capacity[t - 1] * y[t]

    # ---------------------------------------------
    # مرحله 4: حل مدل
    # ---------------------------------------------
    model.solve(pulp.PULP_CBC_CMD(msg=False))

    status = pulp.LpStatus[model.status]
    objective = pulp.value(model.objective)
    x_values = [pulp.value(x[t]) for t in range(1, T + 1)]

    print(f"\n✅ وضعیت مدل: {status}")
    print(f"🎯 مقدار هدف بهینه: {objective}")
    print(f"📦 مقادیر تولید در هر دوره: {x_values}")

    return status, objective, x_values
