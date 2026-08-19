"""Baseline calculator module.

This module is intentionally small and free of side effects.
It is the "subject under review" for the AI PR Review Agent experiments:
future benchmark Pull Requests will modify these functions on purpose
(correct changes, buggy changes, regressions, oversized refactors)
so that the reviewer can be evaluated against a known expected outcome.
"""


class Calculator:
    """Namespace holding the arithmetic operations exposed by this module.

    Every operation is a ``@staticmethod`` so the class carries no state and
    can be used without instantiation. The module-level functions below stay
    as the public entry points and simply delegate here.
    """

    @staticmethod
    def add(a, b):
        """Return the sum of ``a`` and ``b``."""
        return a + b

    @staticmethod
    def subtract(a, b):
        """Return ``a`` minus ``b``."""
        return a - b

    @staticmethod
    def multiply(a, b):
        """Return the product of ``a`` and ``b``."""
        return a * b

    @staticmethod
    def divide(a, b):
        """Return ``a`` divided by ``b``.

        Raises:
            ValueError: If ``b`` is zero.
        """
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    @staticmethod
    def calculate_discount(price, discount_percent):
        """Return ``price`` after applying ``discount_percent`` percent off.

        Example:
            calculate_discount(100, 20) -> 80.0

        Raises:
            ValueError: If ``price`` is negative.
            ValueError: If ``discount_percent`` is outside the 0..100 range.
        """
        if price < 0:
            raise ValueError("Price must be non-negative")
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Discount percent must be between 0 and 100")
        return price * (100 - discount_percent) / 100


def add(a, b):
    """Return the sum of ``a`` and ``b``."""
    return Calculator.add(a, b)


def subtract(a, b):
    """Return ``a`` minus ``b``."""
    return Calculator.subtract(a, b)


def multiply(a, b):
    """Return the product of ``a`` and ``b``."""
    return Calculator.multiply(a, b)


def divide(a, b):
    """Return ``a`` divided by ``b``.

    Raises:
        ValueError: If ``b`` is zero.
    """
    return Calculator.divide(a, b)


def calculate_discount(price, discount_percent):
    """Return ``price`` after applying ``discount_percent`` percent off.

    Example:
        calculate_discount(100, 20) -> 80.0

    Raises:
        ValueError: If ``price`` is negative.
        ValueError: If ``discount_percent`` is outside the 0..100 range.
    """
    return Calculator.calculate_discount(price, discount_percent)
