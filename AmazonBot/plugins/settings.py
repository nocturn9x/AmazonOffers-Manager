from pyrogram import Client, Filters, InlineKeyboardButton, InlineKeyboardMarkup
from ..database import querymanager
import time
from .channels import query_regex
from base64 import b64encode as b64enc
from base64 import b64decode as b64dec
from pyrogram.errors import FloodWait, exceptions
from collections import defaultdict
from ..config import URI_REGEX
from .antiflood import BANNED_USERS
import json
import re


DOING = defaultdict(lambda: ([None, None, None]))

def flt_setting(which):
    return Filters.create(
    lambda flt, message: DOING[message.from_user.id][0] == which,
    data=which)

Filters.setting = flt_setting


@Client.on_callback_query(query_regex("choose_channel_settings"))
def on_settings_button_press(client, query):
    message = query
    channels = querymanager.retrieve_channels(message.from_user.id)
    if message.from_user.first_name:
        name = message.from_user.first_name
    elif message.from_user.username:
        name = message.from_user.username
    else:
        name = "Anonimo"
    if not channels:
        try:
            client.send_message(message.from_user.id, "❌ Errore, non c'è nessun canale registrato a tuo nome!\nRicorda che se hai appena registrato un canale, potrebbero occorrere un paio di minuti prima che esso venga mostrato qui")
        except FloodWait as fw:
            logging.error(
                f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
            time.sleep(fw.x)
    else:
        response = "**AmazonOffers Manager - Seleziona Canale**\n\nUtilizzando i bottoni qui sotto, scegli per quale canale desideri modificare le impostazioni"
        buttons = []
        for channel_id, channel_name, sub, amzn_code in channels:
            if len(channel_name) > 15:
                channel_name = channel_name[0:20] + "..."
            data = f"1_{channel_id}_{b64enc(channel_name.encode()).decode()}_{sub}"
            if len(data) > 64:
                data = f"1_{channel_id}_{b64enc(channel_name[0:10].encode()).decode()}_{sub}"
            buttons.append([InlineKeyboardButton(text=channel_name, callback_data=data)])
        buttons.append([InlineKeyboardButton("⬅️ Indietro", callback_data="back_start")])
        try:
            query.edit_message_text(response, reply_markup=InlineKeyboardMarkup(buttons))
        except exceptions.bad_request_400.MessageNotModified as exc:
            logging.error(f"Error in chat with {name} [{query.from_user.id}] -> {exc}")
        except FloodWait as fw:
            logging.error(
                f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
            time.sleep(fw.x)


@Client.on_callback_query(query_regex("1\_\-\d+\_.+\_\w+"))
def on_channel_chosen(client, query):
    message = query
    if message.from_user.first_name:
        name = message.from_user.first_name
    elif message.from_user.username:
        name = message.from_user.username
    else:
        name = "Anonimo"
    _, channel_id, channel_name, sub = query.data.split("_")
    pro = "Sì" if sub == 'pro' else 'No'
    if pro == 'Sì':
        channel_name = b64dec(channel_name.encode()).decode()
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("✍ Aspetto Post", callback_data=f"post_{channel_id}"), InlineKeyboardButton("⌨ Crea tastiere", callback_data=f"keyb_{channel_id}")], [InlineKeyboardButton("⬅️ Indietro", callback_data="choose_channel_settings")]])
        try:
            query.edit_message_text(f"**AmazonOffers Manager - Impostazioni**\n\nBenvenuto nel menù impostazioni, premi uno dei bottoni qui sotto per continuare\n\n📣 Canale: {channel_name}\n🆔 ID: `{channel_id}`\n⭐ Pro: {pro}", reply_markup=buttons)
        except exceptions.bad_request_400.MessageNotModified as exc:
            logging.error(f"Error in chat with {name} [{query.from_user.id}] -> {exc}")
        except FloodWait as fw:
            logging.error(
                f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
            time.sleep(fw.x)
    else:
        try:
            query.answer("Non sei PRO!")
        except FloodWait as fw:
            logging.error(
                f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
            time.sleep(fw.x)


@Client.on_callback_query(query_regex("post_\-\d+"))
def change_template_menu(_, query):
    message = query
    _, channel_id = query.data.split("_")
    if message.from_user.first_name:
        name = message.from_user.first_name
    elif message.from_user.username:
        name = message.from_user.username
    else:
        name = "Anonimo"
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("❌ Annulla", callback_data="back_start")]])
    try:
        query.edit_message_text("**AmazonOffers Manager - Impostazioni**\n\nQui puoi modificare l'aspetto dei post sul canale, invia ora il nuovo messaggio che vuoi impostare.\n**Puoi usare i seguenti placeholder**:\n\n`{oldPrice}`: Il prezzo del prodotto prima dello sconto\n\n`{newPrice}`: Il prezzo scontato\n\n`{name}`: Il nome del prodotto\n\n`{save}`: La % di sconto applicata\n\n`{reviewsNum}`: Il numero di recensioni\n\n`{seller}`: Il nome del venditore\n\n`{realLink}`: Il link al prodotto (contiene il tuo ID affiliato)\n\n`{img}`: Link all'immagine del prodotto\n\n`{starsNum}`: Il numero di stelle di un prodotto (su 5)\n\n**N.B.** Consigliamo di inserire img all'interno di un tag HTML come in questo esempio\n\n`<a href='{realLink}'>💵</a>`\n\n⚠️ Se vuoi inserire del testo tra {}, dovrai utilizzare 2 coppie di parentesi graffe, così: `{{testo}}`, altrimenti il bot non potrà inviare post nel canale!", reply_markup=buttons, parse_mode="md")
        DOING[query.from_user.id] = ["SET_POST", int(time.time()), channel_id]
    except exceptions.bad_request_400.MessageNotModified as exc:
        logging.error(f"Error in chat with {name} [{query.from_user.id}] -> {exc}")
    except FloodWait as fw:
        logging.error(
                f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
        time.sleep(fw.x)


@Client.on_callback_query(query_regex("keyb_\-\d+"))
def change_keyb_menu(_, query):
    message = query
    _, channel_id = query.data.split("_")
    if message.from_user.first_name:
        name = message.from_user.first_name
    elif message.from_user.username:
        name = message.from_user.username
    else:
        name = "Anonimo"
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("❌ Annulla", callback_data="back_start")]])
    try:
        query.edit_message_text("**AmazonOffers Manager - Impostazioni**\n\nQui puoi impostare una tastiera che apparirà sotto ai tuoi post\n\nInvia ora la tastiera che desideri rispettando questo pattern\nTesto del bottone - url\n\nInvia una coppia testo-messaggio per riga", reply_markup=buttons)
        DOING[query.from_user.id] = ["SET_KEYB", int(time.time()), channel_id]
    except exceptions.bad_request_400.MessageNotModified as exc:
        logging.error(f"Error in chat with {name} [{query.from_user.id}] -> {exc}")
    except FloodWait as fw:
        logging.error(
                f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
        time.sleep(fw.x)



@Client.on_message(Filters.setting("SET_POST") & Filters.private & Filters.text & ~BANNED_USERS)
def change_post_handler(client, message):
    if message.from_user.first_name:
        name = message.from_user.first_name
    elif message.from_user.username:
        name = message.from_user.username
    else:
        name = "Anonimo"
    try:
        client.send_message(message.from_user.id, "✅ Fatto! Template salvato")
    except FloodWait as fw:
        logging.error(
                f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
        time.sleep(fw.x)
        del DOING[message.from_user.id]

    template = message.text
    querymanager.save_post(template, DOING[message.from_user.id][2])
    del DOING[message.from_user.id]


@Client.on_message(Filters.setting("SET_KEYB") & Filters.private & Filters.text & ~BANNED_USERS)
def change_buttons_handler(client, message):
    if message.from_user.first_name:
        name = message.from_user.first_name
    elif message.from_user.username:
        name = message.from_user.username
    else:
        name = "Anonimo"
    valid = True
    keyboard_data = {}
    raw_data = message.text.splitlines()
    for line in raw_data:
        print(line)
        if len(line.split("-")) == 2:
            name, url = line.split("-")
            if not re.match(URI_REGEX, url.strip()):
                valid = False
                break
            else:
                keyboard_data[name] = url.strip()
        else:
            valid = False
    if valid:
        try:
            client.send_message(message.from_user.id, "✅ Fatto! Tastiera salvata")
            querymanager.save_buttons(json.dumps(keyboard_data), DOING[message.from_user.id][2])
        except FloodWait as fw:
            logging.error(
                f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
            time.sleep(fw.x)
        del DOING[message.from_user.id]
    else:
        try:
            client.send_message(message.from_user.id, "❌ Errore: La tastiera fornita non é valida, riprova")
        except FloodWait as fw:
            logging.error(
                f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
            time.sleep(fw.x)


