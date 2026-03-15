"""Unit tests for the TransactionLog first-class collection."""

from bank.amount import Amount
from bank.transaction import Transaction
from bank.transaction_log import TransactionLog
from bank.transaction_type import TransactionType


class TestTransactionLogBalance:
    def test_empty_log_balance_is_zero(self) -> None:
        assert TransactionLog().balance() == 0

    def test_single_deposit_sets_balance(self) -> None:
        log = TransactionLog()
        log.record(Transaction(Amount(200), TransactionType.DEPOSIT))
        assert log.balance() == 200

    def test_withdrawal_reduces_balance(self) -> None:
        log = TransactionLog()
        log.record(Transaction(Amount(200), TransactionType.DEPOSIT))
        log.record(Transaction(Amount(50), TransactionType.WITHDRAWAL))
        assert log.balance() == 150

    def test_multiple_deposits_accumulate(self) -> None:
        log = TransactionLog()
        log.record(Transaction(Amount(100), TransactionType.DEPOSIT))
        log.record(Transaction(Amount(75), TransactionType.DEPOSIT))
        assert log.balance() == 175


class TestTransactionLogFiltered:
    def test_filtered_deposits_only(self) -> None:
        log = TransactionLog()
        log.record(Transaction(Amount(500), TransactionType.DEPOSIT))
        log.record(Transaction(Amount(100), TransactionType.WITHDRAWAL))
        result = log.filtered(TransactionType.DEPOSIT)
        items = list(result)
        assert len(items) == 1
        assert items[0].transaction_type == TransactionType.DEPOSIT

    def test_filtered_withdrawals_only(self) -> None:
        log = TransactionLog()
        log.record(Transaction(Amount(500), TransactionType.DEPOSIT))
        log.record(Transaction(Amount(100), TransactionType.WITHDRAWAL))
        result = log.filtered(TransactionType.WITHDRAWAL)
        items = list(result)
        assert len(items) == 1
        assert items[0].transaction_type == TransactionType.WITHDRAWAL

    def test_filtered_none_returns_all(self) -> None:
        log = TransactionLog()
        log.record(Transaction(Amount(500), TransactionType.DEPOSIT))
        log.record(Transaction(Amount(100), TransactionType.WITHDRAWAL))
        assert len(list(log.filtered(None))) == 2

    def test_filtered_returns_new_log_instance(self) -> None:
        log = TransactionLog()
        log.record(Transaction(Amount(100), TransactionType.DEPOSIT))
        assert log.filtered() is not log


class TestTransactionLogIteration:
    def test_iterates_over_recorded_transactions(self) -> None:
        log = TransactionLog()
        t1 = Transaction(Amount(100), TransactionType.DEPOSIT)
        t2 = Transaction(Amount(50), TransactionType.WITHDRAWAL)
        log.record(t1)
        log.record(t2)
        assert list(log) == [t1, t2]
