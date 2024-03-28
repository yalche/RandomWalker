def check_float(*args: str) -> bool:
    """
    This function checks if the strings arguments are floats.
    """
    for num in args:
        if not num.lstrip("-").replace(".", "").isdigit():
            return False
    return True


def check_float_positive(*args: str) -> bool:
    """
    This function checks if the strings arguments are positive floats.
    """
    for num in args:
        if not num.replace(".", "").isdigit() or float(num) < 0:
            return False
    return True