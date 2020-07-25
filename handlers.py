from typing import List, Dict

import requests
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode

import utilities
from enums import bank_names, flags


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


def exchange(update, context):
    button_list = [
        InlineKeyboardButton(
            f"{currency_name} {flag}", callback_data=str(currency_name)
        )
        for currency_name, flag in flags.items()
    ]
    reply_markup = InlineKeyboardMarkup(utilities.build_menu(button_list, n_cols=2))
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Choose a currency to exchange",
        reply_markup=reply_markup,
    )


def button(update, context):
    query = update.callback_query
    callback_data = query.data

    currency_url: str = "https://still-badlands-57221.herokuapp.com/currency?by=rate"
    exchange_rates = requests.get(currency_url).json()
    exchange_rate_for_currency = exchange_rates.get(callback_data)
    if exchange_rate_for_currency:
        message: str = f"Exchange rate for {callback_data} {flags[callback_data]}\n\n"
        for k in exchange_rate_for_currency:
            for bank_name, rate in k.items():
                buy_amount = float(rate["buy"]) if rate["buy"] != "-" else 0

                message += f"*\t\t{bank_names[bank_name]}: {int(buy_amount)}*\n"
    else:
        message: str = f"Exchange rate for {callback_data} {flags[callback_data]} is not available"

    context.bot.send_message(
        text=message,
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        parse_mode=ParseMode.MARKDOWN,
    )
