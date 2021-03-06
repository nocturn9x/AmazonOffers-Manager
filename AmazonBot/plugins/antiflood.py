from pyrogram import Filters, InlineKeyboardMarkup, InlineKeyboardButton, Client
import time
import logging
from collections import defaultdict
from ..config import MAX_MESS_THRESHOLD, BAN_TIME
import time


messages = defaultdict(list)
BANNED_USERS = Filters.chat()


@Client.on_message(Filters.private, group=-1)
def anti_flood(client, message):
    if isinstance(messages[message.from_user.id], tuple):
        if time.time() - messages[message.from_user.id][1] >= BAN_TIME:
            BANNED_USERS.remove(message.from_user.id)
            messages[message.from_user.id] = []
    elif len(messages[message.from_user.id]) == MAX_MESS_THRESHOLD:
        timestamps = messages.pop(message.from_user.id)
        subtractions = []
        for index, timestamp in enumerate(timestamps):
            if index < MAX_MESS_THRESHOLD - 1:
                subtractions.append(timestamp - timestamps[index + 1])
            else:
                subtractions.append(timestamps[index - 1] - timestamp)
        if all(i <= 0.5 for i in subtractions):
            logging.debug(f"Flood detected from {message.from_user.id}")
            BANNED_USERS.add(message.from_user.id)
            messages[message.from_user.id] = 'remove_at', time.time()
        else:
            messages[message.from_user.id] = []
    else:
        messages[message.from_user.id].append(message.date)
