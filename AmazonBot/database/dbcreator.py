import logging
import sqlite3.dbapi2 as sqlite3
import os
from ..config import CREATE_QUERY, TEST_QUERY


def load_database(path):
    DB_INSTANCE = sqlite3.connect(path)
    cursor = DB_INSTANCE.cursor()
    try:
        cursor.execute(TEST_QUERY)
    except sqlite3.OperationalError as e:
        logging.error(f"Something went wrong while dealing with the database! More info: {e}")
        cursor.close()
        exit(e)
    logging.info("Done! Database was loaded succesfully!")
    cursor.close()


def create_database(path: str):
    if not os.path.isfile(path):
        new = True
        logging.info(f"Creating new database at {path}")
    else:
        new = False
        logging.info(f"Loading database from {path}")
    DB = sqlite3.connect(path)
    if new:
        cursor = DB.cursor()
        try:
            cursor.execute(CREATE_QUERY)
            DB.commit()
            cursor.close()
        except sqlite3.OperationalError as e:
            logging.error(f"Something went wrong while creating the database! More info: {e}")
            cursor.close()
            exit(e)
        logging.debug(f"Succesfully ran CREATE_QUERY on database at {path}, preparing to load")
    load_database(path)
