import math_helper


def test_math_helper_check_float() -> None:
    assert math_helper.check_float("1", "2") == True
    assert math_helper.check_float("1.0", "2.78") == True
    assert math_helper.check_float("1.0", "-2.78", "3") == True
    assert math_helper.check_float("1.0", "2.78", "3j") == False


def test_math_helper_check_float_positive() -> None:
    assert math_helper.check_float_positive("1", "2") == True
    assert math_helper.check_float_positive("1.0", "2.78") == True
    assert math_helper.check_float_positive("-1.0", "2.78") == False
