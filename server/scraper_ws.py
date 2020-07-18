import uuid
from tornado.websocket import WebSocketHandler, WebSocketClosedError
import logging
import string
import json
from webscraper import scraper

logger = logging.getLogger(__name__)

class ScraperWS(WebSocketHandler):
    """
    """
    watchers = set()
    def open(self):
        logger.info("Scraping websocket opened")
        self.write_message(json.dumps(dict(targets=json.load(open('predictions.json', 'rb')))))
        ScraperWS.watchers.add(self)

    def check_origin(self, origin):
        """
            Allow CORS requests
        """
        return True

    """
    broadcast to clients, assumes its target data
    """
    def on_message(self, message):
        for waiter in ScraperWS.watchers:
            if waiter == self:
                continue
            if(message == 'get articles'):
              print('obtaining articles')
              with open('predictions.json') as file:
                  positive_articles = json.load(file)
                  waiter.write_message(json.dumps(positive_articles))
            

    def send_msg(self, msg):
        try:
            self.write_message(msg, False)
        except WebSocketClosedError:
            logger.warn("websocket closed when sending message")

    def on_close(self):
        logger.info("Data streaming websocket closed")
        ScraperWS.watchers.remove(self)