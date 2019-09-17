import socket
import time
import logging
import socket
import sys

from sqlalchemy import create_engine

import database_init
import database_methods 


####### THE PROPRIETARY TCP-INTERFACE FOR COMMUNICATION #######
class socketInterface():
    def __init__(self):
        pass

    def listen(self):
        pass

    def send_channel(self):
        pass

####### THIS IS THE ACTUAL SERVER CLASS #######
class Server():
    
    def __init__(self, logger):
        logger = logger
        logger.info('Initializing database')
        engine = create_engine('mysql://tshatti:tshattipassu@db:3306')
        database_init.initialize(engine, logger)
        logger.info('Database initialized')
        # DBiface = database_methods(engine)

    def run(self):
        logger.info('Server started')
        totaltime = 0
        while True:
            time.sleep(5)
            totaltime += 5
            logger.info(f'waited total of {totaltime} seconds')

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.info('Starting server...')
    server = Server(logger)
    server.run()
