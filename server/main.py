#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing import Process
from websocket import create_connection

import logging
import json
import time
import start_web
import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] [%(levelname)-5.5s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('app')

def main():

    print('hello')

    time.sleep(5)

    print(config.tornado_server_port)

    
    # ml_ws.send("stay awake")
    #data_ws = create_connection("ws://merrymachine.herokuapp.com:" + config.tornado_server_port + "/data/ws")
    #scraper_ws = create_connection("ws://merrymachine.herokuapp.com:" + config.tornado_server_port + "/scraper/ws")

    # schedule.every().day.at("06:30").do(os.system('python webscraper/scraper.py'))
    # schedule.every().day.at("07:00").do(os.system('python model.py'))
    # schedule.every().day.at("11:30").do(os.system('python webscraper/scraper.py'))
    # schedule.every().day.at("12:00").do(os.system('python model.py'))
    # schedule.every().day.at("17:30").do(os.system('python webscraper/scraper.py'))
    # schedule.every().day.at("18:00").do(os.system('python model.py'))

    # while True:
    #   schedule.run_pending()


if __name__ == '__main__':

    p = Process(target=start_web.main)
    p.start()
    main()
    p.join()
