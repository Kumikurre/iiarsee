import asyncio
import argparse
import json
import logging
import socket
import prompt_toolkit
import sys
import nest_asyncio
from datetime import datetime

nest_asyncio.apply()

#### CONSTANTS:
client_session = None
username = prompt_toolkit.prompt("Register as: ")
client_start_message = f"Welcome to iiarsee {username}. Press [Ctrl-Q] to quit.\n Commands: /read_channel /read_client /msg_channel /msg_client /join_channel /leave_channel"
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
    def __init__(self, logger, args, client_name):
        self.logger = logger
        self.client_name = client_name
        self.channels = {}
        # channels = {
        #   "channel1": [{timestamp: <timestamp>, client_name: <client_name>, message: <informative message>"}],
        #   "channel2": []
        # }
        # 
        self.server_addr = args.address
        self.server_port = args.port
        self.client_port = args.client_port
        self.clients = {}
        # clients {
        #   "client1": {
        #       "address": "127.0.0.1",
        #       "messages": [],
        #       "state": "INACTIVE"
        #   }
        # }
        self.logger.debug(f"ClientSession.__init__(): initializing client {self.client_name} with arguments: {args}")
        # init the event loop for whole client to server
        self.loop = asyncio.get_event_loop()
        # data = self.loop.run_until_complete(self.tcp_client("127.0.0.1", 8666, message, self.loop))
        # loop.close()
        # init the client side server for receiving new messages and talking to other clients
        client_server = asyncio.start_server(self.client_server, "0.0.0.0", self.client_port, loop=self.loop)
        # self.server = self.loop.run_until_complete(client_server)
        # self.loop.create_task(client_server)
        asyncio.ensure_future(client_server)

        # start the server and run it in the background (we have no controls over it basically)
        # asyncio.create_task(self.client_server())
        message = {"operation":"register_client",
                   "client_name": self.client_name,
                   "client_port": self.client_port}
        # register the client to server, hardcoded defaults
        register_return = self.loop.run_until_complete(self.tcp_client(self.server_addr, self.server_port, message, self.loop))
        self.logger.debug(f"ClientSession.__init__(): registered client to server, received response: {register_return}")
        if register_return["status"]:
            raise RuntimeError("The given username was already in use")

    async def client_server(self, reader, writer):
        data = await reader.read(1000)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        addr = addr[0] + ':' + str(addr[1])
        self.logger.info(f'client_server(): Received {message} from {addr}')

        try:
            parsed_data = json.loads(message)
        except Exception as e:
            parsed_data = None
            answer = {
                'status': 1,
                'statusmessage': str(e)
                }
            self.logger.info(f'JSON parsing failed for received message')

        # Call the correct method with data parsed from JSON
        if parsed_data:
            operation = parsed_data.get('operation')
            client_name = parsed_data.get('client_name')
            channel_name = parsed_data.get('channel_name')
            message = parsed_data.get('message')
            sender = parsed_data.get('sender')
            # do the operations here? receive messages mainly...
            # if we have a channel name, assume its from the server
            if channel_name:
                self.logger.info(f'client_server(): received a message {message} for channel {channel_name}')
                self.channels.setdefault(channel_name, {"messages": []})
                self.channels[channel_name]['messages'].append(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': <' + sender + '>: ' + message) # should we have timestamps?
                self.logger.debug(f'!!!client_server(): channel messages after assignment: {self.channels[channel_name]["messages"]}')


            # if we have client name its from another client, yes we have no security here... (giggle)
            elif client_name:
                self.logger.info(f'client_server(): received a message {message} from client {client_name}')
                self.clients.setdefault(client_name, {"messages": []})
                self.clients[client_name]['messages'].append(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': <' + client_name + '>: ' + message)
                self.logger.debug(f'!!!client_server(): channel messages after assignment: {self.clients[client_name]["messages"]}')

        answer = {'status': 0}  # rok rok
        writer.write(json.dumps(answer).encode('utf-8'))
        await writer.drain()

        self.logger.info('Close the client socket')
        writer.close()


    # @staticmethod
    async def tcp_client(self, address, port, message, loop):
        reader, writer = await asyncio.open_connection(address, port, loop=loop)

        self.logger.debug(f"tcp_client(): sending message {message} to address {address} on port {port}")
        if type(message) is not str:
            message = json.dumps(message)
        writer.write(message.encode())

        data = await reader.read(1000)
        self.logger.debug(f"tcp_client(): received response: {data}")

        self.logger.debug("tcp_client(): closing client")
        writer.close()
        return json.loads(data)

    def read_channel_messages(self, channel_name, rows=5):
        """Prints n last messages for given channel"""
        if channel_name in self.channels:
            new_text = "\n"
            for row in self.channels[channel_name]['messages'][-rows:]:
                # "add to the top"
                new_text = str(row) + "\n" + new_text
            new_text = chat_field.text + new_text
            chat_field.buffer.document = prompt_toolkit.document.Document(text=new_text, cursor_position=len(new_text))
        else:
            new_text = chat_field.text + "\nChannel not found\n"
            chat_field.buffer.document = prompt_toolkit.document.Document(text=new_text, cursor_position=len(new_text))
        return "End of messages"


    def read_client_messages(self, client_name, rows=5):
        """Prints n last messages for given client"""
        if client_name in self.clients:
            new_text = "\n"
            for row in self.clients[client_name]['messages'][-rows:]:
                # "add to the top"
                new_text = str(row) + "\n" + new_text
            new_text = chat_field.text + new_text
            chat_field.buffer.document = prompt_toolkit.document.Document(text=new_text, cursor_position=len(new_text))
        else:
            new_text = chat_field.text + "\nClient not found\n"
            chat_field.buffer.document = prompt_toolkit.document.Document(text=new_text, cursor_position=len(new_text))
        return "End of messages"

    def message_channel(self, channel_name, msg):
        """Sends a message to a given channel on the server"""
        self.logger.info("ClientSession.message_channel(): sending a message %s to channel %s", msg, channel_name)
        message = {"operation":"message_channel",
                   "client_name": self.client_name,
                   "channel_name": channel_name,
                   "message": msg,
                   "client_port": self.client_port}
        response = self.loop.run_until_complete(self.tcp_client(self.server_addr, self.server_port, message, self.loop))
        self.logger.info("ClientSession.message_channel(): sent message to channel, received response: %s", response)
        if response["status"]:
            # failed to send the message
            return "Failed to send the message"
        return "Message sent"

    def message_client(self, client_name, msg): # this needs  fixing
        """Sends a message to a given client"""
        self.logger.info("ClientSession.message_client(): sending message to client %s, resolving address first", client_name)
        client_address = self._find_client_address(client_name)
        self.logger.info("ClientSession.message_channel(): sending message %s to client %s in addr %s", msg, client_name, client_address)
        message = {"operation":"message_client",
                   "client_name": self.client_name,
                   "message": msg,
                   "client_port": self.client_port}
        client_address, client_port = client_address.split(":")
        response = self.loop.run_until_complete(self.tcp_client(client_address, client_port, message, self.loop))  # We probably should not hardcode the client port but instead get it from the server? dunno...
        # new_text = chat_field.text + "\n" + response.decode()
        # chat_field.buffer.document = prompt_toolkit.document.Document(text=new_text, cursor_position=len(new_text))
        #client_address = self._find_client_address()
        if response["status"]:
            # failed to send the message
            return "Failed to send the message."
        # append the message to messages on our side
        self.clients.setdefault(client_name, {"messages": []})
        self.clients[client_name]['messages'].append(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': <' + self.client_name + '>: ' + message)
        return "Message sent"


    def receive_message_server(self):
        """Handle receiving of message from server"""
        # Ummm... I suppose the server knows our address and the port we have for communicating to it...
        # but is the socket actually open when we are not actively sending a message to the server?
        # Do we actually need the client-side server implementation also for this to work? :P
        pass

    def receive_message_client(self):
        """Handle receiving of message from clients"""
        # I suppose we need to have a asyncio server active for receiving messages from other clients,
        # in other words we need to impelent also a server
        pass

    def join_channel(self, channel_name):
        """Joins a given channel on the server"""
        self.logger.info("ClientSession.join_channel(): joining channel %s on the server", channel_name)
        message = {"operation":"join_channel",
                   "client_name": self.client_name,
                   "channel_name": channel_name,
                   "client_port": self.client_port}
        response = self.loop.run_until_complete(self.tcp_client(self.server_addr, self.server_port, message, self.loop))
        self.logger.info("ClientSession.join_channel(): joined channel %s, received response: %s", channel_name, response)
        if response["status"]:
            # failed to send the message
            return "Failed to join the channel"
        return "joined channel " + channel_name


    def leave_channel(self, channel_name):
        """Leaves a given channel on the server"""
        self.logger.info("ClientSession.join_channel(): leaving channel %s on the server", channel_name)
        message = {"operation":"leave_channel",
                   "client_name": self.client_name,
                   "channel_name": channel_name,
                   "client_port": self.client_port}
        response = self.loop.run_until_complete(self.tcp_client(self.server_addr, self.server_port, message, self.loop))
        self.logger.info("ClientSession.join_channel(): leaved channel %s, received response: %s", channel_name, response)
        if response["status"]:
            # failed to send the message
            return "Failed to leave the channel"
        return "left channel " + channel_name

    def quit_client(self, app):
        """Sends a "remove_client" message to the server and other clients in the clients object"""
        message = {"operation": "remove_client",
                   "client_name": self.client_name,
                   "client_port": self.client_port}
        # register the client to server, hardcoded defaults
        data = self.loop.run_until_complete(self.tcp_client(self.server_addr, self.server_port, message, self.loop))
        self.logger.debug("ClientSession.quit_client(): sent remove_client message to server, received response: %s", data)

        # last
        self.loop.stop()
        self.loop.close()
        self.logger.debug("ClientSession.quit_client(): quitting client")
        app.exit()
        # send also quit message to whole client_address_book -> client removed from client_address_book

    def _find_client_address(self, client_name):
        """Find a given client"s true network address from the server"""
        self.logger.info("ClientSession.join_channel(): finding address for client %s", client_name)
        message = {"operation":"find_client",
                   "search_name": client_name,
                   "client_port": self.client_port}
        response = self.loop.run_until_complete(self.tcp_client(self.server_addr, self.server_port, message, self.loop))
        self.logger.info("ClientSession.join_channel(): found address for client %s, response: %s", client_name, response)
        # what if the client is not found?
        return response["address"]


