from pyrogram import Filters, Client
import time
import logging
from collections import defaultdict
from ..config import MAX_MESS_THRESHOLD, BAN_TIME



messages = defaultdict(list)
BANNED_USERS = Filters.user()

@Client.on_message(Filters.private, group=-1)
def anti_flood(client, message):
    if isinstance(messages[message.from_user.id], tuple):
        if (int(time.time())) - messages[message.from_user.id][1] >= BAN_TIME:
            logging.warning(f"{message.from_user.id} has waited at least {BAN_TIME} seconds and can now text again")
            BANNED_USERS.remove(message.from_user.id)
            messages[message.from_user.id] = []
    elif len(messages[message.from_user.id]) == MAX_MESS_THRESHOLD:
        logging.warning(f"MAX_MESS_THRESHOLD ({MAX_MESS_THRESHOLD}) Reached for {message.from_user.id}")
        timestamps = messages.pop(message.from_user.id)
        subtractions = []
        for index, timestamp in enumerate(timestamps):
            if index < MAX_MESS_THRESHOLD - 1:
                subtractions.append(timestamps[index + 1] - timestamp)
            else:
                subtractions.append(timestamp - timestamps[index - 1])
        if all(i <= 1 for i in subtractions):
            logging.warning(f"Flood detected from {message.from_user.id}")
            BANNED_USERS.add(message.from_user.id)
            messages[message.from_user.id] = 'added_on', int(time.time())
        else:
            messages[message.from_user.id] = []
    else:
        messages[message.from_user.id].append(message.date)
