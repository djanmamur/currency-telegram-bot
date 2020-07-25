import requests
import html
from typing import List, Dict
from enums import bank_names, flags
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode


def index(update, context):
    keyboard = [
        [InlineKeyboardButton("Message the developer", url="telegram.me/djanmamur")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome to currency exchange in Uzbekistan",
        reply_markup=reply_markup,
    )


def currency(update, context):
    currency_url: str = "https://still-badlands-57221.herokuapp.com/currency?by=rate"
    exchange_rates: List[Dict] = requests.get(currency_url).json()
    message: str = ""
    for exchange_rate in exchange_rates:
        flag: str = flags.get(exchange_rate, "")
        message += f"*{exchange_rate}* {flag}\n"
        for bank_rate in exchange_rates[exchange_rate]:
            for key, value in bank_rate.items():
                bank_name: str = bank_names[key]
                buy = value["buy"]
                sell = value["sell"] if value["sell"] != "-" else "N/A"
                message += f"*\t\t{bank_name}*\n"
                message += f"\t\tBuy: {buy}, Sell: {sell}\n"
        message += "\n"
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.MARKDOWN
    )
