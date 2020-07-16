#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tornado_server

import logging

logger = logging.getLogger('app')


def main():
    print('hello')
    logger.info("starting server")
    tornado_server.start()

if __name__ == '__main__':

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] [%(levelname)-5.5s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )
    main()
