import os
import json
import ast
from typing import Any, Dict, List, Union


def _parse_instance_file(content: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Robust parser for instance files that may contain:
      - JSON
      - Python literals (list/dict)
      - numpy-style dumps: array([...], dtype=object)
        حتی اگر ناقص باشند و مثلا ] یا ) انتهایی را نداشته باشند.

    خروجی:
      - یک dict (برای یک نمونه)
      - یا لیستی از dictها (برای چند نمونه)
    """
    content = content.strip()

    # 1) ابتدا تلاش به عنوان JSON
    try:
        data = json.loads(content)
        return data
    except Exception:
        pass

    # 2) تلاش به عنوان literal پایتون (لیست / دیکشنری)
    try:
        data = ast.literal_eval(content)
        return data
    except Exception:
        pass

    # 3) فرمت numpy یا ناقص:
    #    فقط دیکشنری بین اولین { و آخرین } را جدا می‌کنیم و همان را eval می‌کنیم.
    first_brace = content.find("{")
    last_brace = content.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        dict_str = content[first_brace : last_brace + 1]
        try:
            instance = ast.literal_eval(dict_str)
            # برای یکدست بودن، آن را در لیست برمی‌گردانیم
            return [instance]
        except Exception as e:
            raise ValueError(
                f"Could not parse instance dictionary from content. Last error: {e}"
            )

    # اگر هیچکدام موفق نشدند، خطا می‌دهیم
    raise ValueError("Could not parse instance file into a usable format.")


def _ensure_output_dir(path: str) -> None:
    """ایجاد دایرکتوری خروجی اگر وجود نداشت."""
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def _extract_parameters(instance: Dict[str, Any]) -> Dict[str, Any]:
    """
    از دیکشنری instance پارامترهای CLSP را استخراج می‌کند.

    انتظار می‌رود instance حداقل شامل موارد زیر باشد
    (نام دقیق کلیدها را با نمونه‌ی real خودت چک کن و اگر فرق داشت اینجا را تنظیم کن):

      - T: تعداد دوره‌ها (int)
      - i_n: موجودی اولیه (int یا float)
      - d: تقاضا (لیست/دیکشنری/آرایه)
      - p: هزینه تولید
      - cap: ظرفیت تولید
      - s: هزینه setup
      - h: هزینه نگهداری

    اگر کلیدها در داده‌ی واقعی‌ات نام دیگری دارند
    (مثلاً 'I0' به‌جای 'i_n' یا 'dem' به‌جای 'd') اینجا نگاشت را اصلاح کن.
    """

    # اینجا با فرض نام‌های مستقیم:
    T = instance.get("T")
    i_n = instance.get("i_n") or instance.get("i0") or instance.get("I0")
    d = instance.get("d") or instance.get("dem") or instance.get("demand")
    p = instance.get("p") or instance.get("prod_cost")
    cap = instance.get("cap") or instance.get("capacity")
    s = instance.get("s") or instance.get("setup_cost")
    h = instance.get("h") or instance.get("hold_cost")

    params = {
        "T": T,
        "i_n": i_n,
        "d": d,
        "p": p,
        "cap": cap,
        "s": s,
        "h": h,
    }

    return params


def solve_model(file_path: str):
    """
    تابع اصلی که توسط run_experiment.py فراخوانی می‌شود.

    مطابق با run_experiment.py باید سه خروجی بدهد:
        status, objective, x_values

    در این نسخه:
      1. فایل instance را می‌خواند.
      2. آن را با _parse_instance_file پارس می‌کند.
      3. پارامترهای CLSP را استخراج می‌کند.
      4. پارامترها را روی کنسول چاپ می‌کند.
      5. پارامترها را در output/extracted_params.json ذخیره می‌کند.
      6. مقادیر placeholder به صورت
         status="ok", objective=None, x_values={}
         برمی‌گرداند تا run_experiment.py بدون خطا اجرا شود.
    """

    # 1) خواندن محتوا
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Instance file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 2) پارس کردن
    data = _parse_instance_file(content)

    # 3) انتخاب instance
    if isinstance(data, list):
        if not data:
            raise ValueError("Parsed instance list is empty.")
        instance = data[0]
        if not isinstance(instance, dict):
            raise ValueError(
                f"Expected a dict as first element of list, got: {type(instance)}"
            )
    elif isinstance(data, dict):
        instance = data
    else:
        raise ValueError(
            f"Parsed data has unexpected type: {type(data)}. Expected dict or list."
        )

    # 4) استخراج پارامترها
    params = _extract_parameters(instance)

    # 5) چاپ روی کنسول (برای دیباگ در GitHub Actions)
    print("=== Extracted CLSP parameters ===")
    for k, v in params.items():
        print(f"{k}: {v}")
    print("================================")

    # 6) ذخیره در فایل JSON
    output_path = os.path.join("output", "extracted_params.json")
    _ensure_output_dir(output_path)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(params, f, indent=2, ensure_ascii=False)

    # 7) خروجی مورد انتظار run_experiment.py
    status = "ok"     # در آینده می‌توانی "feasible"/"infeasible" واقعی را اینجا قرار دهی
    objective = None  # فعلاً مدل حل نمی‌شود
    x_values = {}     # فعلاً هیچ متغیر تصمیمی محاسبه نشده است

    return status, objective, x_values
    return result
