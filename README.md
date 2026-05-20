# Finance Tracker Telegram Bot

## Project Description

Finance Tracker Bot is a Telegram bot for personal finance management.  
It helps users track income, expenses, current balance, expense statistics, monthly reports, budget limits, and currency exchange rates.

The project was created as a final Python project using Object-Oriented Programming, JSON file storage, exception handling, external API integration, and Telegram bot interaction.

## Features

- Add income transactions
- Add expense transactions
- Choose categories using interactive buttons
- View current balance
- View transaction history
- View expense statistics with percentages
- Generate monthly financial report
- Set budget limits by category
- Receive budget warnings
- Edit the last transaction
- Delete the last transaction
- Export transaction history to CSV
- Check USD/KZT and EUR/KZT currency rates
- Handle text commands
- Handle image messages
- Use JSON files for data persistence

## Technologies Used

- Python
- aiogram
- JSON
- CSV
- requests
- python-dotenv
- pytest
- Telegram Bot API
- External currency exchange API

## Project Structure

```text
finance_tracker_bot/
│
├── bot.py
├── finance_manager.py
├── transaction.py
├── storage.py
├── currency_api.py
├── test_finance_manager.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── REPORT.md