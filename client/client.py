import argparse
import json
import logging
import socket
import click

clientId = "test_client"

possible_actions = {"receive": receive, }

def receive(self, parameter_list):
    raise NotImplementedError


logger = logging.getLogger("ds_messaging_client")
logger.setLevel("info")

parser = argparse.ArgumentParser("ds_messaging_client")
parser.add_argument("--debug", help="Enable debugging")
parser.add_argument("--address", help="IP addrss for the server")
parser.add_argument("--port", help="Which port to connect to", type=int)

args = parser.parse_args()
if not args.address or not args.port:
    raise Exception('Missing critical input')
if args.debug:
    logger.setLevel("debug")

# the client also needs to have a "server" at all times listening to other clients possibly wanting to connect to them.
# so we should have some sort of background listener running that interupts (? or what ever you call it) incase someone connects to it
# 


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((args.address, args.port))
        s.sendall("Hey monseaur server. Gimme things. I'm {}".format(clientId))
        # switchcases for every possible action
        # inside a while loop.

        #send the first message connecting to server
        while (True):
            #receive the response from server
            #decode the data received
            # based on the action given from server jump to that in the switchcases
            if action == "receive stuff":
                pass
            elif action == "moar":
                pass
            else:
                continue

        # we need to a while loop for the client ui in which the user can send messages, change channels etc etc



# TODO: Design the interactive cli.
# TODO: Design the switchcase and functions for the client logic
# TODO: Create the separate server to listen for incoming other clients
# TODO: Glue it all together
# NOTE: https://opensource.com/article/17/5/4-practical-python-libraries
# NOTE: https://codeburst.io/building-beautiful-command-line-interfaces-with-python-26c7e1bb54df
# NOTE: https://realpython.com/python-sockets/
