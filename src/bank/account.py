from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional


class TransactionType(Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"


class Transaction:
    def __init__(
        self,
        amount: float,
        transaction_type: TransactionType,
        date: Optional[datetime] = None,
    ) -> None:
        self.amount = amount
        self.transaction_type = transaction_type
        self.date: datetime = date or datetime.now()


class Account:
    def __init__(self) -> None:
        self._transactions: List[Transaction] = []

    def deposit(self, amount: float) -> None:
        raise NotImplementedError

    def withdraw(self, amount: float) -> None:
        raise NotImplementedError

    def transfer(self, amount: float, target: Account) -> None:
        raise NotImplementedError

    def balance(self) -> float:
        raise NotImplementedError

    def balance_slip(self) -> str:
        raise NotImplementedError

    def statement(
        self, filter_type: Optional[TransactionType] = None
    ) -> str:
        raise NotImplementedError
