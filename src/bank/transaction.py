from __future__ import annotations

from datetime import datetime
from typing import Optional

from bank.amount import Amount
from bank.transaction_type import TransactionType


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
