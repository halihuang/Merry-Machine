import tornado.web
from tornado.ioloop import IOLoop
from os.path import abspath, dirname, join
import config
import logging

from data_ws import DataWS
from scraper_ws import ScraperWS


logger = logging.getLogger(__name__)

def start():

    app = tornado.web.Application(
        handlers=[
            ("/data/ws", DataWS),
            ("/scraper/ws", ScraperWS),
        ],
        sockets=[]
    )


    # Start the app
    logger.info("Listening on http://localhost:%s/", config.tornado_server_port)

    app.listen(config.tornado_server_port)
    IOLoop.current().start()
