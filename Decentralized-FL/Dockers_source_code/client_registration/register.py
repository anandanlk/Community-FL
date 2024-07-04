import requests
import json
import time
import pathlib
import os
from get_system_config import get_system_info_list

DISCOVERY_SERVER_URL = os.getenv('COMMUNICATION_IP', 'http://localhost') + ':8088'
directory = pathlib.Path(__file__).parent.resolve()

if 'localhost' in DISCOVERY_SERVER_URL or '127.0.0.1' in DISCOVERY_SERVER_URL:
    DISCOVERY_SERVER_URL = 'http://host.docker.internal:8088'

client_ip = requests.get('http://checkip.amazonaws.com/').text.strip()

host_directory = f'{directory}/files'

weights_file = next((f for f in os.listdir(f'{host_directory}/') if f.endswith('.pt')), None)

if weights_file is None:
    weights_file = 'client.pt'
    with open(f'{host_directory}/{weights_file}', 'w') as f:
        pass

data = {}

output_file = 'client_info.json'

if os.path.exists(f'{host_directory}/{output_file}'):
    with open(f'{host_directory}/{output_file}', 'r') as f:
        data = json.load(f)
else:
    data = {
        "last_seen": "0",
    }

data['weights'] = weights_file
data['client_ip'] = client_ip + ":3000"

with open(f'{host_directory}/{output_file}', 'w') as f:
    json.dump(data, f)

connection_file = f'{host_directory}/connection.json'
if not os.path.exists(connection_file):
    connection_data = {
        "uid": "Enter your UID here",
        "tags": ["MINST", "Decentralized", "Labelled"]
    }
    with open(connection_file, 'w') as f:
        json.dump(connection_data, f)

system_info = get_system_info_list()

while True:
    with open(f'{host_directory}/client_info.json') as fp:
        data.update(json.load(fp))
    
    with open(f'{host_directory}/connection.json') as f:
        connection_data = json.load(f)
        connection_data['tags'].extend(system_info)
    
    data.update(connection_data)

    response = requests.post(f'{DISCOVERY_SERVER_URL}/register', json=data)

    if response.status_code == 200:
        print('Service registered successfully')
    else:
        print(f'Error registering service: {response.text}')
    time.sleep(7)