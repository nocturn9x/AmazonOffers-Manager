from .scraper import scrape_random_deal
from pyrogram.errors import RPCError
import logging
import random
import logging
from urllib import parse
from pyrogram import InlineKeyboardMarkup, InlineKeyboardButton
from collections import deque


SCHEDULED = deque()


def send_post(client, choices, channel, scheduled, amzn_code, template=None, buttons_template=None):
    product = scrape_random_deal()
    if product and not scheduled:
        img = product["img"]
        currency = "€"
        name = product["name"]
        old_price = product["oldPrice"]
        new_price = product["newPrice"]
        percentage = product["save"]
        link = product["link"]
        real_link = f"{link}?tag={amzn_code}"
        stars = product["stars"]
        revs = product["reviews"]
        seller = product["seller"]
        if not buttons_template:
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("💰 Acquista ora", url=real_link)]])
        else:
            buttons = []
            for name, url in buttons_template.items():
                buttons.append([InlineKeyboardButton(name, url=url)])
            buttons = InlineKeyboardMarkup(buttons)
        if not template:
            message = ""
            if choices['pic'] == "✅":
                message += f"<a href='{img}'>🔥</a> **Nuova Offerta** 🔥\n\n"
            else:
                message += "🔥 **Nuova Offerta** 🔥\n\n"
            message += f"✔️ __{name}__"
            if choices['text'] == "✅":
                message += f"\n\n◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤\n\n❌ ~~{old_price}{currency}~~ in offerta a `{new_price}{currency}` ✅\n\n🤑 Risparmio del {percentage} 🤑\n\n⭐️ {stars} stelle ⭐\n\n📣 Recensioni: {revs}\n\n📦 Venduto da: {seller}"
            message += f"\n\n🌐 <a href='{real_link}'>Link prodotto</a>\n\n◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤"
        else:
            message = template.format(oldPrice=old_price, newPrice=new_price, name=name, save=percentage, reviewsNum=revs, seller=seller, realLink=real_link, img=img)
        try:
            client.send_message(channel, message, reply_markup=buttons)
        except RPCError as generic_error:
            logging.error(f"Error while sending post in {channel} -> {generic_error}")
    if not product:
        logging.debug("No deals to send!")
    elif scheduled:
        SCHEDULED.append([client, choices, channel, amzn_code, template])
