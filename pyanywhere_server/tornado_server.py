import tornado.web
import tornado.wsgi
import requests
import logging
import json
from model import predict_pos_labels, predict_neg_labels, predict_pol_labels, run_process

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
        self.write("Pinging")

class NegModelHandler(tornado.web.RequestHandler):
    def post(self):
        print('got neg get request')
        try:
            encoded_sources = json.loads(self.request.body)
            predictions = run_process(predict_neg_labels, encoded_sources)
            if predictions is not None:
                # requests.post("https://merrymachine.herokuapp.com/predicter", json=predictions)
                print('wrote neg data')
                self.write('success')
            else:
                print('failure to predict')
                self.write('failure')
        except json.decoder.JSONDecodeError:
            print("invalid json")

class PosModelHandler(tornado.web.RequestHandler):
    def post(self):
        print('got pos get request')
        try:
            encoded_sources = json.loads(self.request.body)
            print(encoded_sources)
            predictions = run_process(predict_pos_labels, encoded_sources)
            if predictions is not None:
                # requests.post("https://merrymachine.herokuapp.com/predicter", json=predictions)
                print('wrote pos data')
                self.write('success')
            else:
                print('failure to predict')
                self.write('failure')
        except json.decoder.JSONDecodeError:
            print("invalid json")

class PolModelHandler(tornado.web.RequestHandler):
    def post(self):
        print('got pol get request')
        try:
            encoded_sources = json.loads(self.request.body)
            predictions = run_process(predict_pol_labels, encoded_sources)
            if predictions is not None:
                # requests.post("https://merrymachine.herokuapp.com/predicter", json=predictions)
                print('wrote pol data')
                self.write('success')
            else:
                print('failure to predict')
                self.write('failure')
        except json.decoder.JSONDecodeError:
            print("invalid json")

class DataHandler(tornado.web.RequestHandler):
    def get(self):
        with open('predictions.json') as file:
          predictions = json.load(file)
          self.set_header("Access-Control-Allow-Origin", "*")
          self.set_header("Access-Control-Allow-Headers", "x-requested-with")
          self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
          self.write(json.dumps(predictions))

application = tornado.wsgi.WSGIApplication(
    handlers=[
        (r"/", MainHandler),
        (r"/positive", PosModelHandler),
        (r"/negative", NegModelHandler),
        (r"/political", PolModelHandler),
        (r"/data", DataHandler)
    ],
    sockets=[]
)