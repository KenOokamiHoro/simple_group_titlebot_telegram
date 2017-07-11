#!/usr/bin/python
# from telegram.bot import Bot
import os
import subprocess
import random
import sys
import time

from telegram.chataction import ChatAction
from telegram.error import TelegramError

import config
import db
import helpers


def eat(target):
    prompts = ["😋 => {}", "😋({})"]
    return random.choice(prompts).format(target)


@helpers.group_required
def start(bot, update):
    '''resopnse /start'''
    if update.message.from_user in helpers.get_admin_ids(bot, update,
                                                         update.message.chat_id):
        init(bot, update)
    else:
        update.message.reply_text("呼叫管理员用 /init 初始化啦~")


@helpers.group_required
@helpers.admin_required
def init(bot, update):
    title = bot.getChat(update.message.chat_id).title
    config.dbc.init_title(group=update.message.chat_id, title=title)
    update.message.reply_text("准备就绪 😋")


@helpers.group_required
def status(bot, update):
    current_title = bot.getChat(update.message.chat_id).title
    original_title = config.dbc.Query(db.Title).filter_by(
        group_id=update.message.chat_id).first().title

    current_title = current_title.replace(
        original_title, "").lstrip().split(" ")
    message_text = "{}\n    {}".format(
        original_title, "\n    ".join(current_title))
    update.message.reply_text(message_text)


@helpers.group_required
def append(bot, update, args):
    if args:
        title = "{} {}".format(bot.getChat(update.message.chat_id).title,
                               args[0])
        bot.set_chat_title(chat_id=update.message.chat_id, title=title)


@helpers.group_required
def lappend(bot, update, args):
    if args:
        original_title = config.dbc.Query(db.Title).filter_by(
            group_id=update.message.chat_id).first().title
        current_title = bot.getChat(update.message.chat_id).title.replace(
            original_title, "")

        title = "{} {} {}".format(original_title, args[0], current_title)
        bot.set_chat_title(chat_id=update.message.chat_id, title=title)


@helpers.group_required
def pop(bot, update):
    current_title = bot.getChat(update.message.chat_id).title.strip()
    original_title = config.dbc.Query(db.Title).filter_by(
        group_id=update.message.chat_id).first().title
    if current_title == original_title:
        update.message.reply_text("🍃")
        return
    else:
        current_title = current_title.replace(
            original_title, "").lstrip().split(" ")
        current_title.pop()
        title = "{} {}".format(original_title, " ".join(current_title))
        bot.set_chat_title(chat_id=update.message.chat_id,
                           title=title)


@helpers.group_required
def lpop(bot, update):
    current_title = bot.getChat(update.message.chat_id).title.strip()
    original_title = config.dbc.Query(db.Title).filter_by(
        group_id=update.message.chat_id).first().title
    if current_title == original_title:
        update.message.reply_text("🍃")
        return
    else:
        current_title = current_title.replace(
            original_title, "").lstrip().split(" ")[1:]
        title = "{} {}".format(original_title, " ".join(current_title))
        bot.set_chat_title(chat_id=update.message.chat_id,
                           title=title)


@helpers.group_required
def empty(bot, update):
    current_title = bot.getChat(update.message.chat_id).title
    original_title = config.dbc.Query(db.Title).filter_by(
        group_id=update.message.chat_id).first().title
    current_title = current_title.replace(original_title, "").lstrip()
    bot.set_chat_title(chat_id=update.message.chat_id, title=original_title)


@helpers.operator_required
def restart(bot, update):
    bot.send_message(update.message.chat_id, "受汝照顾了。")
    time.sleep(0.2)
    os.execl(sys.executable, sys.executable, *sys.argv)


@helpers.operator_required
def upgrade(bot, update):
    try:
        proc = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, universal_newlines=True)
        time.sleep(3)
        bot.sendMessage(chat_id=update.message.chat_id, text="受汝照顾了。")
        os.execl(sys.executable, sys.executable, *sys.argv)
    except subprocess.CalledProcessError:
        bot.sendMessage(chat_id=update.message.chat_id, text="唔，发生了点意外😱")
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=proc.stderr.read())
