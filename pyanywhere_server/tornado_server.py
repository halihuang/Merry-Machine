import tornado.web
import tornado.wsgi
from tornado.ioloop import IOLoop
import config
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
        try:
            encoded_sources = json.loads(self.request.body)
            predictions = run_process(predict_pos_labels, encoded_sources)
            if predictions is not None:
                requests.post("https://merrymachine.herokuapp.com/predicter", json=predictions)
                print('sent pos post')
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
            predictions = run_process(predict_pos_labels, encoded_sources)
            if predictions is not None:
                requests.post("https://merrymachine.herokuapp.com/predicter", json=predictions)
                print('sent pos post')
                self.write('success')
            else:
                print('failure to predict')
                self.write('failure')
        except json.decoder.JSONDecodeError:
            print("invalid json")

class PolModelHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            encoded_sources = json.loads(self.request.body)
            predictions = run_process(predict_pos_labels, encoded_sources)
            if predictions is not None:
                requests.post("https://merrymachine.herokuapp.com/predicter", json=predictions)
                print('sent pos post')
                self.write('success')
            else:
                print('failure to predict')
                self.write('failure')
        except json.decoder.JSONDecodeError:
            print("invalid json")

application = tornado.wsgi.WSGIApplication(
    handlers=[
        (r"/", MainHandler),
        (r"/positive", PosModelHandler),
        (r"/negative", NegModelHandler),
        (r"/political", PolModelHandler)
    ],
    sockets=[]
)