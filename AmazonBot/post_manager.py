from .scraper import scrape_deals
from pyrogram.errors import RPCError
import logging
import random
import logging
from urllib import parse
from pyrogram import InlineKeyboardMarkup, InlineKeyboardButton


SCHEDULED = list()


def send_post(client, choices, channel, scheduled, amzn_code):
    deals = scrape_deals()
    if deals and not scheduled:
        product = deals[random.randint(0, len(deals) - 1)]
        link = product["link"]
        img = product["img"]
        name = product["name"][:-3]
        currency = product["currency"]
        old_price = product["oldPrice"]
        new_price = product["newPrice"]
        percentage = product["saving"]
        ASIN = parse.urlparse(link).query.split("=")[1]
        real_link = f"https://amazon.it/dp/{ASIN}?tag={amzn_code}"
        message = ""
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("💰 Acquista ora", url=real_link)]])
        if choices['pic'] == "✅":
            message += f"<a href='{img}'>🌏</a> __Nuova Offerta__\n\n"
        else:
            message += "🌏 __Nuova Offerta__\n\n"
        message += f"✔️ **{name}**"
        if choices['text'] == "✅":
            message += f"\n\n◢◤◢◤◢◤◢◤◢◤◢◤◢◤\n💳 ➠ ❌ ~~{old_price} {currency}~~ in offerta a `{new_price} {currency}` ✅\n\n🤑 Risparmio del {percentage} 🤑"
        message += f"\n\n🌐 <a href='{real_link}'>Link prodotto</a>\n◢◤◢◤◢◤◢◤◢◤◢◤◢◤"
        try:
            client.send_message(channel, message, reply_markup=buttons)
        except RPCError as generic_error:
            logging.error(f"Error while sending post in {channel} -> {generic_error}")
    if not deals:
        logging.debug("No deals to send!")
    elif scheduled:
        SCHEDULED.append([client, choices, channel, scheduled, amzn_code])
