import socket
import time
import logging
import socket
import sys

from sqlalchemy import create_engine
import asyncio

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

    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        # TODO move these credentials to the config file
        self.engine = create_engine('mysql://tshatti:tshattipassu@db:3306')

    """
    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.config['HOSTNAME'], self.config['PORT']))
        self.socket.listen(1)
        self.logger.info('Server started')
        totaltime = 0
        while True:
            time.sleep(5)
            totaltime += 5
            self.logger.info(f'waited total of {totaltime} seconds')
    """
    
    def run(self):
        # https://asyncio.readthedocs.io/en/latest/tcp_echo.html

        async def handle_echo(reader, writer):
            data = await reader.read(100)
            message = data.decode()
            addr = writer.get_extra_info('peername')
            self.logger.info(f'Received {message} from {addr}')

            self.logger.info(f'Send: {message}')
            writer.write(data)
            await writer.drain()

            self.logger.info('Close the client socket')
            writer.close()

        loop = asyncio.get_event_loop()
        coroutine = asyncio.start_server(handle_echo, self.config['HOSTNAME'], self.config['PORT'], loop=loop)
        server = loop.run_until_complete(coroutine)

        # Serve requests until Ctrl+C is pressed
        self.logger.info(f'Serving on {server.sockets[0].getsockname()}')
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass

        # Close the server
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()


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
        "PORT": 8666,
        "BUFFER_SIZE": 1024,
        "HOSTNAME": '0.0.0.0'
    }
    
    # Start the actual server
    logger.info('Starting server...')
    server = Server(logger, config)
    server.run()
