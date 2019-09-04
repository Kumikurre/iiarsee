import socket
from sqlalchemy import create_engine



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
    def run(self):
        while True:
            pass


if __name__ == '__main__':
    engine = create_engine('mysql://tshatti:tshattipassu@localhost:3306')
    server = Server()
    server.run()
