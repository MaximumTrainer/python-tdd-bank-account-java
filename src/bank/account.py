from __future__ import annotations

from datetime import datetime
from typing import Optional

from bank.amount import Amount
from bank.transaction import Transaction
from bank.transaction_log import TransactionLog
from bank.transaction_type import TransactionType


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
