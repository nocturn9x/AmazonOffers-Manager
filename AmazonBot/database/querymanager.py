import sqlite3.dbapi2 as sqlite3
import json
from ..config import DB_PATH
import logging


def register_channel(channel_id, admins, subscription, affiliate_code, channel_name):
    print(DB_PATH)
    DB = sqlite3.connect(DB_PATH)
    cursor = DB.cursor()
    admins = json.dumps({"admins": admins})
    try:
        logging.info(f"Inserting: {channel_id}, {admins}, {subscription}, {affiliate_code}")
        cursor.execute("INSERT INTO channels(channel, channel_name, admins, subscription, amzn_code) VALUES(?, ?, ?, ?, ?);", (channel_id, channel_name, admins, subscription, affiliate_code))
        DB.commit()
    except sqlite3.IntegrityError as err:
        try:
            cursor.execute(
    except sqlite3.Error:
        logging.error(f"Error while inserting! {err}")
    cursor.close()
