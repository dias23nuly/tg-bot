import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from transaction import Income, Expense
from finance_manager import FinanceManager


TOKEN = "7819915716:AAETR-h4gMxbX7x3rEHsib2W3cj0LAnKhss"

bot = Bot(token=TOKEN)
dp = Dispatcher()

manager = FinanceManager()
user_states = {}


def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Add Income"), KeyboardButton(text="Add Expense")],
            [KeyboardButton(text="Balance"), KeyboardButton(text="History")],
            [KeyboardButton(text="Statistics"), KeyboardButton(text="Delete Last")]
        ],
        resize_keyboard=True
    )


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Welcome to Finance Tracker Bot!\nChoose an option:",
        reply_markup=main_menu()
    )


@dp.message(F.text == "Add Income")
async def add_income(message: types.Message):
    user_states[message.chat.id] = "income_amount"
    await message.answer("Enter income amount:")


@dp.message(F.text == "Add Expense")
async def add_expense(message: types.Message):
    user_states[message.chat.id] = "expense_amount"
    await message.answer("Enter expense amount:")


@dp.message(F.text == "Balance")
async def show_balance(message: types.Message):
    balance = manager.get_balance(message.chat.id)
    await message.answer(f"Your balance: {balance} KZT")


@dp.message(F.text == "History")
async def show_history(message: types.Message):
    history = manager.get_history(message.chat.id)

    if len(history) == 0:
        await message.answer("History is empty.")
        return

    text = "Transaction history:\n\n"

    for index, item in enumerate(history[-10:], start=1):
        text += f"{index}. {item['type']} | {item['amount']} KZT | {item['category']} | {item['date']}\n"

    await message.answer(text)


@dp.message(F.text == "Statistics")
async def show_statistics(message: types.Message):
    stats = manager.get_statistics(message.chat.id)

    if len(stats) == 0:
        await message.answer("No expenses yet.")
        return

    text = "Expense statistics:\n\n"

    for category, amount in stats.items():
        text += f"{category}: {amount} KZT\n"

    await message.answer(text)


@dp.message(F.text == "Delete Last")
async def delete_last(message: types.Message):
    deleted = manager.delete_last_transaction(message.chat.id)

    if deleted is None:
        await message.answer("No transactions to delete.")
    else:
        await message.answer(
            f"Deleted: {deleted['type']} | {deleted['amount']} KZT | {deleted['category']}"
        )


@dp.message()
async def handle_messages(message: types.Message):
    chat_id = message.chat.id

    if chat_id not in user_states:
        await message.answer("Choose an option from the menu.", reply_markup=main_menu())
        return

    state = user_states[chat_id]

    try:
        if state == "income_amount":
            amount = float(message.text)

            if amount <= 0:
                await message.answer("Amount must be greater than 0.")
                return

            user_states[chat_id] = {
                "type": "income_category",
                "amount": amount
            }

            await message.answer("Enter income category:")

        elif state == "expense_amount":
            amount = float(message.text)

            if amount <= 0:
                await message.answer("Amount must be greater than 0.")
                return

            user_states[chat_id] = {
                "type": "expense_category",
                "amount": amount
            }

            await message.answer("Enter expense category:")

        elif isinstance(state, dict) and state["type"] == "income_category":
            income = Income(state["amount"], message.text)
            manager.add_transaction(chat_id, income)

            del user_states[chat_id]

            await message.answer("Income added successfully!", reply_markup=main_menu())

        elif isinstance(state, dict) and state["type"] == "expense_category":
            expense = Expense(state["amount"], message.text)
            manager.add_transaction(chat_id, expense)

            del user_states[chat_id]

            await message.answer("Expense added successfully!", reply_markup=main_menu())

    except ValueError:
        await message.answer("Please enter a valid number.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())