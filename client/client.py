import asyncio
import argparse
import json
import logging
import socket
import prompt_toolkit
import sys

#### CONSTANTS:
username = prompt_toolkit.prompt("Register as: ")
client_start_message = f"Welcome to iiarsee {username}. Press [Ctrl-Q] to quit."
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
        self.client_name = None
        self.channels = {}
        # channels = {
        #   "channel1": [{timestamp: <timestamp>, client_name: <client_name>, message: <informative message>"}],
        #   "channel2": []
        # }
        # 
        self.clients = {}
        # clients {
        #   "client1": {
        #       "address": "127.0.0.1",
        #       "messages": [],
        #       "state": "INACTIVE"
        #   }
        # }

    def register_client(self, client_name):
        """A method for registering the client to the server"""
        # this method sets the self.client_name
        pass

    def read_messages(self, channel_name, rows=5):
        """Prints n last messages for given channel"""
        pass

    def message_channel(self, channel_name, message):
        """Sends a message to a given channel on the server"""
        pass

    def message_client(self, client_name):
        """Sends a message to a given client"""
        client_address = self._find_client_address()
        pass

    def receive_message_server(self):
        """Handle receiving of message from server"""
        pass

    def receive_message_client(self):
        """Handle receiving of message from server"""
        pass

    def join_channel(self, client_name, client_ip, channel_name):
        """Joins a given channel on the server"""
        pass

    def leave_channel(self, client_name, channel_name):
        """Leaves a given channel on the server"""
        pass

    def quit_client(self, client_name, channel_name, message):
        """Sends a "CLIENT_QUITTING" message to the server and other clients in the clients object"""
        pass
        # send also quit message to whole client_address_book -> client removed from client_address_book

    def _find_client_address(self, client_name, client_ip):
        """Find a given client's true network address from the server"""
        pass
        # clients send quit message also to other clients  they're in contact with
        # clients keep a client_address_book in which they also keep the state of other clients
        # if client_name in clients and clients[client_name].state == "ACTIVE": suoraan clientille jutteleen
        # muuten käydään serverillä



    # have internal state of the session here
    # e.g. the channel in which the client is, do we want to have client actively in one channel?
    # or should we just have the state of each channel displayed to the client at all times with no "active" channel
    # simply printing 

    # we need a separate process to handle the incoming messages from the server and other clients
    # that writes the messages to files and notifies the actual interactive client of new messages in a channel

    # should we create the clientS server when we call the login to the actual server.


def receive(self, parameter_list):
    raise NotImplementedError

# Takes the user input from input_field and begins operations based on it
# TODO: parse user input to <operation> [<kelle/mille kanavalle> <teksti>]
#    esim. /register latsis
#          /q
#          /msg sakkoja mitäpä ukko mee töihin
def accept_input(buff):
    """Handler for accepting user input"""
    new_text = chat_field.text + "\n" + input_field.text
    chat_field.buffer.document = prompt_toolkit.document.Document(text=new_text, cursor_position=len(new_text))

    user_input = input_field.text.split()
    try:
        operation = str(user_input[0])
        recipient = str(user_input[1])
        message = " ".join(map(str, user_input[2:]))

        if operation == "/register":
            #register_client()
            pass
        if operation== "/read_msg":
            #read_messages()
            pass
        elif operation == "/channel":
            #message_channel()
            pass
        elif operation == "/msg":
            #message_client()
            #tää kauhee sekasotku pois heti kun funkkarit toimii
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(("127.0.0.1", 8666))
                s.sendall(str.encode(f"{username}: " + message))
                data = s.recv(1024)
                new_text = chat_field.text + "\n" + data.decode()
                chat_field.buffer.document = prompt_toolkit.document.Document(text=new_text, cursor_position=len(new_text))
        elif operation == "/join":
            #join_channel()
            pass
        elif operation == "/leave":
            #leave_channel()
            pass
        elif operation == "/quit":
            #quit_client()
            pass

    except IndexError:
        pass

# Create the layout
chat_field = prompt_toolkit.widgets.TextArea()
input_field = prompt_toolkit.widgets.TextArea(
        height=1,
        prompt=">>> ",
        style="class:input-field",
        multiline=False,
        wrap_lines=False,
        accept_handler=accept_input,
    )

root_container = prompt_toolkit.layout.containers.HSplit([
    prompt_toolkit.layout.containers.Window(
        height=2, 
        content=prompt_toolkit.layout.controls.FormattedTextControl(client_start_message), 
        align=prompt_toolkit.layout.containers.WindowAlign.CENTER), 
    prompt_toolkit.layout.containers.HSplit([
        chat_field, 
        input_field], 
        padding=1, 
        padding_char='_'),
    ], 
    padding=1, 
    padding_char='_')

input_field.accept_handler = accept_input

# Add keybinds to make user's life easier
# Ctrl+C and Ctrl+Q: exit application
kb = prompt_toolkit.key_binding.KeyBindings()
@kb.add('c-c', eager=True)
@kb.add('c-q', eager=True)
def _(event):
    """Pressing Ctrl-Q or Ctrl-C will exit the user interface."""
    event.app.exit()

# Create an 'Application' instance
application = prompt_toolkit.application.Application(
    layout=prompt_toolkit.layout.layout.Layout(root_container, focused_element=input_field),
    key_bindings=kb,
    mouse_support=True,
    full_screen=True)


def main():
    channels = {}
    privates = {}
    application.run()
    # session = prompt_toolkit.PromptSession()
    # while True:
    #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #         s.connect((args.address, args.port))

    #         try:
    #             # here we handle the client giving us a command
    #             # interactive shell code here?
    #             # have logic to only allow the given commands and retry if not in the possible commands
    #             # 
    #             text = session.prompt('client> ')
    #         except KeyboardInterrupt:
    #             continue
    #         except EOFError:
    #             break
    #         else:
    #             ### If else block which checks for each possible command and calls the corresponding methods
                
    #             print('You entered:', text)
    #             print("sending...")
    #             s.sendall(text.encode())
    #             data = s.recv(1024)
    #             if not data:
    #                 break
    #             # here comes the logic after receiving an answer from the server.
    #             # another dict/function/class with functions/methods for possible responses?
    #             print("Received back:", data.decode())
    #             s.close()
    print('Done.')


if __name__ == '__main__':
    logger = logging.getLogger("iiarsee_client")
    logger.setLevel("INFO")
    # create file handler which logs even debug messages
    fh = logging.FileHandler('iiarsee_client.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info("__main__: starting the client")

    parser = argparse.ArgumentParser("iiarsee_client")
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

    logger.debug("__main__: set client arguments: %s", args)
    # the client also needs to have a "server" at all times listening to other clients possibly wanting to connect to them.
    # so we should have some sort of background listener running that interupts (? or what ever you call it) incase someone connects to it

    main(logger, args)
