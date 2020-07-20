from os.path import abspath, dirname, join

import uuid
from tornado.websocket import WebSocketHandler, WebSocketClosedError
import logging

import json
import string

logger = logging.getLogger(__name__)

class MLWS(WebSocketHandler):
    """
    """
    watchers = set()
    def open(self):
        logger.info("Data streaming websocket opened")
        self.write_message("hallo!")
        MLWS.watchers.add(self)

    def check_origin(self, origin):
        """
            Allow CORS requests
        """
        return True

    """
    broadcast to clients, assumes its target data
    """
    def on_message(self, message):
        for waiter in MLWS.watchers:
            if waiter == self:
                continue
            print(message)
            if(message == 'stay awake'):
              waiter.write_message('stay awake')
            elif(message == 'pos'):
              print('sending articles')
              with open('encoded.json') as file:
                  articles = json.load(file)
                  waiter.write_message('{"category": "positive", "json": ' + articles + '}')
            elif(message == 'neg'):
              print('sending articles')
              with open('encoded.json') as file:
                  articles = json.load(file)
                  waiter.write_message('{"category": "negative", "json": ' + articles + '}')
            elif(message == 'pol'):
              print('sending articles')
              with open('encoded.json') as file:
                  articles = json.load(file)
                  waiter.write_message(json.dumps({"category": "political", "json": articles}))
            else:
              print('got predicitions')
              with open('predictions.json', 'w') as outfile:
                  try:
                      json.dump(json.loads(message), outfile)
                      waiter.write_message("Thank you for the Data!")
                  except:
                      print('that was not a json!')
                      waiter.write_message("Please send a JSON file")


            

    def send_msg(self, msg):
        try:
            self.write_message(msg, False)
        except WebSocketClosedError:
            logger.warn("websocket closed when sending message")

    def on_close(self):
        logger.info("Data streaming websocket closed")
        MLWS.watchers.remove(self)
