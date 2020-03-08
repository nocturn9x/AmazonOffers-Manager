import sqlite3.dbapi2 as sqlite3
import json
from ..config import DB_PATH
import logging


def register_channel(channel_id, admins, subscription, affiliate_code, channel_name):
    DB = sqlite3.connect(DB_PATH)
    cursor = DB.cursor()
    admins = json.dumps({"admins": admins})
    try:
        logging.info(f"Inserting: {channel_id}, {channel_name}, {admins}, {subscription}, {affiliate_code}")
        cursor.execute("INSERT INTO channels(channel, channel_name, admins, subscription, amzn_code) VALUES(?, ?, ?, ?, ?);", (channel_id, channel_name, admins, subscription, affiliate_code))
    except sqlite3.IntegrityError:
        logging.info("Channel already exists, replacing old values...")
        try:
            cursor.execute("UPDATE channels SET channel_name = ?, admins = ?, amzn_code = ? WHERE channel = ?", (channel_name, admins, affiliate_code, channel_id))
        except sqlite3.Error as err:
            logging.error(f"Error while inserting! {err}")
        else:
            logging.info("Done!")
    except sqlite3.Error as err:
        logging.error(f"Error while inserting! {err}")
    else:
        logging.info("Done!")
    DB.commit()
    cursor.close()


def retrieve_channels(user_id):
    channels = []
    DB = sqlite3.connect(DB_PATH)
    cursor = DB.cursor()
    try:
        query = cursor.execute("SELECT * FROM channels")
    except sqlite3.Error as err:
        logging.error(f"Error while retrieving! {err}")
    else:
        for channel_id, name, json_data, sub, code, _, _ in query.fetchall():
            if user_id in json.loads(json_data)["admins"]:
                channels.append((channel_id, name, sub, code))
    return channels


def add_admin(user_id, super: bool = False):
    DB = sqlite3.connect(DB_PATH)
    cursor = DB.cursor()
    try:
        cursor.execute("INSERT INTO admins(id, super_user) VALUES(?, ?)", (user_id, 0 if not super else 1))
    except sqlite3.Error as err:
        logging.error(f"Error while inserting admin -> {err}")
    else:
        DB.commit()


def remove_admin(user_id):
    DB = sqlite3.connect(DB_PATH)
    cursor = DB.cursor()
    try:
        exists = cursor.execute("SELECT * FROM admins WHERE id = ?", (user_id, ))
    except sqlite3.Error as err:
        logging.error(f"Error while removing admin -> {err}")
    else:
        if exists.fetchall():
            try:
                cursor.execute("DELETE FROM admins WHERE id = ?", (user_id, ))
            except sqlite3.Error as err:
                logging.error(f"Error while removing admin -> {err}")
            else:
                DB.commit()
                return True
        else:
            return False


def add_pro(id):
    DB = sqlite3.connect(DB_PATH)
    cursor = DB.cursor()
    try:
        cursor.execute("UPDATE channels SET subscription = 'pro'  WHERE channel = ?", (id, ))
    except sqlite3.Error as err:
        logging.error(f"Error while updating subscription for {id} -> {err}")
    else:
        DB.commit()
        return True


def remove_pro(id):
    DB = sqlite3.connect(DB_PATH)
    cursor = DB.cursor()
    try:
        cursor.execute("UPDATE channels SET subscription = 'free' WHERE channel = ?", (id, ))
    except sqlite3.Error as err:
        logging.error(f"Error while updating subscription for {id} -> {err}")
    else:
        DB.commit()
        return True


def get_admins():
    DB = sqlite3.connect(DB_PATH)
    cursor = DB.cursor()
    try:
        query = cursor.execute("SELECT * from ADMINS")
    except sqlite3.Error as err:
        logging.error(f"Error while retrieving admins! -> {err}")
    else:
        return query.fetchall()


def save_post(post, channel):
    DB = sqlite3.connect(DB_PATH)
    cursor = DB.cursor()
    try:
        query = cursor.execute("UPDATE channels SET post_template = ? WHERE channel = ?", (post, channel))
    except sqlite3.Error as err:
        logging.error(f"Error while updating post template for {channel}! -> {err}")
    DB.commit()


def save_buttons(buttons, channel):
    DB = sqlite3.connect(DB_PATH)
    cursor = DB.cursor()
    try:
        query = cursor.execute("UPDATE channels SET buttons_template = ? WHERE channel = ?", (buttons, channel))
    except sqlite3.Error as err:
        logging.error(f"Error while retrieving buttons template for {channel}! -> {err}")
    DB.commit()


def get_buttons(channel):
    DB = sqlite3.connect(DB_PATH)
    cursor = DB.cursor()
    try:
        query = cursor.execute("SELECT buttons_template FROM channels WHERE channel = ?", (channel, ))
    except sqlite3.Error as err:
        logging.error(f"Error while retrieving buttons template template for {channel}! -> {err}")
    return query.fetchall()


def get_post(channel):
    DB = sqlite3.connect(DB_PATH)
    cursor = DB.cursor()
    try:
        query = cursor.execute("SELECT post_template FROM channels WHERE channel = ?", (channel, ))
    except sqlite3.Error as err:
        logging.error(f"Error while retrieving post template template for {channel}! -> {err}")
    return query.fetchall()
