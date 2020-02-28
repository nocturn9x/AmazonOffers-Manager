from pyrogram import Filters, InlineKeyboardMarkup, InlineKeyboardButton, Client
from pyrogram.errors import *
import time
import logging
from collections import defaultdict


BANNED_USERS = Filters.chat()
messages = defaultdict(list)


@Client.on_message(Filters.private & ~BANNED_USERS)
def anti_flood(client, message):
    if len(messages[client.id]) == 7:
        timestamps = messages.pop(client.id)
        subtractions = []
        for index, timestamp in enumerate(timestamps):
            if index < 6:
                subtractions.append(timestamp - timestamps[index + 1])
            else:
                subtractions.append(timestamps[index - 1] - timestamp)
        if all(i <= 0.5 for i in subtractions):
            logging.debug(f"Flood detected from {client.id}")
    else:
        messages[client.id].append(message.date)
