"""Unit tests for the Transaction ledger entry."""

from datetime import datetime

from bank.amount import Amount
from bank.transaction import Transaction
from bank.transaction_type import TransactionType


class TestTransaction:
    def test_stores_amount(self) -> None:
        t = Transaction(Amount(100), TransactionType.DEPOSIT)
        assert t.amount == Amount(100)

    def test_stores_transaction_type(self) -> None:
        t = Transaction(Amount(100), TransactionType.WITHDRAWAL)
        assert t.transaction_type == TransactionType.WITHDRAWAL

    def test_defaults_to_current_datetime(self) -> None:
        before = datetime.now()
        t = Transaction(Amount(50), TransactionType.DEPOSIT)
        after = datetime.now()
        assert before <= t.date <= after

    def test_accepts_explicit_date(self) -> None:
        fixed = datetime(2024, 1, 15, 10, 30, 0)
        t = Transaction(Amount(50), TransactionType.DEPOSIT, date=fixed)
        assert t.date == fixed

    def test_str_contains_type(self) -> None:
        t = Transaction(Amount(50), TransactionType.DEPOSIT)
        assert "DEPOSIT" in str(t)

    def test_str_contains_amount(self) -> None:
        t = Transaction(Amount(50), TransactionType.DEPOSIT)
        assert "50.00" in str(t)
