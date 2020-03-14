import socket
import time
import logging
import socket
import sys

import asyncio

op_codes = {
    "find_client": "find_client",
    "register_client": "register_client",
    "remove_client": "remove_client",
    "join_channel": "join_channel",
    "leave_channel": "leave_channel",
    "message_channel": "message_channel"
}


####### Handler for internal data structure #######
class DataHandler():

    def __init__(self, logger):
        self.logger = logger
        self.clients = {}
        self.channels = {}

    def client_register(self, client_name, client_ip):
        self.logger.info(f'Registering client {client_name}@{client_ip}')
        # TODO should first call find_client() if a client already exists and then return an error message
        try:
            self.clients[client_name] = {"address": client_ip}
            return
        pass

    def client_remove(self, client_name):
        self.logger.info(f'Removing client {client_name}@{client_ip}')
        try:
            del self.clients[client_name]
            return
        pass

    def find_client(self, search_name):
        self.logger.info(f'Finding client {search_name}')
        try:
            return self.clients[search_name]

    def join_channel(self, client_name, client_ip, channel_name):
        self.logger.info(f'Client {client_name}@{client_ip} joining: {channel_namme}')
        try:
            # This sets the key 'channel_name' as '{}' if it does not exist and returns it otherwise
            self.channels.setdefault(channel_name, {})
            # set a name:address pair in the channel object
            self.channels[channel_name][client_name] = client_ip
            return
        pass

    def leave_channel(self, client_name, channel_name):
        self.logger.info(f'Client {client_name}@{client_ip} leaving: {channel_namme}')
        try:
            del self.channels[channel_name][client_name]
            return
        pass

    def find_channel_participants(self, channel_name):
        self.logger.info(f'Finding participants for channel {channel_name}')
        try:
            return self.channels[channel_name]
        pass



####### Actual server class that handles communication #######
class Server():

    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        self.dataOperations = DataHandler(self.logger)
    
    def run(self):
        # https://asyncio.readthedocs.io/en/latest/tcp_echo.html

        async def handle_socketdata(reader, writer):
            data = await reader.read(100)
            message = data.decode()
            addr = writer.get_extra_info('peername')
            print(f'Received {message} from {addr}')

            answer = {
                'status': 0
            }

            if operation == op_codes["register_client"]:
                try:
                    DataHandler.client_register(self, "client_name", "client_ip")
                except Exception as e:
                    answer['status'] = 1
                    answer['statusmessage'] = e
                pass
            if operation == op_codes["remove_client"]:
                try:
                    DataHandler.client_remove(self, "client_name")
                except Exception as e:
                    answer['status'] = 1
                    answer['statusmessage'] = e
                pass
            if operation == op_codes["find_client"]:
                try:
                    ip_address = DataHandler.find_client(self, "search_name")
                    answer['address'] = ip_address
                except Exception as e:
                    answer['status'] = 1
                    answer['statusmessage'] = e
                pass
            if operation == op_codes["join_channel"]:
                try:
                    DataHandler.join_channel(self, "client_name", "client_ip", "channel_name")
                except Exception as e:
                    answer['status'] = 1
                    answer['statusmessage'] = e
                pass
            if operation == op_codes["leave_channel"]:
                try:
                    DataHandler.join_channel(self, "client_name", "channel_name")
                except Exception as e:
                    answer['status'] = 1
                    answer['statusmessage'] = e
                pass
            if operation == op_codes["message_channel"]:
                try:
                    recipients = DataHandler.find_channel_participants(self, "channel_name")
                    pass
                except Exception as e:
                    answer['status'] = 1
                    answer['statusmessage'] = e
            else:
                answer['status'] = 1
                answer['statusmessage'] = "unkown operation"


            self.logger.info(f'Send: {message}')
            writer.write(data)
            await writer.drain()

            self.logger.info('Close the client socket')
            writer.close()

        loop = asyncio.get_event_loop()
        coroutine = asyncio.start_server(handle_socketdata, self.config['HOSTNAME'], self.config['PORT'], loop=loop)
        server = loop.run_until_complete(coroutine)

        # Serve requests until Ctrl+C is pressed
        self.logger.info(f'Serving on: {server.sockets[0].getsockname()}')
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
