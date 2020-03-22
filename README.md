# iiarsee
Distributed chat system with server-client architecture. 

## How to start (requires *NIX operating system, good luck if you use windows)
Create a python virtualenv:
```
virtualenv env
```

Activate virtuane environment:
```
source env/bin/activate
```

Install dependencies to the virtualenv:
```
pip install -r ./client/requirements.txt
```

Run the server and client (in a different terminal or machine):
```
python ./server/server.py
python ./client/client.py --address <server_address> --port <server_port> --client_port <client_port>
```

## Docs
https://drive.google.com/drive/folders/1ZDsQJ17zLuiBYE5VebH6TFDyHK6yb_sk?usp=sharing

Older folder: https://drive.google.com/drive/folders/1NUd_iwhmTALR-qohe0_RFurxrbugoi2c?usp=sharing
