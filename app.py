from flask import Flask, jsonify
import requests
import telegram

import os
from telegram.ext import Updater, CommandHandler, Dispatcher
from handlers import index, currency

TELEGRAM_BOT_TOKEN: str = os.environ.get("TELEGRAM_BOT_TOKEN")
updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)


def register_handlers(dispatcher: Dispatcher):
    """Register and add handler in this function"""
    dispatcher.add_handler(CommandHandler("start", index))
    dispatcher.add_handler(CommandHandler("rates", currency))


register_handlers(updater.dispatcher)
updater.start_polling()

app = Flask(__name__)

if __name__ == "__main__":
    app.run(port=5000)
