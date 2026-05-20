import asyncio
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, BufferedInputFile
from dotenv import load_dotenv

from transaction import Income, Expense
from finance_manager import FinanceManager
from currency_api import CurrencyAPI


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

if TOKEN is None:
    raise ValueError("BOT_TOKEN is missing. Please add it to your .env file.")

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

manager = FinanceManager()
currency_api = CurrencyAPI()

user_states = {}


def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Add Income"), KeyboardButton(text="➖ Add Expense")],
            [KeyboardButton(text="💰 Balance"), KeyboardButton(text="📜 History")],
            [KeyboardButton(text="📊 Statistics"), KeyboardButton(text="📅 Monthly Report")],
            [KeyboardButton(text="🎯 Set Budget"), KeyboardButton(text="📋 My Budgets")],
            [KeyboardButton(text="✏️ Edit Last"), KeyboardButton(text="🗑 Delete Last")],
            [KeyboardButton(text="📁 Export CSV"), KeyboardButton(text="💱 Currency Rates")],
            [KeyboardButton(text="ℹ️ About"), KeyboardButton(text="🆘 Help")]
        ],
        resize_keyboard=True
    )


def income_categories_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💼 Salary"), KeyboardButton(text="🎁 Gift")],
            [KeyboardButton(text="💸 Bonus"), KeyboardButton(text="💻 Freelance")],
            [KeyboardButton(text="➕ Other Income")],
            [KeyboardButton(text="⬅️ Back")]
        ],
        resize_keyboard=True
    )


def expense_categories_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🍔 Food"), KeyboardButton(text="🚕 Transport")],
            [KeyboardButton(text="🎮 Entertainment"), KeyboardButton(text="🏠 Rent")],
            [KeyboardButton(text="🛒 Shopping"), KeyboardButton(text="📚 Education")],
            [KeyboardButton(text="💊 Health"), KeyboardButton(text="➕ Other Expense")],
            [KeyboardButton(text="⬅️ Back")]
        ],
        resize_keyboard=True
    )


def transaction_type_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="income"), KeyboardButton(text="expense")],
            [KeyboardButton(text="⬅️ Back")]
        ],
        resize_keyboard=True
    )


def clean_category(text):
    categories = {
        "💼 Salary": "Salary",
        "🎁 Gift": "Gift",
        "💸 Bonus": "Bonus",
        "💻 Freelance": "Freelance",
        "➕ Other Income": "Other Income",
        "🍔 Food": "Food",
        "🚕 Transport": "Transport",
        "🎮 Entertainment": "Entertainment",
        "🏠 Rent": "Rent",
        "🛒 Shopping": "Shopping",
        "📚 Education": "Education",
        "💊 Health": "Health",
        "➕ Other Expense": "Other Expense"
    }

    return categories.get(text, text)


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 <b>Welcome to Finance Tracker Bot!</b>\n\n"
        "This bot helps users track income, expenses, balance, statistics, "
        "monthly reports, budget limits, and currency rates.\n\n"
        "Choose an option from the menu 👇",
        reply_markup=main_menu()
    )


@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "🆘 <b>Help</b>\n\n"
        "➕ Add Income — add income transaction\n"
        "➖ Add Expense — add expense transaction\n"
        "💰 Balance — show current balance\n"
        "📜 History — show last transactions\n"
        "📊 Statistics — show expenses by category\n"
        "📅 Monthly Report — show monthly summary\n"
        "🎯 Set Budget — set spending limit\n"
        "📋 My Budgets — show saved limits\n"
        "✏️ Edit Last — update last transaction\n"
        "🗑 Delete Last — delete last transaction\n"
        "📁 Export CSV — export history as CSV file\n"
        "💱 Currency Rates — get USD and EUR exchange rates\n\n"
        "You can also send a photo of a receipt. The bot will recognize it as an image message.",
        reply_markup=main_menu()
    )


@dp.message(Command("about"))
async def about_command(message: types.Message):
    await message.answer(
        "ℹ️ <b>About Finance Tracker Bot</b>\n\n"
        "Finance Tracker Bot is a Telegram bot created for personal finance management.\n\n"
        "Technologies used:\n"
        "• Python\n"
        "• aiogram\n"
        "• JSON file storage\n"
        "• External currency API\n"
        "• Object-Oriented Programming\n\n"
        "Main goal: help users control income, expenses, budgets, and financial statistics.",
        reply_markup=main_menu()
    )


@dp.message(F.text == "ℹ️ About")
async def about_button(message: types.Message):
    await about_command(message)


@dp.message(F.text == "🆘 Help")
async def help_button(message: types.Message):
    await help_command(message)


@dp.message(F.text == "⬅️ Back")
async def back(message: types.Message):
    user_states.pop(message.chat.id, None)
    await message.answer("Main menu 👇", reply_markup=main_menu())


@dp.message(F.text == "➕ Add Income")
async def add_income(message: types.Message):
    user_states[message.chat.id] = "income_amount"

    await message.answer(
        "➕ <b>Add Income</b>\n\n"
        "Enter income amount:\n"
        "Example: <code>50000</code>"
    )


