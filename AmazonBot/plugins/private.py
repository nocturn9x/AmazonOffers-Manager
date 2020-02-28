from pyrogram import Filters, InlineKeyboardMarkup, InlineKeyboardButton, Client
from pyrogram.errors import *
import time
import logging
from ..config import BANNED_USERS


def query_filter(data):
    return Filters.create(
        lambda flt, query: flt.data == query.data,
        data=data)


@Client.on_callback_query(query_filter("help"))
def on_help_button_press(_, query):
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("◀ Indietro", callback_data="back_start")], ])
    message = query
    if message.from_user.first_name:
        name = message.from_user.first_name
    elif message.from_user.username:
        name = message.from_user.username
    else:
        name = "Anonimo"
    try:
        query.edit_message_text("**AmazonOffers Manager - Cos'è?**\n\nAmazonOffers Manager è un bot pensato per semplificare la gestione dei canali di offerte Amazon, solo in italia, che ti permette di inserire il tuo link affiliato Amazon nei post, programmare messaggi, impostare l'immagine dei prodotti e molto altro ancora!\nQuando sei pronto per iniziare, invia /config e ti guiderò nella procedura di configurazione del bot", reply_markup=buttons)
    except exceptions.bad_request_400.MessageNotModified as exc:
        logging.error(f"Error in chat with {name} [{query.from_user.id}] -> {exc}")
    except FloodWait as fw:
        logging.error(
            f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
        time.sleep(fw.x)


@Client.on_callback_query(query_filter("back_start"))
def on_back_button_press(_, query):
    message = query
    if message.from_user.first_name:
        name = message.from_user.first_name
    elif message.from_user.username:
        name = message.from_user.username
    else:
        name = "Anonimo"
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton(url="telegram.me/isgiambyy", text="💻 Sviluppatore"), InlineKeyboardButton(text="❓ Cos'è?", callback_data=f"help")]])
    try:
        query.edit_message_text(f"Ciao [{name}](tg://user?id={query.from_user.id})! Sono un bot creato per gestire canali di offerte Amazon, con tante funzioni interessanti!\n\nPremi i bottoni qui sotto per saperne di più, o invia /config se sei pronto ad iniziare", reply_markup=buttons)
    except exceptions.bad_request_400.MessageNotModified as exc:
        logging.error(f"Error in chat with {name} [{query.from_user.id}] -> {exc}")
    except FloodWait as fw:
        logging.error(
            f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
        time.sleep(fw.x)


@Client.on_message(Filters.command("start") & Filters.private & ~Filters.forwarded & ~BANNED_USERS)
def on_start(client, message):
    msg = message
    if message.from_user.first_name:
        name = message.from_user.first_name
    elif message.from_user.username:
        name = message.from_user.username
    else:
        name = "Anonimo"
    user_id = msg.from_user.id
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton(url="telegram.me/isgiambyy", text="💻 Sviluppatore"), InlineKeyboardButton(text="❓ Cos'è?", callback_data=f"help")]])
    try:
        client.send_message(msg.chat.id, f"Ciao [{name}](tg://user?id={user_id})! Sono un bot creato per gestire canali di offerte Amazon, con tante funzioni interessanti!\n\nPremi i bottoni qui sotto per saperne di più, o invia /config se sei pronto ad iniziare", reply_markup=buttons)
    except FloodWait as fw:
        logging.error(
            f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
        time.sleep(fw.x)


