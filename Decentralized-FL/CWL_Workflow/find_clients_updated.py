import requests
import yaml
import json
import sys
import os
# Get the JSON response from the link
information_server_ip = sys.argv[1]

# response = requests.get(f'{information_server_ip}:8088/discover')
# json_data = response.json()

# Read from client_list.json instead of API
# json_file = 'client_list.json'
# with open(json_file, 'r') as f:
#     json_data = json.load(f)
json_data = [
  {
    "client_ip": "34.32.210.97:3000",
    "weights": "client_id1.pt",
    "last_seen": 1719937754
  },
  {
    "client_ip": "34.34.13.170:3000",
    "weights": "client_id2.pt",
    "last_seen": 1719937753
  }
]

# Extract the client IP and weights from the JSON data
clients = ['http://{}/{}'.format(item['client_ip'], item['weights']) for item in json_data]
#output the clients to the stdout
for client in clients: 
    print(client)

