from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import socket
import json
import time
import os
from flask_cors import CORS
import subprocess

#Variables
NULL_CHAR = chr(0)

# Flag to control execution of `check_execute_script_setting`   
execute_script_flag = False 

#Functions
#Create write_report function t write HID codes to the HID Keyboard
def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())
time.sleep(4)
#"chr(0x4F) is =>"
#"chr(0x50) is <="
# Alt = chr(5)
# for i in range(100, 101):
#     time.sleep(2)
#     print(i)
#     write_report(chr(5) + NULL_CHAR + chr(100) + NULL_CHAR * 5)
#     write_report(NULL_CHAR * 8)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def is_usb_connected():
    print("Checking if USB is connected")
    try:
        if os.path.exists('/dev/hidg0'):
            print("Found hid0")
            # Try writing a test report to /dev/hidg0
            with open('/dev/hidg0', 'wb') as fd:
                fd.write(b'\x00')  # Write a test report
        # If the write operation succeeds, assume USB is connected
        print("USB is connected")
        return True
    except OSError:
        # If an OSError occurs, assume USB is not connected
        return False
print(is_usb_connected())

def type_text(text, speed):
    print("type_text called with" + text + " speed: " + str(speed))
    enter_keyword = "<enter>"
    windows_keyword = "<windows>"
    windowsR_keyword = "<windows+r>"
    end_keyword = "<end>"
    right_arrow = "<right>"
    enter_code = chr(40)  # ASCII code for Enter key

    #Custom commands
    for line in text.splitlines():
        time.sleep(1.8)
        line = line.strip()
        if line == enter_keyword:
            # Press Enter key
            write_report(NULL_CHAR * 2 + enter_code + NULL_CHAR * 5)
            write_report(NULL_CHAR * 8)
        elif line == windowsR_keyword:
            # Press Windows+R key
            write_report(chr(8)+NULL_CHAR+chr(21)+NULL_CHAR*5)
            write_report(NULL_CHAR * 8)
        elif line == windows_keyword:
            # Press Windows key
            write_report(chr(8) + NULL_CHAR * 7)
            write_report(NULL_CHAR * 8)
        elif line == right_arrow:
            write_report(NULL_CHAR * 2 + chr(0x50) + NULL_CHAR * 5)
            write_report(NULL_CHAR * 8)
        elif line == end_keyword:
            break
        else:
            for char in line:
                time.sleep(0.05)
                #Check for space
                
                if char.isalpha():
                    char_upper = char.upper()
                    if char == char_upper:
                        print(f"Uppercase {char}")
                        # Press the corresponding uppercase letter key
                        write_report(chr(2) + NULL_CHAR + chr(ord(char) - ord('A') + 4) + NULL_CHAR * 5)
                        write_report(NULL_CHAR * 8)
                    # Checks if not digit but a lowercase letter
                    elif char != char_upper and char.isalpha():
                        print(f"Lowercase {char}")
                        # Press the corresponding lowercase letter key
                        write_report(NULL_CHAR * 2 + chr(ord(char_upper) - ord('A') + 4) + NULL_CHAR * 5)
                        write_report(NULL_CHAR * 8)
                elif char.isdigit():
                    if char == "0":
                        #Needed to hardcode 0 due to strange offset
                        write_report(NULL_CHAR * 2 + chr(39) + NULL_CHAR * 5)
                        write_report(NULL_CHAR * 8)
                    else:
                        print(f"Digit {char}")
                        # Press the corresponding number key, offset with 1
                        write_report(NULL_CHAR * 2 + chr(ord(char) - ord('0') + 30 - 1) + NULL_CHAR * 5)
                        write_report(NULL_CHAR * 8)
                elif char == ' ':
                    # Press the Spacebar key
                    print(f"Spacebar {char}")
                    write_report(NULL_CHAR * 2 + chr(44) + NULL_CHAR * 5)
                    write_report(NULL_CHAR * 8)
                #Catching ' " ' character
                elif char == '\u0022':
                    print(f"Double quote {char}")
                    write_report(chr(2)+NULL_CHAR+chr(31)+NULL_CHAR*5) ## Shift + key
                    write_report(NULL_CHAR * 8)
                else:
                    # Handle special characters based on their ASCII values
                    special_char_codes = {
                        '(': 37, ')':38,'!': 30, '#': 32, '$': 33, '%': 34, '^': 35,
                        '/': 36, '-': 56,
                        '=': 39, '+': 46, '[': 47, ']': 48, '}': 48,
                        '\\': 100, '|': 999, ';': 51, ':': 55, "'": 50, '"': 31,
                        ',': 54, '<': 54, '.': 55, '?': 45
                    }
                    if char in special_char_codes:
                        # Press the corresponding special character key
                        if char in ['.', '-', "'"]:
                            print("Special character no shift")
                            write_report(NULL_CHAR * 2 + chr(special_char_codes[char]) + NULL_CHAR * 5)
                            write_report(NULL_CHAR * 8)
                        elif char in ['$', '\\']:
                            #AltGr Alt
                            write_report(chr(5) + NULL_CHAR + chr(special_char_codes[char]) + NULL_CHAR * 5)
                        else:
                            print("Special character with shift")
                            write_report(chr(2) + NULL_CHAR + chr(special_char_codes[char]) + NULL_CHAR * 5)
                            write_report(NULL_CHAR * 8)
                        write_report(NULL_CHAR * 8)
                        print(f"Typed {char} with ASCII value {special_char_codes[char]}")
        # Add a small delay between lines
        time.sleep(0.1)
    global execute_script_flag
    execute_script_flag = False 

