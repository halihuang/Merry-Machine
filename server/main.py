#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing import Process
from websocket import create_connection

import logging
import json
import time
import start_web

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] [%(levelname)-5.5s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('app')


def main():
    
    time.sleep(5)

    data_ws = create_connection("ws://localhost:5000/data/ws")
    political_ws = create_connection("ws://localhost:5000/political/ws")
    positive_ws = create_connection("ws://localhost:5000/positive/ws")
    negative_ws = create_connection("ws://localhost:5000/negative/ws")

    # while(True):
    #   data_ws.send(json.dumps(dict(targets=json.load(open('example.json', 'rb')))))


if __name__ == '__main__':

    p = Process(target=start_web.main)
    p.start()
    main()
    p.join()
