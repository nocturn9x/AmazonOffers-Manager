# Simple scheduler for messages

import time
from .post_manager import SCHEDULED, send_post
import logging
import math


def scheduler_thread():
    logging.info("Message Scheduler started")
    while True:
        for index, args in enumerate(SCHEDULED):
            if math.isclose(args[3], time.time(), abs_tol=3):
                logging.debug("Found message to schedule, sending...")
                send_post(*args)
