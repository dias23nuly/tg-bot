from datetime import datetime
import csv
import io

from storage import Storage


class FinanceManager:
    def __init__(self, data_file="data.json", budget_file="budgets.json"):
        self.storage = Storage(data_file)
        self.budget_storage = Storage(budget_file)

    def add_transaction(self, user_id, transaction):
        data = self.storage.load_data()
        user_id = str(user_id)

        if user_id not in data:
            data[user_id] = []

        data[user_id].append(transaction.to_dict())
        self.storage.save_data(data)

    def get_history(self, user_id):
        data = self.storage.load_data()
        return data.get(str(user_id), [])

    def get_last_transaction(self, user_id):
        history = self.get_history(user_id)

        if len(history) == 0:
            return None

        return history[-1]

    def get_balance(self, user_id):
        history = self.get_history(user_id)

        income = sum(item["amount"] for item in history if item["type"] == "income")
        expense = sum(item["amount"] for item in history if item["type"] == "expense")

        return income - expense

    def get_statistics(self, user_id):
        history = self.get_history(user_id)
        stats = {}

        for item in history:
            if item["type"] == "expense":
                category = item["category"]

                if category not in stats:
                    stats[category] = 0

                stats[category] += item["amount"]

        return stats

    def get_statistics_with_percent(self, user_id):
        stats = self.get_statistics(user_id)
        total = sum(stats.values())

        result = {}

        for category, amount in stats.items():
            percent = round((amount / total) * 100, 1) if total > 0 else 0

            result[category] = {
                "amount": amount,
                "percent": percent
            }

        return result

    def delete_last_transaction(self, user_id):
        data = self.storage.load_data()
        user_id = str(user_id)

        if user_id not in data or len(data[user_id]) == 0:
            return None

        deleted = data[user_id].pop()
        self.storage.save_data(data)

        return deleted

    def update_last_transaction(self, user_id, amount, category, transaction_type):
        data = self.storage.load_data()
        user_id = str(user_id)

        if user_id not in data or len(data[user_id]) == 0:
            return None

        data[user_id][-1]["amount"] = amount
        data[user_id][-1]["category"] = category
        data[user_id][-1]["type"] = transaction_type
        data[user_id][-1]["date"] = datetime.now().strftime("%Y-%m-%d %H:%M")

        self.storage.save_data(data)

        return data[user_id][-1]

    def get_monthly_report(self, user_id):
        history = self.get_history(user_id)
        current_month = datetime.now().strftime("%Y-%m")

        income = 0
        expense = 0
        category_expenses = {}

        for item in history:
            if item["date"].startswith(current_month):
                if item["type"] == "income":
                    income += item["amount"]
                elif item["type"] == "expense":
                    expense += item["amount"]

                    category = item["category"]

                    if category not in category_expenses:
                        category_expenses[category] = 0

                    category_expenses[category] += item["amount"]

        balance = income - expense

        top_category = None
        top_amount = 0

        if category_expenses:
            top_category = max(category_expenses, key=category_expenses.get)
            top_amount = category_expenses[top_category]

        return {
            "month": current_month,
            "income": income,
            "expense": expense,
            "balance": balance,
            "top_category": top_category,
            "top_amount": top_amount
        }

    def set_budget(self, user_id, category, limit):
        data = self.budget_storage.load_data()
        user_id = str(user_id)

        if user_id not in data:
            data[user_id] = {}

        data[user_id][category] = limit
        self.budget_storage.save_data(data)

    def get_budgets(self, user_id):
        data = self.budget_storage.load_data()
        return data.get(str(user_id), {})

    def check_budget_warning(self, user_id, category):
        budgets = self.get_budgets(user_id)

        if category not in budgets:
            return None

        limit = budgets[category]
        stats = self.get_statistics(user_id)
        spent = stats.get(category, 0)

        if spent >= limit:
            return f"🚨 You exceeded your budget for {category}: {spent} / {limit} KZT"

        if spent >= limit * 0.8:
            return f"⚠️ You spent {spent} / {limit} KZT on {category}. Be careful!"

        return None

    def export_csv(self, user_id):
        history = self.get_history(user_id)

        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(["date", "type", "category", "amount"])

        for item in history:
            writer.writerow([
                item["date"],
                item["type"],
                item["category"],
                item["amount"]
            ])

        return output.getvalue()