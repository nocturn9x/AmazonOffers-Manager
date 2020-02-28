from pyrogram import Filters, InlineKeyboardMarkup, InlineKeyboardButton, Client
from pyrogram.errors import *
import time
import logging
from ..config import BANNED_USERS


def query_filter(data):
    return Filters.create(
        lambda flt, query: flt.data == query.data,
        data=data)


@Client.on_callback_query(query_filter("config_second_step"))
def on_config_step_button_press(_, query):
    user = query.from_user
    user_id = user.id
    message = query
    if message.from_user.first_name:
        name = message.from_user.first_name
    elif message.from_user.username:
        name = message.from_user.username
    else:
        name = "Anonimo"
    try:
        query.edit_message_text("Perfetto, ora inoltra (non copia!) un messaggio dal canale che hai scelto per completare la procedura")
    except exceptions.bad_request_400.MessageNotModified as exc:
        logging.error(f"Error in chat with {name} [{query.from_user.id}] -> {exc}")
    except FloodWait as fw:
        logging.error(
            f"Error in chat with {name} [{user_id}] -> FloodWait! Sleeping for {fw.x} seconds...")
        time.sleep(fw.x)


@Client.on_callback_query(query_filter("config_ready"))
def on_config_ready_button_press(_, query):
    user = query.from_user
    user_id = user.id
    message = query
    if message.from_user.first_name:
        name = message.from_user.first_name
    elif message.from_user.username:
        name = message.from_user.username
    else:
        name = "Anonimo"
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("✅ Procedi", callback_data="config_second_step")]])
    try:
        query.edit_message_text("**AmazonOffers Manager - Configurazione**\n\nEcco cosa devi fare:\n- Aggiungi @AmazonOffersBot come amministratore nel canale che vuoi configurare\n- Assicurati che il bot sia autorizzato a scrivere messaggi\n- DOPO aver aggiunto il bot come amministratore, inoltra (non copia!) un messaggio dal canale per completare la procedura\n\nUna volta che hai aggiunto il bot come amministratore e forniti i permessi necessari, premi il bottone qui sotto", reply_markup=keyboard)
    except exceptions.bad_request_400.MessageNotModified as exc:
        logging.error(f"Error in chat with {name} [{query.from_user.id}] -> {exc}")
    except FloodWait as fw:
        logging.error(
            f"Error in chat with {name} [{user_id}] -> FloodWait! Sleeping for {fw.x} seconds...")
        time.sleep(fw.x)


@Client.on_message(Filters.command("config") & Filters.private & ~BANNED_USERS & ~Filters.forwarded)
def on_config(client, message):
    if message.from_user.first_name:
        name = message.from_user.first_name
    elif message.from_user.username:
        name = message.from_user.username
    else:
        name = "Anonimo"
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("✅ Sono pronto", callback_data="config_ready")]])
    try:
        client.send_message(message.chat.id, f"Ok, ti guiderò nella procedura di configurazione del bot\nQuando sei pronto per iniziare, premi il bottone qui sotto", reply_markup=buttons)
    except FloodWait as fw:
        logging.error(f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
        time.sleep(fw.x)


@Client.on_message(Filters.forwarded & Filters.private & ~BANNED_USERS)
def on_channel_forwarded(client, message):
    forward = message.forward_from_chat
    if message.from_user.first_name:
        name = message.from_user.first_name
    elif message.from_user.username:
        name = message.from_user.username
    else:
        name = "Anonimo"
    if not forward:
        try:
            client.send_message(message.chat.id, "Sembra che il messaggio che hai inoltrato non provenga da un canale, riprova!")
        except FloodWait as fw:
            logging.error(
                f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
            time.sleep(fw.x)
    else:
        try:
            me = client.get_chat_member(forward.id, "me")
        except FloodWait as fw:
            logging.error(
                f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
            time.sleep(fw.x)
        else:
            if not me.status == "administrator":
                try:
                    client.send_message(message.chat.id,
                                        "Non sono admin nel canale selezionato, controlla i permessi!")
                except FloodWait as fw:
                    logging.error(
                        f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
                    time.sleep(fw.x)
            elif not me.can_post_messages:
                try:
                    client.send_message(message.chat.id,
                                        "Non posso scrivere messaggi nel canale selezionato, controlla i permessi!")
                except FloodWait as fw:
                    logging.error(
                        f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
                    time.sleep(fw.x)
            else:
                try:
                    client.send_message(message.chat.id, "✅ Configurazione completata!")
                    logging.info(f"New channel registered: '{forward.title}' [{forward.id}] ")
                except FloodWait as fw:
                    logging.error(
                        f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
                    time.sleep(fw.x)
