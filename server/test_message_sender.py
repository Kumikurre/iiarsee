import socket
import json

TCP_IP = '127.0.0.1'
TCP_PORT = 8666
BUFFER_SIZE = 1024
MESSAGE = {'operation':'register_client',
                   'client_name':'dsa'}
        
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(json.dumps(MESSAGE).encode('utf-8'))
data = s.recv(BUFFER_SIZE)
s.close()

print("received data:", data)

