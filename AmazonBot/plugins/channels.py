from pyrogram import Client, Filters, InlineKeyboardButton, InlineKeyboardMarkup
from ..config import BANNED_USERS
from ..database import querymanager
from pyrogram.errors import FloodWait, exceptions
import logging
import time
import re
from base64 import b64encode as b64enc
from base64 import b64decode as b64dec
import dateparser
from collections import defaultdict


DOING = defaultdict(list)


def query_regex(data):
    return Filters.create(
        lambda flt, query: re.match(data, query.data),
        data=data)


@Client.on_callback_query(query_regex("\-\d+\_.+\_\w+"))
def make_post(_, query):
    message = query
    if message.from_user.first_name:
        name = message.from_user.first_name
    elif message.from_user.username:
        name = message.from_user.username
    else:
        name = "Anonimo"
    channel_id, channel_name, sub = query.data.split("_")
    pro = 'Sì' if sub == 'pro' else 'No'
    channel_name = b64dec(channel_name.encode("utf-8")).decode()
    data = (('📸 Foto: ❌', 'pic_true'), ('✍ Didascalia: ❌', 'text_true',), ('⏰ Programma: ❌', 'schedule_true' if pro == 'Sì'  else 'schedule_false'), ('✅ Procedi', 'post_complete'), ('⬅️ Indietro', 'back_start'))
    buttons = []
    for text, callback in data:
        if not callback.startswith("schedule") and callback not in ("back_start", "post_complete"):
            callback += "_"
            callback += "pro" if pro == 'Sì' else 'free'
        buttons.append([InlineKeyboardButton(text, callback_data=callback)])
    buttons = InlineKeyboardMarkup(buttons)
    try:
        query.edit_message_text(f"**AmazonOffers Manager - Crea Post**\n\nQui puoi rivedere e programmare un post nel canale\n\n📣 Canale: {channel_name}\n🆔 ID: `{channel_id}`\n⭐️ Pro: {pro}\n\n🗺 **Legenda** 🗺\n\nFoto: Se impostato, allega la foto del prodotto al post\n\nDidascalia: Se impostato, allega una breve descrizione del prodotto al post\n\nProgramma: Programma l'invio del post, solo per utenti PRO\n\n__Il prodotto oggetto del post sarà casuale, scelto tra le offerte giornaliere disponibili__", reply_markup=buttons)
    except exceptions.bad_request_400.MessageNotModified as exc:
        logging.error(f"Error in chat with {name} [{query.from_user.id}] -> {exc}")
    except FloodWait as fw:
        logging.error(
            f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
        time.sleep(fw.x)


@Client.on_callback_query(query_regex("post_complete"))
def on_post_complete(client, query):
    message = query
    if message.from_user.first_name:
        name = message.from_user.first_name
    elif message.from_user.username:
        name = message.from_user.username
    else:
        name = "Anonimo"
    choices = {}
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("✅ Conferma", callback_data='confirm_choices'), InlineKeyboardButton('⬅️ Annulla', callback_data='back_start')]])
    for button in query.message.reply_markup.inline_keyboard:
        button = button[0]
        if button.callback_data == "schedule_reset":
            choices["schedule"] = "✅"
            DOING[query.from_user.id].append(True)
        else:
            DOING[query.from_user.id].append(None)
            choices["schedule"] = "❌"
        if button.callback_data == "pic_false":
            choices["pic"] = "❌"
            DOING[query.from_user.id].append(None)
        else:
            choices["pic"] = "✅"
            DOING[query.from_user.id].append(True)
        if button.callback_data == "text_false":
            choices["text"] = "❌"
            DOING[query.from_user.id].append(None)
        else:
            choices["text"] = "✅"
            DOING[query.from_user.id].append(True)
    try:
        query.edit_message_text(f"**AmazonOffers Manager - Conferma Post**\n\nRivedi le informazioni sul post e premi conferma, altrimenti premi annulla per tornare al menù principale\n\n📸 Foto: {choices['pic']}\n✍ Didascalia: {choices['text']}\n⏰ Programma: {choices['schedule']}", reply_markup=buttons)
    except exceptions.bad_request_400.MessageNotModified as exc:
        logging.error(f"Error in chat with {name} [{query.from_user.id}] -> {exc}")
    except FloodWait as fw:
        logging.error(
            f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
        time.sleep(fw.x)


@Client.on_callback_query(query_regex("schedule_false"))
def not_pro_user(_, query):
    message = query
    if message.from_user.first_name:
        name = message.from_user.first_name
    elif message.from_user.username:
        name = message.from_user.username
    else:
        name = "Anonimo"
    try:
        query.answer("Non sei un utente pro!")
    except FloodWait as fw:
        logging.error(
            f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
        time.sleep(fw.x)


@Client.on_callback_query(query_regex("schedule_reset"))
def set_schedule_false(_, query):
    pro = "Sì"
    message = query
    if message.from_user.first_name:
       name = message.from_user.first_name
    elif message.from_user.username:
        name = message.from_user.username
    else:
        name = "Anonimo"
    callback = "schedule_true"
    data = InlineKeyboardButton('⏰ Programma: ❌', callback_data=callback)
    buttons = []
    for button in query.message.reply_markup.inline_keyboard:
        if button[0].callback_data == "schedule_reset":
            buttons.append([data])
        else:
            buttons.append(button)
    buttons = InlineKeyboardMarkup(buttons)
    try:
        query.edit_message_reply_markup(buttons)
    except FloodWait as fw:
        logging.error(
            f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
        time.sleep(fw.x)
    except exceptions.bad_request_400.MessageNotModified as exc:
        logging.error(f"Error in chat with {name} [{query.from_user.id}] -> {exc}")


@Client.on_callback_query(query_regex("pic_true\_\w+"))
def set_pic_true(_, query):
    pro = "Sì" if query.data.split("_")[-1] == "pro" else "No"
    message = query
    if message.from_user.first_name:
        name = message.from_user.first_name
    elif message.from_user.username:
        name = message.from_user.username
    else:
        name = "Anonimo"
    callback = "pic_false" + "_"
    callback += "pro" if pro == 'Sì' else 'free'
    data = InlineKeyboardButton('📸 Foto: ✅', callback_data=callback)
    buttons = []
    for button in query.message.reply_markup.inline_keyboard:
        if button[0].callback_data.startswith("pic_true"):
            buttons.append([data])
        else:
            buttons.append(button)
    buttons = InlineKeyboardMarkup(buttons)
    try:
        query.edit_message_reply_markup(buttons)
    except FloodWait as fw:
        logging.error(
            f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
        time.sleep(fw.x)
    except exceptions.bad_request_400.MessageNotModified as exc:
        logging.error(f"Error in chat with {name} [{query.from_user.id}] -> {exc}")


@Client.on_callback_query(query_regex("pic_false\_\w+"))
def set_pic_false(_, query):
    pro = "Sì" if query.data.split("_")[-1] == "pro" else "No"
    message = query
    if message.from_user.first_name:
        name = message.from_user.first_name
    elif message.from_user.username:
        name = message.from_user.username
    else:
        name = "Anonimo"
    callback = "pic_true" + "_"
    callback += "pro" if pro == 'Sì' else 'free'
    data = InlineKeyboardButton('📸 Foto: ❌', callback_data=callback)
    buttons = []
    for button in query.message.reply_markup.inline_keyboard:
        if button[0].callback_data.startswith("pic_false"):
            buttons.append([data])
        else:
            buttons.append(button)
    buttons = InlineKeyboardMarkup(buttons)
    try:
        query.edit_message_reply_markup(buttons)
    except FloodWait as fw:
        logging.error(
            f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
        time.sleep(fw.x)
    except exceptions.bad_request_400.MessageNotModified as exc:
        logging.error(f"Error in chat with {name} [{query.from_user.id}] -> {exc}")


@Client.on_callback_query(query_regex("text_true\_\w+"))
def set_text_true(_, query):
    pro = "Sì" if query.data.split("_")[-1] == "pro" else "No"
    message = query
    if message.from_user.first_name:
       name = message.from_user.first_name
    elif message.from_user.username:
        name = message.from_user.username
    else:
        name = "Anonimo"
    callback = "text_false" + "_"
    callback += "pro" if pro == 'Sì' else 'free'
    data = InlineKeyboardButton('✍ Didascalia: ✅', callback_data=callback)
    buttons = []
    for button in query.message.reply_markup.inline_keyboard:
        if button[0].callback_data.startswith("text_true"):
            buttons.append([data])
        else:
            buttons.append(button)
    buttons = InlineKeyboardMarkup(buttons)
    try:
        query.edit_message_reply_markup(buttons)
    except FloodWait as fw:
        logging.error(
            f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
        time.sleep(fw.x)
    except exceptions.bad_request_400.MessageNotModified as exc:
        logging.error(f"Error in chat with {name} [{query.from_user.id}] -> {exc}")



@Client.on_callback_query(query_regex("text_false\_\w+"))
def set_text_false(_, query):
    pro = "Sì" if query.data.split("_")[-1] == "pro" else "No"
    message = query
    if message.from_user.first_name:
       name = message.from_user.first_name
    elif message.from_user.username:
        name = message.from_user.username
    else:
        name = "Anonimo"
    callback = "text_true" + "_"
    callback += "pro" if pro == 'Sì' else 'free'
    data = InlineKeyboardButton('✍ Didascalia: ❌', callback_data=callback)
    buttons = []
    for button in query.message.reply_markup.inline_keyboard:
        if button[0].callback_data.startswith("text_false"):
            buttons.append([data])
        else:
            buttons.append(button)
    buttons = InlineKeyboardMarkup(buttons)
    try:
        query.edit_message_reply_markup(buttons)
    except FloodWait as fw:
        logging.error(
            f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
        time.sleep(fw.x)
    except exceptions.bad_request_400.MessageNotModified as exc:
        logging.error(f"Error in chat with {name} [{query.from_user.id}] -> {exc}")


@Client.on_callback_query(query_regex("schedule_true"))
def set_schedule_true(_, query):
    pro = "Sì"
    message = query
    if message.from_user.first_name:
       name = message.from_user.first_name
    elif message.from_user.username:
        name = message.from_user.username
    else:
        name = "Anonimo"
    callback = "schedule_reset"
    data = InlineKeyboardButton('⏰ Programma: ✅', callback_data=callback)
    buttons = []
    for button in query.message.reply_markup.inline_keyboard:
        if button[0].callback_data == "schedule_true":
            buttons.append([data])
        else:
            buttons.append(button)
    buttons = InlineKeyboardMarkup(buttons)
    try:
        query.edit_message_reply_markup(buttons)
    except FloodWait as fw:
        logging.error(
            f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
        time.sleep(fw.x)
    except exceptions.bad_request_400.MessageNotModified as exc:
        logging.error(f"Error in chat with {name} [{query.from_user.id}] -> {exc}")





@Client.on_message(Filters.private & ~BANNED_USERS & Filters.command("post"))
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
        for channel_id, channel_name, sub in channels:
            if len(channel_name) > 15:
                channel_name = channel_name[0:20] + "..."
            data = f"{channel_id}_{b64enc(channel_name.encode()).decode()}_{sub}"
            if len(data) > 64:
                data = f"{channel_id}_{b64enc(channel_name[0:10].encode()).decode()}_{sub}"
            buttons.append([InlineKeyboardButton(text=channel_name, callback_data=data)])
        try:
            client.send_message(message.chat.id, response, reply_markup=InlineKeyboardMarkup(buttons))
        except FloodWait as fw:
            logging.error(
                f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
            time.sleep(fw.x)
