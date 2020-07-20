import tornado.web
from tornado.ioloop import IOLoop
from os.path import abspath, dirname, join
import config
import logging
import json
import requests

from data_ws import DataWS
from scraper_ws import ScraperWS
from model import encode_text
from webscraper.scraper import create_json

logger = logging.getLogger(__name__)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello")

class PredicterHandler(tornado.web.RequestHandler): 
    def get(self): 
        self.write("Data should be sent to me! Don't ask me for data!") 
    def post(self): 
      #self.set_header("Content-Type", "application/json")
      data = json.loads(self.request.body)
      print('post data')
      print(data)
      print('here')
      with open('predictions.json', 'w') as outfile:
        print('here2')
        json.dump(data, outfile)
        print('done')
        self.write("Thank you for the Data!")

    # def set_default_headers(self): 
    #     self.set_header("Content-Type", 'application/json') 
    # def post(self): 
    #     data = self.get_argument('key') 

    #     cbtp = cbt.main(value) 
    #     r = json.dumps({'cbtp': cbtp}) 
    #     self.write(r)

class JSONFileHandler(tornado.web.RequestHandler):
    def get(self):
        with open('encoded.json') as file:
          encoded_sources = json.load(file)
          print(encoded_sources)
          self.write(json.dumps(encoded_sources))

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
            print(encoded_sources)
            requests.post('https://merrymachine-ml.herokuapp.com/positive', json=encoded_sources)
            self.write('pos')

class NegativeHandler(tornado.web.RequestHandler):
    def get(self):
        with open('encoded.json') as file:
            encoded_sources = json.load(file)
            print(encoded_sources)
            requests.post('https://merrymachine-ml.herokuapp.com/negative', json=encoded_sources)
            self.write('pos')

class PoliticalHandler(tornado.web.RequestHandler):
    def get(self):
        with open('encoded.json') as file:
            encoded_sources = json.load(file)
            print(encoded_sources)
            requests.post('https://merrymachine-ml.herokuapp.com/political', json=encoded_sources)
            self.write('pos')

def start():

    app = tornado.web.Application(
        handlers=[
            ("/data/ws", DataWS),
            ("/scraper/ws", ScraperWS),
            (r"/", MainHandler),
            (r"/positive", PositiveHandler),
            (r"/negative", NegativeHandler),
            (r"/political", PoliticalHandler),
            (r"/predicter", PredicterHandler),
            (r"/json", JSONFileHandler),
            (r"/webscraper", ScraperHandler),
            (r"/encoder", EncoderHandler)
        ],
        sockets=[]
    )


    # Start the app
    logger.info("Listening on http://localhost:%s/", config.tornado_server_port)

    app.listen(config.tornado_server_port)
    IOLoop.current().start()
