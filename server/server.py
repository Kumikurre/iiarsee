import socket
import time
import logging
import socket
import sys

from sqlalchemy import create_engine
import asyncio

import database_init
import database_methods 


# https://asyncio.readthedocs.io/en/latest/tcp_echo.html
"""
async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print("Received %r from %r" % (message, addr))

    print("Send: %r" % message)
    writer.write(data)
    await writer.drain()

    print("Close the client socket")
    writer.close()

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', 8888, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
"""


# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()

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
        self.logger = logger
        self.logger.info('Initializing database')
        # TODO move these credentials to the config file
        self.engine = create_engine('mysql://tshatti:tshattipassu@db:3306')
        database_init.initialize(self.engine, logger)
        self.logger.info('Database initialized')
        # DBiface = database_methods(self.engine)


    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(1)
        self.logger.info('Server started')
        totaltime = 0
        while True:
            time.sleep(5)
            totaltime += 5
            self.logger.info(f'waited total of {totaltime} seconds')

if __name__ == '__main__':
    # Setting up logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Configs for the server. 
    # TODO This should be moved to external file
    config = {
        "TCP_PORT": 8666,
        "BUFFER_SIZE": 1024,
        "TCP_IP": '127.0.0.1'
    }
    
    # Start the actual server
    logger.info('Starting server...')
    server = Server(logger)
    server.run()
