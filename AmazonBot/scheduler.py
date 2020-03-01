# Simple scheduler for messages

import time
from .post_manager import SCHEDULED, send_post
import logging


def scheduler_thread():
    logging.info("Message Scheduler started")
    while True:
        for index, args in enumerate(SCHEDULED):
            if args[3] == int(time.time()):
                logging.debug("Found message to schedule, sending...")
                args[3] = False
                send_post(*args)
                del args
