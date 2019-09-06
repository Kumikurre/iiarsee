import socket
import time

from sqlalchemy import create_engine

import database_init


####### THE PROPRIETARY TCP-INTERFACE FOR COMMUNICATION #######
class socketInterface():
    pass

# class Channel(Base):
#     users = []

#     def user_join():
#         pass

#     def _broadcast():
#         pass 

#     def _receive():
#         pass

#     def receive_and_broadcast():
#         _receive()
#         _broadcast()

# class User(Base):
#     pass


####### THIS IS THE ACTUAL SERVER CLASS #######
class Server():
    users = []
    channels = []
    
    def __init__(self):
        print('Initializing database')
        engine = create_engine('mysql://tshatti:tshattipassu@db:3306')
        database_init.initialize(engine)

    def run(self):
        print('Server started')
        
if __name__ == '__main__':
    print('Starting server...')
    server = Server()
    server.run()
