from __future__ import annotations


class Amount:
    """Immutable value object representing a positive monetary amount.

    Owns positivity validation and arithmetic so that no raw floats
    leak into the rest of the domain.
    """

    def __init__(self, value: float) -> None:
        if value <= 0:
            raise ValueError(f"Amount must be positive, got {value}.")
        self._value = float(value)

    def __add__(self, other: Amount) -> Amount:
        return Amount._of(self._value + other._value)

    def __sub__(self, other: Amount) -> Amount:
        return Amount._of(self._value - other._value)

    def __gt__(self, other: Amount) -> bool:
        return self._value > other._value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, (int, float)):
            return self._value == float(other)
        if isinstance(other, Amount):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)

    def __str__(self) -> str:
        return f"{self._value:.2f}"

    def __repr__(self) -> str:
        return f"Amount({self._value!r})"

    @classmethod
    def _of(cls, raw: float) -> Amount:
        obj = cls.__new__(cls)
        obj._value = raw
        return obj

    @classmethod
    def zero(cls) -> Amount:
        return cls._of(0.0)
