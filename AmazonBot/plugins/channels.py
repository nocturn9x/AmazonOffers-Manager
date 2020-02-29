from pyrogram import Client, Filters, InlineKeyboardButton, InlineKeyboardMarkup
from ..config import BANNED_USERS
from ..database import querymanager
from pyrogram.errors import FloodWait
import logging
import time


@Client.on_message(Filters.private & ~BANNED_USERS & Filters.command("channels"))
def on_channels(client, message):
    channels = querymanager.retrieve_channels(message.from_user.id)
    if message.from_user.first_name:
        name = message.from_user.first_name
    elif message.from_user.username:
        name = message.from_user.username
    else:
        name = "Anonimo"
    if not channels:
        try:
            client.send_message(message.chat.id, "❌ Errore, non c'è nessun canale registrato a tuo nome!\nRicorda che se hai appena registrato un canale, potrebbero occorrere un paio di minuti prima che esso venga mostrato qui")
        except FloodWait as fw:
            logging.error(
                f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
            time.sleep(fw.x)
    else:
        response = "**AmazonOffers Manager - Seleziona Canale**\n\nUtilizzando i bottoni qui sotto, scegli in quale canale desideri inviare i post"
        buttons = []
        for channel_id, channel_name in channels:
            buttons.append([InlineKeyboardButton(text=channel_name, callback_data=str(channel_id))])
        try:
            client.send_message(message.chat.id, response, reply_markup=InlineKeyboardMarkup(buttons))
        except FloodWait as fw:
            logging.error(
                f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
            time.sleep(fw.x)