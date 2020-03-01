import os


# HTTP Headers for the scraper module
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}  # We pretend to be a legitimate browser

# API Endpoints to fetch deals and search products
API_OFFERS_URL = "https://nocturn9x.space/amazon/deals.php"
API_SEARCH_URL = "https://nocturn9x.space/amazon/search.php?name={which}"

# Logging config: (format, datefmt)
LOGGING_CONFIG = ("%d/%m/%Y %H:%M:%S %p", "[%(levelname)s] [%(asctime)s]: %(message)s", 20)

API_ID = 123456
API_HASH = "123456789"
WORKERS_NUM = 10
SESSION_NAME = "AmazonOffers"
BOT_TOKEN = "TOKEN"A
PLUGINS_ROOT = "AmazonBot/plugins"
MAX_MESS_THRESHOLD = 7
BAN_TIME = 60

# DANGER ZONE - DO NOT CHANGE ANYTHING BELOW THIS LINE - SHARED VARIABLES

DB_PATH = os.path.join(os.getcwd(), "users.db")
CREATE_QUERY = """CREATE TABLE channels (channel INTEGER NOT NULL PRIMARY KEY,
                                        channel_name TEXT NOT NULL,
                                        admins TEXT NULL,
                                        subscription TEXT NULL DEFAULT 'free',
                                        amzn_code TEXT NOT NULL);"""
TEST_QUERY = """SELECT * FROM channels WHERE channel != 1;"""


