from __future__ import annotations

from bank.amount import Amount
from bank.transaction import Transaction
from bank.transaction_log import TransactionLog
from bank.transaction_type import TransactionType


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
        from bank.account import Account
        return Account(TransactionLog(list(self._log)))
