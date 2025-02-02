def safe_divide(x: float, y: float) -> float | None:
    try:
        return x / y
    except ZeroDivisionError:
        return None