from __future__ import annotations

from typing import Iterator, List, Optional

from bank.amount import Amount
from bank.transaction import Transaction
from bank.transaction_type import TransactionType


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
