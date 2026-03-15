"""Unit tests for the TransactionType enum."""

from bank.transaction_type import TransactionType


class TestTransactionType:
    def test_deposit_value(self) -> None:
        assert TransactionType.DEPOSIT.value == "DEPOSIT"

    def test_withdrawal_value(self) -> None:
        assert TransactionType.WITHDRAWAL.value == "WITHDRAWAL"

    def test_deposit_and_withdrawal_are_distinct(self) -> None:
        assert TransactionType.DEPOSIT != TransactionType.WITHDRAWAL