def handle_input(buff):
    """Handler for accepting user input"""
    new_text = chat_field.text + "\n" + input_field.text
    chat_field.buffer.document = prompt_toolkit.document.Document(text=new_text, cursor_position=len(new_text))

    user_input = input_field.text.split()
    try:
        operation = str(user_input[0])
        if len(user_input) > 1:
            opt_parameter = str(user_input[1])
        if len(user_input) > 2:
            message = " ".join(map(str, user_input[2:]))

        if operation == "/read_channel":
            new_text = client_session.read_channel_messages(opt_parameter)
        elif operation == "/read_client":
            new_text = client_session.read_client_messages(opt_parameter)
        elif operation == "/msg_channel":
            new_text = client_session.message_channel(opt_parameter, message)
        elif operation == "/msg_client":
            new_text = client_session.message_client(opt_parameter, message)
        elif operation == "/join_channel":
            new_text = client_session.join_channel(opt_parameter)
        elif operation == "/leave_channel":
            new_text = client_session.leave_channel(opt_parameter)
        elif operation == "/quit":
            client_session.quit_client(application)
        else:
            logger.error("invalid operation: %s", operation)
            new_text = "Invalid operation\n"
        if not new_text:
            new_text = "invalid return text from operaration " + operation
        new_text = chat_field.text + "\n" + new_text
        chat_field.buffer.document = prompt_toolkit.document.Document(text=new_text, cursor_position=len(new_text))

    except Exception as e:
        logger.debug(f"failed to parse user input {user_input} with error {e}")

