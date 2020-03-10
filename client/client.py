# import asyncio
import argparse
import json
import logging
import socket
import prompt_toolkit
import sys

#### CONSTANTS:
client_start_message = "Welcome to iiarsee, the ultimate communication tool."
client_main_menu = \
    "What do you want to do? \n" \
    "(r)ead messages from channel\n" \
    "send message to (c)hannel\n" \
    "send message to (u)ser\n" \
    "(j)oin channel\n" \
    "(l)eave a channel\n" \
    "(q)uit"

possible_operations_to_server: {
    "register_client": "register_client",
    "message_channel": "message_channel",
    "join_channel": "join_channel",
    "leave_channel": "leave_channel",
    "find_client": "find_client",
    "quit_client": "quit_client"
}

# when client starts it registers to the server
# even when client is inactive, idling, it will still send a heartbeat to the server
# when the client quits it will send a "quitting" message to the server

# should all the channels the client is in be in a dict with a list of messages
# a message could be like "<username>: <message>"


# should we have a separate worker for p2p messaging to act as a server to the other client, which would take care of the message
# receiving and notification of the actual client

class ClientSession():
    def __init__(self):
        self.channels = {}
        self.privates = {}
        self.clients = {}

    def register_client(self, client_name):
        """A method for registering the client to the server"""
        pass

    def read_messages(self):
        pass

    def message_channel(self, client_name, client_ip):
        pass

    def message_client(self, client_name):
        self._find_client_address()
        pass

    def join_channel(self, client_name, client_ip, channel_name):
        pass

    def leave_channel(self, client_name, channel_name):
        pass

    def quit_client(self, client_name, channel_name, message):
        pass

    def _find_client_address(self, client_name, client_ip):
        pass

    # have internal state of the session here
    # e.g. the channel in which the client is, do we want to have client actively in one channel?
    # or should we just have the state of each channel displayed to the client at all times with no "active" channel
    # simply printing 

    # we need a separate process to handle the incoming messages from the server and other clients
    # that writes the messages to files and notifies the actual interactive client of new messages in a channel

    # should we create the clientS server when we call the login to the actual server.


def receive(self, parameter_list):
    raise NotImplementedError


def main():
    channels = {}
    privates = {}
    session = prompt_toolkit.PromptSession()
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((args.address, args.port))

            try:
                # here we handle the client giving us a command
                # interactive shell code here?
                # have logic to only allow the given commands and retry if not in the possible commands
                # 
                text = session.prompt('client> ')
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
            else:
                ### If else block which checks for each possible command and calls the corresponding methods
                
                print('You entered:', text)
                print("sending...")
                s.sendall(text.encode())
                data = s.recv(1024)
                if not data:
                    break
                # here comes the logic after receiving an answer from the server.
                # another dict/function/class with functions/methods for possible responses?
                print("Received back:", data.decode())
                s.close()
    print('Done.')


logger = logging.getLogger("ds_messaging_client")
logger.setLevel("INFO")

parser = argparse.ArgumentParser("ds_messaging_client")
parser.add_argument("--debug", help="Enable debugging")
parser.add_argument("--address", help="IP addrss for the server")
parser.add_argument("--port", help="Which port to connect to", type=int)

args = parser.parse_args()
# default to local host if no arguments given
if not args.address:
    args.address = '127.0.0.1'
if not args.port:
    args.port = 8666
if args.debug:
    logger.setLevel("debug")

# the client also needs to have a "server" at all times listening to other clients possibly wanting to connect to them.
# so we should have some sort of background listener running that interupts (? or what ever you call it) incase someone connects to it


if __name__ == '__main__':
    main()


# NOTE: https://opensource.com/article/17/5/4-practical-python-libraries
# NOTE: https://codeburst.io/building-beautiful-command-line-interfaces-with-python-26c7e1bb54df
# NOTE: https://realpython.com/python-sockets/
