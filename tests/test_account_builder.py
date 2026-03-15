"""Unit tests for the AccountBuilder fluent builder."""

from bank.account import Account
from bank.account_builder import AccountBuilder


class TestAccountBuilder:
    def test_build_returns_account(self) -> None:
        account = AccountBuilder().build()
        assert isinstance(account, Account)

    def test_with_deposit_sets_balance(self) -> None:
        account = AccountBuilder().with_deposit(300).build()
        assert account.balance() == 300

    def test_with_withdrawal_reduces_balance(self) -> None:
        account = AccountBuilder().with_deposit(300).with_withdrawal(100).build()
        assert account.balance() == 200

    def test_chained_deposits_accumulate(self) -> None:
        account = (
            AccountBuilder()
            .with_deposit(100)
            .with_deposit(200)
            .build()
        )
        assert account.balance() == 300

    def test_each_build_returns_independent_account(self) -> None:
        builder = AccountBuilder().with_deposit(100)
        account_a = builder.build()
        account_a.deposit(50)
        account_b = builder.build()
        assert account_b.balance() == 100