# Create the layout
chat_field = prompt_toolkit.widgets.TextArea()
input_field = prompt_toolkit.widgets.TextArea(
        height=1,
        prompt=">>> ",
        style="class:input-field",
        multiline=False,
        wrap_lines=False,
        accept_handler=handle_input,
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
        padding_char="_"),
    ], 
    padding=1, 
    padding_char="_")

input_field.accept_handler = handle_input

# Add keybinds to make user's life easier
# Ctrl+C and Ctrl+Q: exit application
kb = prompt_toolkit.key_binding.KeyBindings()
@kb.add("c-c", eager=True)
@kb.add("c-q", eager=True)
def _(event):
    """Pressing Ctrl-Q or Ctrl-C will exit the user interface."""
    client_session.quit_client(event.app)
    # event.app.exit()

# Create an "Application" instance
application = prompt_toolkit.application.Application(
    layout=prompt_toolkit.layout.layout.Layout(root_container, focused_element=input_field),
    key_bindings=kb,
    mouse_support=True,
    full_screen=True)


if __name__ == "__main__":
    logger = logging.getLogger("iiarsee_client")
    logger.setLevel("INFO")
    # create file handler which logs even debug messages
    fh = logging.FileHandler(f"iiarsee_client_{username}.log")
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    # ch = logging.StreamHandler()
    # ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    # ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    # logger.addHandler(ch)

    logger.info("__main__: starting the client")

    parser = argparse.ArgumentParser("iiarsee_client")
    parser.add_argument("--debug", help="Enable debugging")
    parser.add_argument("--address", help="IP addrss for the server")
    parser.add_argument("--port", help="Which port to connect to", type=int)
    parser.add_argument("--client_port", help="Port for inter-client connections", type=int)

    args = parser.parse_args()
    # default to local host if no arguments given
    if not args.address:
        args.address = "127.0.0.1"
    if not args.port:
        args.port = 8666
    if not args.client_port:
        args.client_port = 8777
    # if args.debug:
    # default debugging...
    logger.setLevel("DEBUG")

    logger.debug("__main__: set client arguments: %s", args)
    # the client also needs to have a "server" at all times listening to other clients possibly wanting to connect to them.
    # so we should have some sort of background listener running that interupts (? or what ever you call it) incase someone connects to it

    client_session = ClientSession(logger, args, username)
    application.run()
