from pyrogram import Client, Filters
from ..config import ADMINS
from ..database.querymanager import add_admin, remove_admin, add_pro, remove_pro, get_admins
import time



@Client.on_message(Filters.private & Filters.command("admin"))
def pex_admin(client, message):
    admins = []
    for admin in get_admins():
        if admin[1]:
            admins.append(admin[0])
    if message.from_user.id in admins + ADMINS:
        if len(message.command) >= 2:
            if message.command[1].isdigit():
                user_id = int(message.command[1])
                if user_id > 0:
                    super = False
                    if len(message.command) == 3:
                        if message.command[2] == 'super':
                            super = True
                    add_admin(user_id, super)
                    try:
                        client.send_message(message.chat.id, f"✅ Fatto! Ho aggiunto `{user_id}` alla lista amministratori")
                    except FloodWait as err:
                        time.sleep(fw.x)


@Client.on_message(Filters.private & Filters.command("depex"))
def depex_admin(client, message):
    admins = []
    for admin in get_admins():
        if admin[1]:
            admins.append(admin[0])
    if message.from_user.id in admins + ADMINS:
        if len(message.command) == 2:
            if message.command[1].isdigit():
                user_id = int(message.command[1])
                if user_id > 0:
                    remove_admin(user_id)
                    try:
                        client.send_message(message.chat.id, f"✅ Fatto! Ho rimosso `{user_id}` dalla lista amministratori")
                    except FloodWait as err:
                        time.sleep(fw.x)

@Client.on_message(Filters.private & Filters.command("pro"))
def make_pro(client, message):
    admins = []
    for admin in get_admins():
        admins.append(admin[0])
    if message.from_user.id in admins + ADMINS:
        if len(message.command) == 2:
            if len(message.command) >= 2:
                if message.command[1][1:].isdigit():
                    user_id = int(message.command[1])
                    if user_id < 0:
                        add_pro(user_id)
                    try:
                       client.send_message(message.chat.id, f"✅ Fatto! Ora il canale con ID `{user_id}` é pro!")
                    except FloodWait as err:
                       time.sleep(fw.x)


@Client.on_message(Filters.private & Filters.command("unpro"))
def unmake_pro(client, message):
    admins = []
    for admin in get_admins():
        admins.append(admin[0])
    if message.from_user.id in admins + ADMINS:
        if len(message.command) == 2:
            if len(message.command) >= 2:
                if message.command[1][1:].isdigit():
                    user_id = int(message.command[1])
                    if user_id < 0:
                        remove_pro(user_id)
                        try:
                            client.send_message(message.chat.id, f"✅ Fatto! Ora il canale con ID `{user_id}` non é più pro!")
                        except FloodWait as err:
                           time.sleep(fw.x)

