from typing import Any, Dict, List, Optional, Union
import os
import json
import ast


def _parse_instance_file(content: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Robust parser for instance files that may contain JSON, Python literals,
    or numpy-style dumps. Returns either a dict or a list of dicts.
    """
    content = content.strip()

    # 1) Try JSON
    try:
        return json.loads(content)
    except Exception:
        pass

    # 2) Try Python literal (dict/list)
    try:
        return ast.literal_eval(content)
    except Exception:
        pass

    # 3) Try numpy-like / partial structure
    first_brace = content.find("{")
    last_brace = content.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        try:
            inner = content[first_brace:last_brace + 1]
            parsed = ast.literal_eval(inner)
            return [parsed]
        except Exception as e:
            raise ValueError(f"Failed to parse dict from numpy-like dump: {e}")

    raise ValueError("Could not parse instance file in any known format.")


def _ensure_output_dir(path: str) -> None:
    """Create output directory if missing."""
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def _normalize_index_key(x: Union[int, str]) -> str:
    """Converts any index into a clean string key for JSON-safe dicts."""
    return str(x)


def _key2(t: Any, j: Any) -> str:
    """Creates a JSON-safe 2D key like 't-j'."""
    return f"{t}-{j}"


def _extract_parameters(instance: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extracts all model parameters from instance and produces a JSON-safe output.
    All keys become strings, including 2D indices.
    """

    T = instance.get("T")
    d = instance.get("d") or instance.get("dem") or instance.get("demand")
    p = instance.get("p") or instance.get("prod_cost")
    cap = instance.get("cap") or instance.get("capacity")
    s = instance.get("s") or instance.get("setup_cost")
    h = instance.get("h") or instance.get("hold_cost")

    if T is None:
        raise ValueError("Missing planning horizon T.")

    # Build time index set
    if isinstance(T, int):
        T_set = list(range(1, T + 1))
    elif isinstance(T, list):
        T_set = T
    else:
        raise ValueError("T must be int or list.")

    # Normalize 1D parameter keys to strings
    def normalize_1d(dct):
        if not isinstance(dct, dict):
            # if list: convert to { "1": value1, ... }
            if isinstance(dct, list):
                return {str(i + 1): dct[i] for i in range(len(dct))}
            raise ValueError("Parameter must be dict or list.")
        return {str(k): v for k, v in dct.items()}

    d = normalize_1d(d)
    p = normalize_1d(p)
    cap = normalize_1d(cap)
    s = normalize_1d(s)
    h = normalize_1d(h)

    # ---- Compute h_{t,j} ----
    h_tj: Dict[str, float] = {}
    for t in T_set:
        for j in T_set:
            if t < j:
                key = _key2(t, j)
                total = 0
                for k in range(t, j):
                    total += h[str(k)]
                h_tj[key] = total

    # ---- Compute a(t,j) and a_ratio(t,j) ----
    a: Dict[str, float] = {}
    a_ratio: Dict[str, Optional[float]] = {}

    for t in T_set:
        for j in T_set:
            if t < j:
                key = _key2(t, j)

                hsum = h_tj[key]
                dj = d[str(j)]
                term = s[str(j)] - (hsum - p[str(j)] + p[str(t)]) * dj
                a[key] = term

                denom = (hsum + p[str(t)]) * dj
                if denom != 0:
                    a_ratio[key] = (s[str(j)] + p[str(j)] * dj) / denom
                else:
                    a_ratio[key] = None

    # Return publication-ready structure
    return {
        "T": T,
        "d": d,
        "p": p,
        "cap": cap,
        "s": s,
        "h": h,
        "a": a,
        "a_ratio": a_ratio,
        "h_tj": h_tj,
    }


def Read_input(file_path: str):
    """
    Reads instance, extracts parameters, dumps a JSON-safe parameter file,
    and returns placeholder (status, objective, x_values).
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Instance not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    parsed = _parse_instance_file(content)

    if isinstance(parsed, list):
        if not parsed:
            raise ValueError("Empty instance list.")
        instance = parsed[0]
    else:
        instance = parsed

    if not isinstance(instance, dict):
        raise ValueError(f"Unexpected instance type after parsing: {type(instance)}")

    params = _extract_parameters(instance)

    return params
