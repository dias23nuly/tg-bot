from finance_manager import FinanceManager
from transaction import Income, Expense


def test_balance_calculation(tmp_path):
    data_file = tmp_path / "test_data.json"
    budget_file = tmp_path / "test_budgets.json"

    manager = FinanceManager(data_file=str(data_file), budget_file=str(budget_file))

    user_id = "test_user"

    manager.add_transaction(user_id, Income(1000, "Salary"))
    manager.add_transaction(user_id, Expense(300, "Food"))

    assert manager.get_balance(user_id) == 700


def test_expense_statistics(tmp_path):
    data_file = tmp_path / "test_data.json"
    budget_file = tmp_path / "test_budgets.json"

    manager = FinanceManager(data_file=str(data_file), budget_file=str(budget_file))

    user_id = "test_user"

    manager.add_transaction(user_id, Expense(500, "Food"))
    manager.add_transaction(user_id, Expense(200, "Transport"))
    manager.add_transaction(user_id, Expense(300, "Food"))

    stats = manager.get_statistics(user_id)

    assert stats["Food"] == 800
    assert stats["Transport"] == 200


def test_delete_last_transaction(tmp_path):
    data_file = tmp_path / "test_data.json"
    budget_file = tmp_path / "test_budgets.json"

    manager = FinanceManager(data_file=str(data_file), budget_file=str(budget_file))

    user_id = "test_user"

    manager.add_transaction(user_id, Income(1000, "Salary"))
    manager.add_transaction(user_id, Expense(400, "Food"))

    deleted = manager.delete_last_transaction(user_id)

    assert deleted["amount"] == 400
    assert manager.get_balance(user_id) == 1000


def test_budget_warning(tmp_path):
    data_file = tmp_path / "test_data.json"
    budget_file = tmp_path / "test_budgets.json"

    manager = FinanceManager(data_file=str(data_file), budget_file=str(budget_file))

    user_id = "test_user"

    manager.set_budget(user_id, "Food", 1000)
    manager.add_transaction(user_id, Expense(850, "Food"))

    warning = manager.check_budget_warning(user_id, "Food")

    assert warning is not None