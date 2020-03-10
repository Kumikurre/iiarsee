commands = {
    "register_client": {
        "parameters": {
            "client_name": "client1"
        },
        "possible_responses": {
            "success": "you gots the name",
            "error": "name already in use"
        }
    },
    "send_message": {
        "parameters": {
            "message": "Hello world",
            "channel": "the batcave"
        }
    },
    "join_channel": {
        "parameters": {
            "channel_name": "batcave"
        },
        "possible_responses": {
            "success": "OK"  # if the channel doesn't exist we create it
        }
    },
    "leave_channel": {
        "parameters": {
            "channel_name": "batcave"
        },
        "possible_responses": {
            "success": "byebye",
            "error": "you not in such channel fool"
        }
    },
    "discover_user": {
        "parameters": {
            "userId": "string"
        },
        "possible_responses": {
            "error": "404",
            "success": "info of the user"
        }
    },
    "message_user": {
        "parameters": {
            "client_name": "name of the client to send the message to",
            "message": "bonjour"
        }
    },
    "quit_message": {
        "parameters": {
            "client_name": "client2"
        }
    }
}

message = {
    "command": "<command for the recipient to know what this is about, switch case?>",
    "parameters": {
        "userId": "<senders user id / name>",
        "param1": "these are command specific and may vary",
        "param2": "more information",
        "channel_name": "exampleChannel",
        "message": "If you e.g. have command send_message"
    }
}

response = {
    "status": "OK/NOK",
    "optional_parameter": "e.g. client_address"
}

# sending the actual message over the socket, we just json.strigify(message) and send_all() over the socket.
# receiver reads the data, json.parse(data) and switch_cases (or what ever) with the command