# Delay for a few seconds to ensure the system recognizes the keyboard
time.sleep(3)


# Checks if the setting to execute on project start up is true, or is called by socketio in the executeScript() function
def check_execute_script_setting(source=None):
    print("check_execute_script_setting")
    with open('/var/www/duck/ducktor/settings.json', 'r') as file:
        print("opened settings")
        try:
            print("loading json")
            settings = json.load(file)
            print(settings)
        except Exception as e:
            print (e)

    #If the setting to execute on boot is true it runs, or if the function was called with socketio it runs
    if settings.get('execute_script') and settings.get('duck_file') and is_usb_connected() or source =='socketio' and is_usb_connected():
        print("Check settings if statement true")
        duck_file_path = os.path.join(os.path.dirname(__file__)+"/duckScripts/", settings['duck_file'])
        with open(duck_file_path, 'r') as file:
            text_to_type = file.read()
            #Use with care
            print("Prompt setting loop is= " + str(settings.get('prompt_loop')))
            while settings.get('prompt_loop') and is_usb_connected():
                print("Looping prompt")
                type_text(text_to_type, settings.get('speed'))
                time.sleep(1)  # Add a small delay to avoid high CPU usage
            else:
                print("Single time prompt")
                type_text(text_to_type, settings.get('speed'))
                #type_text(text_to_type)
    
# Listens on "execute" emit from frontend javascript socketio
@socketio.on('execute')
def executeScript():
    print("Execute script called")
    global execute_script_flag
    if not execute_script_flag:
        execute_script_flag = True
        print("Calling check_execute_script_setting() to execute script")
        check_execute_script_setting(source='socketio')
    else:
        print("Script execution already in progress")

@app.route('/')
def settings():
    return render_template('settings.html')

# Saves settings to settings.json file, and creates one if there is no present file located
@app.route('/save_settings', methods=['POST'])
def save_settings():
    print("Save settings called")
    settings = {
        'execute_script': False,
        'duck_file': '',
        'prompt_loop': False,
        'speed': 500,
    }

    # Create file with default settings if it does not exist
    if not os.path.exists('settings.json'):
        print("Making settings.json")
        with open('settings.json', 'w') as file:
            json.dump(settings, file)

    # Load existing settings
    with open('settings.json', 'r') as file:
        print("Writing to json settings")
        loaded_settings = json.load(file)
        settings.update(loaded_settings)

    # Update the settings with form data
    if 'execute_script' in request.form:
        settings['execute_script'] = request.form.get('execute_script') == 'True'
    if 'duck_file' in request.form:
        settings['duck_file'] = request.form['duck_file']
    if 'prompt_loop' in request.form:
        settings['prompt_loop'] = request.form.get('prompt_loop') == 'True'
    if 'speed' in request.form:
        settings['speed'] = int(request.form['speed'])

    # Save the updated settings
    with open('settings.json', 'w') as file:
        json.dump(settings, file)

    return jsonify({'message': 'Settings saved successfully'})

# Log generation
def write_log(log):
    try:
        with open('/var/www/duck/ducktor/flask_startup_log.json', 'w') as file:
            json.dump(log, file)
    except Exception as e:
        print(f"Error writing log file: {e}")

if __name__ == '__main__':
    log = {}
    try:
        print("Trying to check settings")
        ##check_execute_script_setting()
        ip_address = socket.gethostbyname(socket.gethostname())
        # Print the IP address
        print("Raspberry Pi IP address:", ip_address ,":5000")
        #In order for socket io to work we have to enable cross origin, not dangerous as its on localhost
        CORS(app, resources={r"/*":{"origins":"*"}})
        #app.run(host='0.0.0.0', port=5000)
        log['status'] = "starting"
        log['message'] = "Starting flask app"
        write_log(log)
        socketio.run(app, host="0.0.0.0", port="5000",allow_unsafe_werkzeug=True)
    except Exception as e:
        log['status'] = 'error'
        log['message'] = str(e)

        write_log(log)

    