@dp.message(F.text == "➖ Add Expense")
async def add_expense(message: types.Message):
    user_states[message.chat.id] = "expense_amount"

    await message.answer(
        "➖ <b>Add Expense</b>\n\n"
        "Enter expense amount:\n"
        "Example: <code>2500</code>"
    )


@dp.message(F.text == "💰 Balance")
async def show_balance(message: types.Message):
    balance = manager.get_balance(message.chat.id)

    await message.answer(
        "💰 <b>Your Balance</b>\n\n"
        f"Current balance: <b>{balance} KZT</b>",
        reply_markup=main_menu()
    )


@dp.message(F.text == "📜 History")
async def show_history(message: types.Message):
    history = manager.get_history(message.chat.id)

    if len(history) == 0:
        await message.answer("📭 <b>History is empty.</b>", reply_markup=main_menu())
        return

    text = "📜 <b>Transaction History</b>\n\n"

    for index, item in enumerate(history[-10:], start=1):
        icon = "🟢" if item["type"] == "income" else "🔴"

        text += (
            f"{icon} <b>{index}. {item['type'].title()}</b>\n"
            f"💵 Amount: <b>{item['amount']} KZT</b>\n"
            f"🏷 Category: <i>{item['category']}</i>\n"
            f"📅 Date: {item['date']}\n\n"
        )

    await message.answer(text, reply_markup=main_menu())


@dp.message(F.text == "📊 Statistics")
async def show_statistics(message: types.Message):
    stats = manager.get_statistics_with_percent(message.chat.id)

    if len(stats) == 0:
        await message.answer("📊 <b>No expenses yet.</b>", reply_markup=main_menu())
        return

    text = "📊 <b>Expense Statistics</b>\n\n"

    for category, info in stats.items():
        text += (
            f"🔹 <b>{category}</b>: "
            f"{info['amount']} KZT — {info['percent']}%\n"
        )

    await message.answer(text, reply_markup=main_menu())


@dp.message(F.text == "📅 Monthly Report")
async def monthly_report(message: types.Message):
    report = manager.get_monthly_report(message.chat.id)

    text = (
        f"📅 <b>Monthly Report</b>\n\n"
        f"Month: <b>{report['month']}</b>\n\n"
        f"🟢 Income: <b>{report['income']} KZT</b>\n"
        f"🔴 Expenses: <b>{report['expense']} KZT</b>\n"
        f"💰 Balance: <b>{report['balance']} KZT</b>\n\n"
    )

    if report["top_category"] is not None:
        text += (
            f"🏆 Top expense category:\n"
            f"<b>{report['top_category']}</b> — {report['top_amount']} KZT"
        )
    else:
        text += "No expenses this month."

    await message.answer(text, reply_markup=main_menu())


@dp.message(F.text == "🎯 Set Budget")
async def set_budget_start(message: types.Message):
    user_states[message.chat.id] = "budget_category"

    await message.answer(
        "🎯 <b>Set Budget</b>\n\n"
        "Choose expense category:",
        reply_markup=expense_categories_menu()
    )


@dp.message(F.text == "📋 My Budgets")
async def show_budgets(message: types.Message):
    budgets = manager.get_budgets(message.chat.id)

    if len(budgets) == 0:
        await message.answer("📋 <b>You have no budgets yet.</b>", reply_markup=main_menu())
        return

    text = "📋 <b>Your Budgets</b>\n\n"

    for category, limit in budgets.items():
        text += f"🎯 <b>{category}</b>: {limit} KZT\n"

    await message.answer(text, reply_markup=main_menu())


@dp.message(F.text == "✏️ Edit Last")
async def edit_last_start(message: types.Message):
    last = manager.get_last_transaction(message.chat.id)

    if last is None:
        await message.answer("✏️ <b>No transactions to edit.</b>", reply_markup=main_menu())
        return

    user_states[message.chat.id] = "edit_last_amount"

    await message.answer(
        "✏️ <b>Edit Last Transaction</b>\n\n"
        f"Current type: <b>{last['type']}</b>\n"
        f"Current amount: <b>{last['amount']} KZT</b>\n"
        f"Current category: <b>{last['category']}</b>\n\n"
        "Enter new amount:",
    )


@dp.message(F.text == "🗑 Delete Last")
async def delete_last(message: types.Message):
    deleted = manager.delete_last_transaction(message.chat.id)

    if deleted is None:
        await message.answer("🗑 <b>No transactions to delete.</b>", reply_markup=main_menu())
    else:
        await message.answer(
            "🗑 <b>Transaction deleted</b>\n\n"
            f"Type: <b>{deleted['type'].title()}</b>\n"
            f"Amount: <b>{deleted['amount']} KZT</b>\n"
            f"Category: <i>{deleted['category']}</i>",
            reply_markup=main_menu()
        )


