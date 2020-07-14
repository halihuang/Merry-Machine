from os.path import abspath, dirname, join

import uuid
from tornado.websocket import WebSocketHandler, WebSocketClosedError
import logging

import json
import string

logger = logging.getLogger(__name__)

class DataWS(WebSocketHandler):
    """
    """
    watchers = set()
    def open(self):
        logger.info("Data streaming websocket opened")
        self.write_message(json.dumps(dict(targets=json.load(open('example.json', 'rb')))))
        DataWS.watchers.add(self)

    def check_origin(self, origin):
        """
            Allow CORS requests
        """
        return True

    """
    broadcast to clients, assumes its target data
    """
    def on_message(self, message):
        for waiter in DataWS.watchers:
            if waiter == self:
                continue
            waiter.write_message(message)
            #json.dump(message, student_dumped,indent = 4,sort_keys = True)
            logger.info((json.loads(message))['title'])
            fileName = (json.loads(message))['title']
            fileName = "".join(filter(lambda char: char in string.ascii_letters, fileName))  + '.json'
            fileDir = './jsons/' + fileName
            with open(fileDir, 'w') as outfile:
              json.dump(message, outfile, sort_keys=True, indent=4)

    def send_msg(self, msg):
        try:
            self.write_message(msg, False)
        except WebSocketClosedError:
            logger.warn("websocket closed when sending message")

    def on_close(self):
        logger.info("Data streaming websocket closed")
        DataWS.watchers.remove(self)
