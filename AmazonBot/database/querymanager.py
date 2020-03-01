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
        DB.commit()
    except sqlite3.IntegrityError:
        logging.info("Channel already exists, replacing old values...")
        try:
            cursor.execute("UPDATE channels SET channel_name = ?, admins = ?, amzn_code = ?", (channel_name, admins, affiliate_code))
        except sqlite3.Error as err:
            logging.error(f"Error while inserting! {err}")
        else:
            logging.info("Done!")
    except sqlite3.Error as err:
        logging.error(f"Error while inserting! {err}")
    else:
        logging.info("Done!")
    cursor.close()


def retrieve_channels(user_id):
    channels = []
    DB = sqlite3.connect(DB_PATH)
    cursor = DB.cursor()
    try:
        query = cursor.execute("SELECT channel, channel_name, admins, subscription, amzn_code from channels")
    except sqlite3.Error as err:
        logging.error(f"Error while retrieving! {err}")
    else:
        for channel_id, name, json_data, sub, code in query.fetchall():
            if user_id in json.loads(json_data)["admins"]:
                channels.append((channel_id, name, sub, code))
    return channels
