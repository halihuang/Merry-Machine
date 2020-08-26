import tornado.web
import tornado.wsgi
from tornado.ioloop import IOLoop
import config
import logging
import json

from data_ws import DataWS
from scraper_ws import ScraperWS
from model import encode_text, predict_pos_labels, predict_neg_labels, predict_pol_labels
from webscraper.scraper import create_json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] [%(levelname)-5.5s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello")

class ScraperHandler(tornado.web.RequestHandler):
    def get(self):
        create_json()
        self.write("Scraping articles")

class EncoderHandler(tornado.web.RequestHandler):
    def get(self):
        encode_text()
        self.write("Encoding articles")

class PositiveHandler(tornado.web.RequestHandler):
    def get(self):
        with open('encoded.json') as file:
            encoded_sources = json.load(file)
            predict_pos_labels(json.loads(encoded_sources.text))
            self.write("predicted positive")

class NegativeHandler(tornado.web.RequestHandler):
    def get(self):
        with open('encoded.json') as file:
            encoded_sources = json.load(file)
            predict_neg_labels(json.loads(encoded_sources.text))
            self.write("predicted positive")

class PoliticalHandler(tornado.web.RequestHandler):
    def get(self):
        with open('encoded.json') as file:
            encoded_sources = json.load(file)
            predict_pol_labels(json.loads(encoded_sources.text))
            self.write("predicted positive")

app = tornado.wsgi.WSGIApplication(
    handlers=[
        ("/data/ws", DataWS),
        ("/scraper/ws", ScraperWS),
        (r"/", MainHandler),
        (r"/positive", PositiveHandler),
        (r"/negative", NegativeHandler),
        (r"/political", PoliticalHandler),
        (r"/webscraper", ScraperHandler),
        (r"/encoder", EncoderHandler)
    ],
    sockets=[]
)
