''' Main script _(:з」∠)_'''
# !/usr/bin/python
# -*- coding: utf-8 -*-

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          RegexHandler, ConversationHandler)
from telegram.ext.filters import Filters
from telegram.bot import Bot
from telegram.chataction import ChatAction
import logging
import config
import actions
import sys
import db


class TitleBot:
    def __init__(self):
        # Setting up bot
        self.updater = Updater(token=config.token)
        self.dispatcher = self.updater.dispatcher
        self.botObj = Bot(token=config.token)
        # Register handlers
        self.dispatcher.add_handler(CommandHandler('start', actions.start))
        self.dispatcher.add_handler(CommandHandler('init', actions.init))
        self.dispatcher.add_handler(CommandHandler('status', actions.status))
        self.dispatcher.add_handler(CommandHandler('empty', actions.empty))
        self.dispatcher.add_handler(CommandHandler(
            'append', actions.append, pass_args=True))
        self.dispatcher.add_handler(CommandHandler('pop', actions.pop))
        self.dispatcher.add_handler(CommandHandler(
            'lappend', actions.lappend, pass_args=True))
        self.dispatcher.add_handler(CommandHandler('lpop', actions.lpop))
        self.dispatcher.add_handler(CommandHandler('restart', actions.restart))
        self.dispatcher.add_handler(CommandHandler('update', actions.upgrade))

    def start(self):
        self.updater.start_polling()

    def __str__(self):
        return str(self.botObj)


if __name__ == "__main__":
    # import bot components
    try:
        import config
    except ImportError:
        print("Please create config file 'config.py' first.")
        exit(1)
    logging.basicConfig(stream=sys.stderr,
                        format='%(message)s', level=logging.DEBUG)
    bot = TitleBot()
    bot.start()
