# Telegram Finance Tracker Bot

## About Project

This project is a simple Telegram bot for tracking personal finance.  
User can add income and expenses and check balance.  
Main idea of project was practice Python and Telegram bot development.

Bot was made with Python and library `python-telegram-bot`.

---

# What Bot Can Do

Bot have some basic commands:

- add income
- add expense
- show balance
- show history
- save transactions

Example:

User writes:
```text
Food 5000
```

Bot saves this expense and updates balance.

---

# Technologies

- Python
- Telegram Bot API
- JSON
- OOP
- python-telegram-bot

---

# Files Explanation

## bot.py

This is main file.

It starts bot and handles commands from users.  
Also connects all other files together.

Without this file bot will not work.

---

## finance_manager.py

This file have main finance logic.

It:
- adds transactions
- calculates balance
- stores incomes and expenses
- shows history

This file is like main system of project.

---

## transaction.py

Here we created `Transaction` class.

Class stores:
- amount
- type
- category
- date

Example:
```python
Transaction("expense", 5000, "Food")
```

We used class because it is easier to organize data.

---

## storage.py

This file works with saving data.

It:
- reads json file
- saves json file
- loads transactions after restart

Without this file all data will disappear after bot closes.

---

## data.json

This file stores all transactions.

Example:
```json
[
  {
    "type": "expense",
    "amount": 5000,
    "category": "Food"
  }
]
```

---

# How Bot Works

1. User sends command
2. Bot gets message
3. `bot.py` sends info to finance manager
4. transaction object is created
5. data saves in json
6. bot sends answer back

---

# OOP In Project

Project uses OOP concepts:
- class
- object
- methods
- constructor

Example:
```python
class Transaction:
    def __init__(self, type, amount, category):
        self.type = type
        self.amount = amount
        self.category = category
```

---

# Problems During Work

During development there was some problems:

- telegram api errors
- saving data wrong
- problems with user input
- connecting files together

But after debugging project started working correctly.

---

# Conclusion

This project helped practice Python better and understand how Telegram bots works.

Also project helped improve:
- OOP skills
- file handling
- json usage
- working with modules

In future project can be improved with:
- database
- charts
- better statistics
- multi user system
- ai support ?

Overall this was good beginner project for practicing Telegram bot development.
