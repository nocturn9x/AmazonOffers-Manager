from pyrogram import Filters, InlineKeyboardMarkup, InlineKeyboardButton, Client
from pyrogram.errors import *
import time
import logging
BANNED_USERS = Filters.chat()


@Client.on_message(Filters.private & ~BANNED_USERS)
def antiflood(client, message):
    pass