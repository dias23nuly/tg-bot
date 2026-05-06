from datetime import datetime


class Transaction:
    def __init__(self, amount, category, transaction_type):
        self.amount = amount
        self.category = category
        self.transaction_type = transaction_type
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "type": self.transaction_type,
            "date": self.date
        }


class Income(Transaction):
    def __init__(self, amount, category):
        super().__init__(amount, category, "income")


class Expense(Transaction):
    def __init__(self, amount, category):
        super().__init__(amount, category, "expense")