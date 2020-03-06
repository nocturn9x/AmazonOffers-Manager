# Made by IsGiambyy aka Nocturn9x - All rights reserved (C) 2020

import requests
import json
import logging
from collections import deque
from .config import API_SEARCH_URL, API_OFFERS_URL, HEADERS


def search_products(which: str):
    """Searches products matching the which query and returns only the ones on sale
    """

    logging.debug(f"Searching for '{which}'...")
    offers = deque()
    logging.info("Scraper started")
    request = requests.get(API_SEARCH_URL.format(which=which), headers=HEADERS)
    if request.status_code != 200:
        logging.error("Uh oh! Could not reach API")
        exit(request.status_code)
    logging.debug(f"Loading JSON...")
    try:
        data = json.loads(request.content)
    except json.JSONDecodeError as e:
        logging.error(f"Error while loading json response from API! -> {e}")
        return None
    logging.info(f"Scraped {len(data)} products, checking for offers...")
    for product in data:
        if product.get("oldPrice", None):
            offers.append(product)
            logging.debug(f"Found an offer! Product name is '{product['name']}'")
    logging.info(f"Out of {len(data)} products, {len(offers)} are on sale")
    if not offers:
        logging.debug("No offers found :(")
        return deque()
    return offers


def scrape_random_deal():
    """Scrapes the latest deals from the API and returns them"""

    logging.debug("Contacting API for deals...")
    while True:
        request = requests.get(API_OFFERS_URL, headers=HEADERS)
        if request.status_code != 200:
            logging.error("Uh oh! Could not reach API")
            exit(request.status_code)
        logging.debug(f"Loading JSON...")
        try:
            data = json.loads(request.content)
        except json.JSONDecodeError as e:
            logging.error(f"Error while loading json response from API! -> {e}")
            return None
        logging.info(f"Scraped a random deal")
        if not data:
            logging.debug("No offers found :(")
            return deque()
        elif "ok" not in data:
            break
    return data



