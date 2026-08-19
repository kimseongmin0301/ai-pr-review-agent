"""Contract tests for app.calculator.

These tests describe the *observable behaviour* of the public functions:
the values they return and the errors they raise. They deliberately avoid
asserting on implementation details, so a legitimate refactor stays green
while a behavioural regression turns red.

Every test is independent: no shared state, no ordering requirement.
"""

import pytest

from app.calculator import add, calculate_discount, divide, subtract


def test_add_returns_sum():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_subtract_returns_difference():
    assert subtract(5, 3) == 2
    assert subtract(3, 5) == -2
    assert subtract(0, 0) == 0


def test_divide_returns_quotient():
    assert divide(10, 2) == 5
    assert divide(7, 2) == 3.5
    assert divide(-9, 3) == -3


def test_divide_by_zero_raises_value_error():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(1, 0)


def test_calculate_discount_applies_percentage():
    assert calculate_discount(100, 20) == 80
    assert calculate_discount(250, 10) == 225


def test_calculate_discount_rejects_negative_price():
    with pytest.raises(ValueError, match="Price must be non-negative"):
        calculate_discount(-1, 10)


def test_calculate_discount_rejects_percent_above_100():
    with pytest.raises(ValueError, match="Discount percent must be between 0 and 100"):
        calculate_discount(100, 101)


def test_calculate_discount_rejects_negative_percent():
    with pytest.raises(ValueError, match="Discount percent must be between 0 and 100"):
        calculate_discount(100, -1)


def test_calculate_discount_with_zero_percent_returns_original_price():
    assert calculate_discount(100, 0) == 100


def test_calculate_discount_with_hundred_percent_returns_zero():
    assert calculate_discount(100, 100) == 0
