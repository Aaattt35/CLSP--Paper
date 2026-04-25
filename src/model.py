import ast
import json
import os


def _parse_instance_file(content: str):
    """
    Robust parser for instance files that may contain:
      - JSON
      - Python literals (list/dict)
      - numpy-style dumps: array([...], dtype=object)
    Returns the parsed Python object (list/dict).
    """
    content = content.strip()

    # 1) Try JSON
    try:
        return json.loads(content)
    except Exception:
        pass

    # 2) Try direct Python literal
    try:
        return ast.literal_eval(content)
    except Exception:
        pass

    # 3) Try numpy array-like: array([...], dtype=object)
    cleaned = content

    # Remove leading "array(" if exists
    if cleaned.startswith("array("):
        cleaned = cleaned[len("array("):]

    # Remove possible trailing ")"
    cleaned = cleaned.rstrip()

    # Remove trailing ", dtype=object)" if exists
    if cleaned.endswith(")"):
        # e.g. " [...], dtype=object)"
        # first remove last ')'
        cleaned = cleaned[:-1].rstrip()

    if cleaned.endswith(", dtype=object"):
        cleaned = cleaned[: -len(", dtype=object")].rstrip()

    # الآن باید چیزی مثل "[{...}]" باشد
    try:
        return ast.literal_eval(cleaned)
    except Exception as e:
        raise ValueError(
            f"Could not parse instance file into a usable format. Last error: {e}"
        )


def solve_model(file_path):
    """
    Load instance file (numpy-array-like or dict/list format),
    extract relevant CLSP parameters, print them, save them,
    and return a placeholder optimization result together
    with extracted parameters (برای این مرحله، مدل حل نمی‌شود).
    """

    # ---------------------------------------------------------
    # STEP 1 — Read raw content
    # ---------------------------------------------------------
    with open(file_path, "r") as f:
        content = f.read()

    # ---------------------------------------------------------
    # STEP 2 — Parse content (robust)
    # ---------------------------------------------------------
    data = _parse_instance_file(content)

    # ---------------------------------------------------------
    # STEP 3 — Normalize to a single instance dictionary
    # ---------------------------------------------------------
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
        # numpy array dump → after cleaning تبدیل به list[dict] شده
        instance = data[0]
    elif isinstance(data, dict):
        instance = data
    else:
        raise ValueError("Parsed data is neither a dict nor a list of dicts.")

    # ---------------------------------------------------------
    # STEP 4 — Extract parameters (using your keys)
    # ---------------------------------------------------------
    # T
    T = int(instance.get("T", 0))

    # initial inventory
    initial_inventory = instance.get("i_n", instance.get("initial_inventory", 0))

    # دیکشنری‌های پارامترها
    demand_dict = instance.get("d", instance.get("demand", {}))
    production_dict = instance.get("p", instance.get("production_cost", {}))
    setup_dict = instance.get("s", instance.get("setup_cost", {}))
    hold_dict = instance.get("h", instance.get("holding_cost", {}))
    capacity_dict = instance.get("cap", instance.get("capacity", {}))

    # تبدیل dict به لیست، با مرتب‌سازی کلیدها 1..T
    def dict_to_ordered_list(d):
        if isinstance(d, dict):
            # کلیدها مثل 1, 2, 3 هستند → به ترتیب عددی
            return [d[k] for k in sorted(d.keys(), key=lambda x: int(x))]
        # اگر خود لیست بود
        return list(d)

    demand = dict_to_ordered_list(demand_dict)
    production_cost = dict_to_ordered_list(production_dict)
    setup_cost = dict_to_ordered_list(setup_dict)
    holding_cost = dict_to_ordered_list(hold_dict)
    capacity = dict_to_ordered_list(capacity_dict)

    # ---------------------------------------------------------
    # STEP 5 — Prepare extracted parameter structure
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
    out_path = os.path.join("output", "extracted_params.json")
    with open(out_path, "w") as f:
        json.dump(extracted, f, indent=4)

    print(f"Saved extracted parameters to: {out_path}")

    # ---------------------------------------------------------
    # STEP 8 — Return something compatible with run_experiment.py
    # (موقتا مدل حل نمی‌کنیم؛ status/objective/x_values را dummy برمی‌گردانیم)
    # اگر می‌خواهی همین‌جا مدل را هم حل کنیم، بگو تا نسخه‌ی کامل ساده را اضافه کنم.
    # ---------------------------------------------------------
    status = "EXTRACTION_ONLY"
    objective = None
    x_values = {}

    return status, objective, x_values
