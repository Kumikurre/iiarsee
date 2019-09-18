# The client logs in once in the beginning of the session (connection) and after that the server trusts the client for the life of that session (connection).

# During registration, if the username is taken etc. respond something to promt retry

# WAIT WHAT!? If we want to have authentication for peer-to-peer messages, we need to implement a system where the connecting user sends
# also a hash of its secret to the other user that the user 2 then verifies from the server and then they either
# 1. exchange a secret between each other and use that in the future to authenticate between each other
# 2. Blindly trust that connection for the duration of that session (connection) and redo the auth to server every time

commands = {
    "register": {
        "parameters": {
            "userId": "iWantThis!",
            "password": "notYourPassword"
        },
        "possible_responses": {
            "failed": "causes retry logic, username was in use or what ever",
            "success": "we good to go."
        }
    },
    "login": {
        "parameters": {
            "userId": "randomUser",
            "password": "salasana1"
        },
        "possible_responses": {
            "failed": "something went wrong :P",
            "success": "welcome"
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
            "failed": "channel doesn't exist",
            "success": "go!"
        }
    },
    "list_channels": {
        "response": "#list of channels"
    },
    "leave_channel": {

    },
    "discover_user": {
        "parameters": {
            "userId": "string"
        },
        "possible_responses": {
            "failed": "user doesn't exist",
            "success": "info of the user"
        }
    },
    "message_user": {
        "parameters": {
            "userId": "username of the sender, if we don't do auth, can be spoofed, but who cares.",
            "message": "bonjour"
        }
    }
}
# in the logic for message_user we need to take of user discovery if that hasn't been done before
# if we want to have authentication between users, we need another command to authenticate_user: {params: {"hash": <hash>}}


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

# sending the actual message over the socket, we just json.strigify(message) and send_all() over the socket.
# receiver reads the data, json.parse(data) and switch_cases (or what ever) with the command