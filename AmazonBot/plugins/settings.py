from pyrogram import Client, Filters
from ..database import querymanager
import time
from .channels import query_regex



@Client.on_callback_query(query_regex("choose_channel_settings"))
def on_settings_button_press(client, message):
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
        response = "**AmazonOffers Manager - Seleziona Canale**\n\nUtilizzando i bottoni qui sotto, scegli per quale canale desideri modificare le impostazioni"
        buttons = []
        for channel_id, channel_name, sub, amzn_code in channels:
            if len(channel_name) > 15:
                channel_name = channel_name[0:20] + "..."
            IDS[channel_id] = amzn_code
            data = f"1_{channel_id}_{b64enc(channel_name.encode()).decode()}_{sub}"
            if len(data) > 64:
                data = f"1_{channel_id}_{b64enc(channel_name[0:10].encode()).decode()}_{sub}"
            buttons.append([InlineKeyboardButton(text=channel_name, callback_data=data)])
        try:
            client.send_message(message.chat.id, response, reply_markup=InlineKeyboardMarkup(buttons))
        except FloodWait as fw:
            logging.error(
                f"Error in chat with {name} [{message.from_user.id}] -> FloodWait! Sleeping for {fw.x} seconds...")
            time.sleep(fw.x)

