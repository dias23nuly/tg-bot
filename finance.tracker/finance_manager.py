from storage import Storage


class FinanceManager:
    def __init__(self):
        self.storage = Storage()

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

    def delete_last_transaction(self, user_id):
        data = self.storage.load_data()
        user_id = str(user_id)

        if user_id not in data or len(data[user_id]) == 0:
            return None

        deleted = data[user_id].pop()
        self.storage.save_data(data)

        return deleted