"""Full passing test suite — the instructor's walkthrough solution.

These tests demonstrate the complete Red → Green → Refactor cycle applied to
all six user requirements of the Bank Account kata.
"""

from datetime import datetime

import pytest

from bank.account import Account, TransactionType


class TestDeposit:
    def test_deposit_increases_balance(self) -> None:
        account = Account()
        account.deposit(100)
        assert account.balance() == 100

    def test_multiple_deposits_accumulate(self) -> None:
        account = Account()
        account.deposit(100)
        account.deposit(50)
        assert account.balance() == 150

    def test_deposit_with_zero_raises(self) -> None:
        account = Account()
        with pytest.raises(ValueError):
            account.deposit(0)

    def test_deposit_with_negative_raises(self) -> None:
        account = Account()
        with pytest.raises(ValueError):
            account.deposit(-10)


class TestWithdraw:
    def test_withdrawal_decreases_balance(self) -> None:
        account = Account()
        account.deposit(100)
        account.withdraw(40)
        assert account.balance() == 60

    def test_full_withdrawal_leaves_zero_balance(self) -> None:
        account = Account()
        account.deposit(100)
        account.withdraw(100)
        assert account.balance() == 0

    def test_cannot_withdraw_more_than_balance(self) -> None:
        account = Account()
        account.deposit(100)
        with pytest.raises(ValueError):
            account.withdraw(200)

    def test_withdrawal_with_zero_raises(self) -> None:
        account = Account()
        account.deposit(100)
        with pytest.raises(ValueError):
            account.withdraw(0)


class TestTransfer:
    def test_transfer_moves_funds_between_accounts(self) -> None:
        source = Account()
        target = Account()
        source.deposit(200)
        source.transfer(75, target)
        assert source.balance() == 125
        assert target.balance() == 75

    def test_transfer_fails_with_insufficient_funds(self) -> None:
        source = Account()
        target = Account()
        source.deposit(50)
        with pytest.raises(ValueError):
            source.transfer(100, target)

    def test_transfer_does_not_alter_target_on_failure(self) -> None:
        source = Account()
        target = Account()
        source.deposit(50)
        with pytest.raises(ValueError):
            source.transfer(100, target)
        assert target.balance() == 0


class TestBalanceSlip:
    def test_balance_slip_contains_balance(self) -> None:
        account = Account()
        account.deposit(250)
        slip = account.balance_slip()
        assert "250.00" in slip

    def test_balance_slip_contains_date(self) -> None:
        account = Account()
        account.deposit(100)
        slip = account.balance_slip()
        assert str(datetime.now().year) in slip

    def test_balance_slip_contains_label(self) -> None:
        account = Account()
        account.deposit(100)
        slip = account.balance_slip()
        assert "Balance" in slip


class TestStatement:
    def test_statement_lists_all_transactions(self) -> None:
        account = Account()
        account.deposit(500)
        account.withdraw(100)
        stmt = account.statement()
        assert "DEPOSIT" in stmt
        assert "WITHDRAWAL" in stmt

    def test_statement_shows_correct_balance(self) -> None:
        account = Account()
        account.deposit(500)
        account.withdraw(100)
        stmt = account.statement()
        assert "400.00" in stmt

    def test_statement_filter_deposits_only(self) -> None:
        account = Account()
        account.deposit(500)
        account.withdraw(100)
        stmt = account.statement(filter_type=TransactionType.DEPOSIT)
        assert "DEPOSIT" in stmt
        assert "WITHDRAWAL" not in stmt

    def test_statement_filter_withdrawals_only(self) -> None:
        account = Account()
        account.deposit(500)
        account.withdraw(100)
        stmt = account.statement(filter_type=TransactionType.WITHDRAWAL)
        assert "WITHDRAWAL" in stmt
        assert "DEPOSIT" not in stmt

    def test_statement_empty_account(self) -> None:
        account = Account()
        stmt = account.statement()
        assert "0.00" in stmt
