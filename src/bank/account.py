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
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._transactions.append(Transaction(amount, TransactionType.DEPOSIT))

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance():
            raise ValueError(
                f"Insufficient funds: balance is {self.balance()}, "
                f"attempted to withdraw {amount}."
            )
        self._transactions.append(Transaction(amount, TransactionType.WITHDRAWAL))

    def transfer(self, amount: float, target: Account) -> None:
        raise NotImplementedError

    def balance(self) -> float:
        total = 0.0
        for t in self._transactions:
            if t.transaction_type == TransactionType.DEPOSIT:
                total += t.amount
            else:
                total -= t.amount
        return total

    def balance_slip(self) -> str:
        raise NotImplementedError

    def statement(
        self, filter_type: Optional[TransactionType] = None
    ) -> str:
        raise NotImplementedError
