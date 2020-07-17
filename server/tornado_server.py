import tornado.web
from tornado.ioloop import IOLoop
from os.path import abspath, dirname, join
import config
import logging

from data_ws import DataWS
from positive_ws import PositiveWS
from negative_ws import NegativeWS
from political_ws import PoliticalWS

logger = logging.getLogger(__name__)

def start():

    app = tornado.web.Application(
        handlers=[
            ("/data/ws", DataWS),
            ("/positive/ws", PositiveWS),
            ("/political/ws", PoliticalWS),
            ("/negative/ws", NegativeWS)
        ],
        sockets=[]
    )


    # Start the app
    logger.info("Listening on http://localhost:%s/", config.tornado_server_port)

    app.listen(config.tornado_server_port)
    IOLoop.current().start()
