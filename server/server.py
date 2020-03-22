import socket
import time
import logging
import socket
import sys
import json

import asyncio

op_codes = {
    "find_client": "find_client",
    "register_client": "register_client",
    "remove_client": "remove_client",
    "join_channel": "join_channel",
    "leave_channel": "leave_channel",
    "message_channel": "message_channel",
    "channel_participants": "find_channel_participants"
}


####### Handler for internal data structure #######
class DataHandler():

    def __init__(self, logger):
        self.logger = logger
        self.clients = {}
        self.channels = {}

    def client_register(self, client_name, client_ip):
        self.logger.info(f'Registering client {client_name}@{client_ip}')
        try:
            
            if self.find_client(client_name) == 1:
                self.clients[client_name] = {"address": client_ip}
            else:
                self.logger.info(f'User {client_name} already exists')
                return 1
        except:
            # TODO return a proper error message
            return 1
        return 0

    def client_remove(self, client_name, client_ip):
        self.logger.info(f'Removing client {client_name}@{client_ip}')
        try:
            del self.clients[client_name]
        except:
            # TODO return a proper error message
            return 1
        return 0

    def find_client(self, search_name):
        self.logger.info(f'Finding client {search_name}')
        if search_name in self.clients:
            return self.clients[search_name]
        else:
            return 1

    def join_channel(self, client_name, client_ip, channel_name):
        self.logger.info(f'Client {client_name}@{client_ip} joining: {channel_name}')
        try:
            # This sets the key 'channel_name' as '{}' if it does not exist and returns it otherwise
            self.channels.setdefault(channel_name, {})
            # set a name:address pair in the channel object
            self.channels[channel_name][client_name] = client_ip
        except:
            # TODO return a proper error message
            return 1
        return 0

    def leave_channel(self, client_name, client_ip, channel_name):
        self.logger.info(f'Client {client_name}@{client_ip} leaving: {channel_name}')
        try:
            del self.channels[channel_name][client_name]
        except:
            # TODO return a proper error message
            return 1
        return 0

    def find_channel_participants(self, channel_name):
        self.logger.info(f'Finding participants for channel {channel_name}')
        try:
            return self.channels[channel_name]
        except:
            # TODO return a proper error message
            return 1

    def __check_internal_data_structure__(self):
        print('clients:', self.clients)
        print('channels:', self.channels)


####### Actual server class that handles communication #######
class Server():

    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        self.dataOperations = DataHandler(self.logger)

    def _send_to_single_client(self, receiving_address_, msg):
        awa

    def _broadcast_to_channel(self, channel_participants, sender_name, channel_name, message):
        msg = {
            "sender": sender_name,
            "channel_name": channel_name,
            "message": message
        }
        loop = asyncio.get_event_loop()
        for participant in channel_participants:
            self._send_to_single_client(self.dataOperations.find_client(participant), msg)
        return 0

    def _execute_operation(self, 
                            op_code, 
                            client_name="", 
                            client_ip="", 
                            search_name="",
                            channel_name="",
                            message=""):
        """
        This method handles the data structural operations.
        Takes the client and channel information as arguments.
        Returns a complete answer that is ready to be sent.
        """
        # TODO add logging to this if-structure.
        answer = {
            'status': 0
            }
        
        if op_code == op_codes["register_client"]:
            try:
                answer['status'] = self.dataOperations.client_register(client_name, client_ip)
            except Exception as e:
                answer['status'] = 1
                answer['statusmessage'] = str(e)

        elif op_code == op_codes["remove_client"]:
            try:
                self.dataOperations.client_remove(client_name, client_ip)
            except Exception as e:
                answer['status'] = 1
                answer['statusmessage'] = str(e)

        elif op_code == op_codes["find_client"]:
            try:
                ip_address = self.dataOperations.find_client(search_name)
                answer['address'] = ip_address
            except Exception as e:
                answer['status'] = 1
                answer['statusmessage'] = str(e)

        elif op_code == op_codes["join_channel"]:
            try:
                self.dataOperations.join_channel(client_name, client_ip, channel_name)
            except Exception as e:
                answer['status'] = 1
                answer['statusmessage'] = str(e)

        elif op_code == op_codes["leave_channel"]:
            try:
                self.dataOperations.leave_channel(client_name, client_ip, channel_name)
            except Exception as e:
                answer['status'] = 1
                answer['statusmessage'] = str(e)

        elif op_code == op_codes["channel_participants"]:
            try:
                recipients = self.dataOperations.find_channel_participants(channel_name)
                answer['participants'] = recipients
            except Exception as e:
                answer['status'] = 1
                answer['statusmessage'] = str(e)

        elif op_code == op_codes["message_channel"]:
            try:
                recipients = self.dataOperations.find_channel_participants(channel_name)
                self._broadcast_to_channel(recipients, client_name, channel_name, message)
                answer['participants'] = recipients
            except Exception as e:
                answer['status'] = 1
                answer['statusmessage'] = str(e)

        else:
            answer['status'] = 1
            answer['statusmessage'] = "unkown operation"
        
        return answer


    def run(self):
        # https://asyncio.readthedocs.io/en/latest/tcp_echo.html

        async def handle_socketdata(reader, writer):
            data = await reader.read(256)
            message = data.decode()
            addr = writer.get_extra_info('peername')
            addr = addr[0] + ':' + str(addr[1])
            self.logger.info(f'Received {message} from {addr}')

            try:
                parsed_data = json.loads(message)
            except Exception as e:
                parsed_data = None
                answer = {
                    'status': 1,
                    'statusmessage': str(e)
                    }
                self.logger.info(f'JSON parsing failed for received message')

            if parsed_data:
                # Call the correct method with data parsed from JSON
                operation = parsed_data.get('operation')
                client_name = parsed_data.get('client_name')
                # TODO Enable this check when client sends the port it uses
                # client_address = addr.split(":")[0] + parsed_data.get('client_port')
                search_name = parsed_data.get('search_name')
                channel_name = parsed_data.get('channel_name')
                message = parsed_data.get('message')
                answer = self._execute_operation(operation, client_name=client_name, client_ip=addr, search_name=search_name, message=message, channel_name=channel_name)
                self.logger.info(f'Sending to {addr}: {answer}')

            writer.write(json.dumps(answer).encode('utf-8'))
            await writer.drain()

            self.logger.info('Close the client socket')
            writer.close()
            # THIS PRINT IS JUST FOR TESTING THE THING SO YOU CAN SEE THE INTERNAL DATA STRUCTURES AFTER EACH MESSAGE
            self.dataOperations.__check_internal_data_structure__()

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
