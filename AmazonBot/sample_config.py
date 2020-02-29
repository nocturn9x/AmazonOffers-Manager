from pyrogram import Filters

# HTTP Headers for the scraper module
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}  # We pretend to be a legitimate browser

# API Endpoints to fetch deals and search products
API_OFFERS_URL = "https://nocturn9x.space/amazon/deals.php"
API_SEARCH_URL = "https://nocturn9x.space/amazon/search.php?name={which}"

# Logging config: (format, datefmt)
LOGGING_CONFIG = ("%d/%m/%Y %H:%M:%S %p", "[%(levelname)s] [%(asctime)s)]: %(message)s", 20)

API_ID = # REPLACE WITH YOUR API ID (INTEGER)
API_HASH = "API HASH HERE"
WORKERS_NUM = 10  # Number of worker threads of the bot
SESSION_NAME = "AmazonOffers"
BOT_TOKEN = "BOT TOKEN HERE"
PLUGINS_ROOT = "AmazonBot/plugins"
MAX_MESS_THRESHOLD = 7  # Max. number of messages to calculate flood rate
BAN_TIME = 60   # The min. duration of the flood ban, in seconds
OWNERS_LIST = []  # List of users that are super-users and can add other admins in the database

# DANGER ZONE - DO NOT CHANGE ANYTHING BELOW THIS LINE - SHARED VARIABLES

DB_PATH = ""
BANNED_USERS = Filters.chat()
CREATE_QUERY = """CREATE TABLE channels(channel INTEGER NOT NULL PRIMARY KEY,
                                        admins TEXT NULL,
                                        subscription TEXT NULL DEFAULT 'free',
                                        amzn_code TEXT NOT NULL);
                  CREATE TABLE admins(user_id INTEGER NOT NULL PRIMARY KEY,
                                      super_user INTEGER NOT NULL DEFAULT 0);"""
TEST_QUERY = """SELECT * FROM channels WHERE channel != 1;"""
