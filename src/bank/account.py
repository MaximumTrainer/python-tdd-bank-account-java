from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Iterator, List, Optional


class TransactionType(Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"


class Amount:
    """Immutable value object representing a positive monetary amount.

    Owns positivity validation and arithmetic so that no raw floats
    leak into the rest of the domain.
    """

    def __init__(self, value: float) -> None:
        if value <= 0:
            raise ValueError(f"Amount must be positive, got {value}.")
        self._value = float(value)

    # ------------------------------------------------------------------
    # Arithmetic — return new Amount instances (immutable)
    # ------------------------------------------------------------------

    def __add__(self, other: Amount) -> Amount:
        return Amount._of(self._value + other._value)

    def __sub__(self, other: Amount) -> Amount:
        return Amount._of(self._value - other._value)

    # ------------------------------------------------------------------
    # Comparison
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        return f"{self._value:.2f}"

    def __repr__(self) -> str:
        return f"Amount({self._value!r})"

    # ------------------------------------------------------------------
    # Internal factory — bypasses positivity guard for computed values
    # ------------------------------------------------------------------

    @classmethod
    def _of(cls, raw: float) -> Amount:
        obj = cls.__new__(cls)
        obj._value = raw
        return obj

    @classmethod
    def zero(cls) -> Amount:
        return cls._of(0.0)


class Transaction:
    """A single immutable ledger entry."""

    def __init__(
        self,
        amount: Amount,
        transaction_type: TransactionType,
        date: Optional[datetime] = None,
    ) -> None:
        self.amount = amount
        self.transaction_type = transaction_type
        self.date: datetime = date or datetime.now()

    def __str__(self) -> str:
        return (
            f"{self.date.strftime('%Y-%m-%d %H:%M:%S')} | "
            f"{self.transaction_type.value:10} | "
            f"{self.amount!s:>10}"
        )


class TransactionLog:
    """First-class collection of Transaction objects.

    Owns balance computation and filtered views so that Account
    stays free of iteration logic.
    """

    def __init__(self, transactions: Optional[List[Transaction]] = None) -> None:
        self._items: List[Transaction] = list(transactions or [])

    def record(self, transaction: Transaction) -> None:
        self._items.append(transaction)

    def filtered(self, transaction_type: Optional[TransactionType] = None) -> TransactionLog:
        if transaction_type is None:
            return TransactionLog(list(self._items))
        return TransactionLog(
            [t for t in self._items if t.transaction_type == transaction_type]
        )

    def balance(self) -> Amount:
        total = Amount.zero()
        for t in self._items:
            if t.transaction_type == TransactionType.DEPOSIT:
                total = total + t.amount
            else:
                total = total - t.amount
        return total

    def __iter__(self) -> Iterator[Transaction]:
        return iter(self._items)


class Account:
    """A bank account that records deposits, withdrawals, and transfers."""

    def __init__(self, log: Optional[TransactionLog] = None) -> None:
        self._log = log or TransactionLog()

    def deposit(self, amount: float) -> None:
        self._log.record(Transaction(Amount(amount), TransactionType.DEPOSIT))

    def withdraw(self, amount: float) -> None:
        withdrawal = Amount(amount)
        if withdrawal > self._log.balance():
            raise ValueError(
                f"Insufficient funds: balance is {self._log.balance()}, "
                f"attempted to withdraw {withdrawal}."
            )
        self._log.record(Transaction(withdrawal, TransactionType.WITHDRAWAL))

    def transfer(self, amount: float, target: Account) -> None:
        self.withdraw(amount)
        target.deposit(amount)

    def balance(self) -> Amount:
        return self._log.balance()

    def balance_slip(self) -> str:
        now = datetime.now()
        return (
            f"Date: {now.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Balance: {self.balance()}"
        )

    def statement(self, filter_type: Optional[TransactionType] = None) -> str:
        header = f"{'Date/Time':<20} | {'Type':<10} | {'Amount':>10}"
        separator = "-" * len(header)
        lines = [header, separator]
        for t in self._log.filtered(filter_type):
            lines.append(str(t))
        lines.append(separator)
        lines.append(f"{'Balance':>34}: {str(self.balance()):>10}")
        return "\n".join(lines)


class AccountBuilder:
    """Fluent builder for constructing Account instances with preset transactions.

    Useful for setting up test scenarios or seeding accounts without
    going through the public deposit/withdraw API.

    Example::

        account = (
            AccountBuilder()
            .with_deposit(500)
            .with_withdrawal(100)
            .build()
        )
    """

    def __init__(self) -> None:
        self._log = TransactionLog()

    def with_deposit(self, amount: float) -> AccountBuilder:
        self._log.record(Transaction(Amount(amount), TransactionType.DEPOSIT))
        return self

    def with_withdrawal(self, amount: float) -> AccountBuilder:
        self._log.record(Transaction(Amount(amount), TransactionType.WITHDRAWAL))
        return self

    def build(self) -> Account:
        return Account(self._log)
