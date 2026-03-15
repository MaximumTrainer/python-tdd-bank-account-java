"""Unit tests for the Amount value object."""

import pytest

from bank.amount import Amount


class TestAmountValidation:
    def test_raises_on_zero(self) -> None:
        with pytest.raises(ValueError):
            Amount(0)

    def test_raises_on_negative(self) -> None:
        with pytest.raises(ValueError):
            Amount(-10)

    def test_positive_value_is_accepted(self) -> None:
        assert Amount(1)


class TestAmountArithmetic:
    def test_add_two_amounts(self) -> None:
        assert Amount(100) + Amount(50) == 150

    def test_subtract_two_amounts(self) -> None:
        result = Amount(100) - Amount(30)
        assert result == 70

    def test_zero_factory(self) -> None:
        assert Amount.zero() == 0


class TestAmountComparison:
    def test_greater_than(self) -> None:
        assert Amount(100) > Amount(50)

    def test_not_greater_than_equal(self) -> None:
        assert not Amount(50) > Amount(100)

    def test_equality_with_float(self) -> None:
        assert Amount(100) == 100.0

    def test_equality_with_amount(self) -> None:
        assert Amount(100) == Amount(100)

    def test_inequality_with_different_amount(self) -> None:
        assert Amount(100) != Amount(99)


class TestAmountDisplay:
    def test_str_formats_two_decimal_places(self) -> None:
        assert str(Amount(100)) == "100.00"

    def test_repr_includes_value(self) -> None:
        assert "100" in repr(Amount(100))