@dp.message(F.text == "📁 Export CSV")
async def export_csv(message: types.Message):
    csv_text = manager.export_csv(message.chat.id)

    file = BufferedInputFile(
        csv_text.encode("utf-8"),
        filename="finance_history.csv"
    )

    await message.answer_document(
        document=file,
        caption="📁 Here is your finance history in CSV format."
    )


@dp.message(F.text == "💱 Currency Rates")
async def currency_rates(message: types.Message):
    rates = currency_api.get_rates()

    if rates is None:
        await message.answer("⚠️ Could not load currency rates. Try again later.")
        return

    await message.answer(
        "💱 <b>Current Currency Rates</b>\n\n"
        f"🇺🇸 1 USD = <b>{rates['USD_KZT']} KZT</b>\n"
        f"🇪🇺 1 EUR = <b>{rates['EUR_KZT']} KZT</b>",
        reply_markup=main_menu()
    )


@dp.message(F.photo)
async def handle_photo(message: types.Message):
    await message.answer(
        "🖼 <b>Photo received!</b>\n\n"
        "This version recognizes image messages. "
        "In future updates, this feature can be improved to scan receipts automatically.",
        reply_markup=main_menu()
    )


@dp.message()
async def handle_messages(message: types.Message):
    chat_id = message.chat.id

    if chat_id not in user_states:
        await message.answer(
            "⚠️ Please choose an option from the menu.",
            reply_markup=main_menu()
        )
        return

    state = user_states[chat_id]

    try:
        if state == "income_amount":
            amount = float(message.text)

            if amount <= 0:
                await message.answer("⚠️ Amount must be greater than 0.")
                return

            user_states[chat_id] = {
                "type": "income_category",
                "amount": amount
            }

            await message.answer(
                "🏷 Choose income category:",
                reply_markup=income_categories_menu()
            )

        elif state == "expense_amount":
            amount = float(message.text)

            if amount <= 0:
                await message.answer("⚠️ Amount must be greater than 0.")
                return

            user_states[chat_id] = {
                "type": "expense_category",
                "amount": amount
            }

            await message.answer(
                "🏷 Choose expense category:",
                reply_markup=expense_categories_menu()
            )

        elif isinstance(state, dict) and state["type"] == "income_category":
            category = clean_category(message.text)

            income = Income(state["amount"], category)
            manager.add_transaction(chat_id, income)

            user_states.pop(chat_id, None)

            await message.answer(
                "✅ <b>Income added successfully!</b>",
                reply_markup=main_menu()
            )

        elif isinstance(state, dict) and state["type"] == "expense_category":
            category = clean_category(message.text)

            expense = Expense(state["amount"], category)
            manager.add_transaction(chat_id, expense)

            user_states.pop(chat_id, None)

            text = "✅ <b>Expense added successfully!</b>"

            warning = manager.check_budget_warning(chat_id, category)

            if warning is not None:
                text += f"\n\n{warning}"

            await message.answer(text, reply_markup=main_menu())

        elif state == "budget_category":
            category = clean_category(message.text)

            user_states[chat_id] = {
                "type": "budget_limit",
                "category": category
            }

            await message.answer(
                f"🎯 Category: <b>{category}</b>\n\n"
                "Enter budget limit in KZT:\n"
                "Example: <code>50000</code>"
            )

        elif isinstance(state, dict) and state["type"] == "budget_limit":
            limit = float(message.text)

            if limit <= 0:
                await message.answer("⚠️ Budget must be greater than 0.")
                return

            category = state["category"]

            manager.set_budget(chat_id, category, limit)

            user_states.pop(chat_id, None)

            await message.answer(
                f"✅ Budget saved!\n\n"
                f"🎯 <b>{category}</b>: {limit} KZT",
                reply_markup=main_menu()
            )

        elif state == "edit_last_amount":
            amount = float(message.text)

            if amount <= 0:
                await message.answer("⚠️ Amount must be greater than 0.")
                return

            user_states[chat_id] = {
                "type": "edit_last_category",
                "amount": amount
            }

            await message.answer(
                "Choose new category:",
                reply_markup=expense_categories_menu()
            )

        elif isinstance(state, dict) and state["type"] == "edit_last_category":
            amount = state["amount"]
            category = clean_category(message.text)

            last = manager.get_last_transaction(chat_id)

            if last is None:
                user_states.pop(chat_id, None)
                await message.answer("⚠️ No transaction found.", reply_markup=main_menu())
                return

            manager.update_last_transaction(
                user_id=chat_id,
                amount=amount,
                category=category,
                transaction_type=last["type"]
            )

            user_states.pop(chat_id, None)

            await message.answer(
                "✅ <b>Last transaction updated!</b>\n\n"
                f"Amount: <b>{amount} KZT</b>\n"
                f"Category: <b>{category}</b>",
                reply_markup=main_menu()
            )

    except ValueError:
        await message.answer("⚠️ Please enter a valid number.")
    except Exception as error:
        await message.answer(
            "❌ Something went wrong. Please try again.\n\n"
            f"Error: <code>{error}</code>",
            reply_markup=main_menu()
        )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())