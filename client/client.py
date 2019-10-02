import asyncio
import argparse
import json
import logging
import socket
import prompt_toolkit


# should we have a separate worker for p2p messaging to act as a server to the other client, which would take care of the message
# receiving and notification of the actual client

class ClientSession:
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
    session = prompt_toolkit.PromptSession()
    # do the login right away here (we don't support offline mode :P)
    # can we pass a socket to another process?
    # or should we first create the server process here and interact with it for the login, then
    # move it to the background and start another process for the actual interactive client

    # TODO Learn how to run separate processes with the asyncio
    # TODO How to handle the communication/notification between the server process and the client process
    # TODO Can we separate a common logic for the messages between client and server
    # TODO Implement actual message/-logic class with actions and re-actions
    # TODO Implement the command-line-interface for the client
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
                # here comes there  logic for a given command
                # do we use a switch case like logic? Have all the possible commands in a dict/function with handles for the corresponding functions as values
                # 
                # once the command is entered and no interuption, we enter here
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
