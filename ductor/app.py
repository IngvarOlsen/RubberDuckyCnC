from flask import Flask, render_template, request, jsonify
import json
import time
import os


#Program variables
LIST    = 1     #If LIST is 1 than complete keymap code is shown on screen
EXECUTE    = 1     #If EXECUTE is 1 than complete keymap code is send to the HID device and executed

#Variables
NULL_CHAR = chr(0)

#Functions
#Create write_report function t write HID codes to the HID Keyboard
def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

# time.sleep(4)
# #Ascii for numpad -
# # For loop which itaretes through 5 keys at time to find the - key
# for i in range(40,60):
#     #write_report(chr(2)+NULL_CHAR+chr(i)+NULL_CHAR*5) ## Shift + key
#     write_report(NULL_CHAR * 2 + chr(i) + NULL_CHAR * 5) ## Without shift
    
#     write_report(NULL_CHAR * 8)
# #write_report(chr(2)+NULL_CHAR+chr(46)+NULL_CHAR*5)¨

# #write_report(NULL_CHAR * 2 + chr(55) + NULL_CHAR * 5)
# write_report(NULL_CHAR * 8)
# TESTING Ascii code for ' is 50
# write_report(NULL_CHAR*2+chr(50)+NULL_CHAR*5) ## Shift + key
# write_report(NULL_CHAR * 8)
# exit()

def type_text(text):
    enter_keyword = "<enter>"
    windows_keyword = "<windows>"
    windowsR_keyword = "<windows+r>"
    end_keyword = "<end>"
    enter_code = chr(40)  # ASCII code for Enter key

    #Custom commands
    for line in text.splitlines():
        time.sleep(0.4)
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
        elif line == end_keyword:
            break
        else:
            for char in line:
                time.sleep(0.2)
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
                        '/': 36, '-': 56, '_': 45,
                        '=': 39, '+': 46, '[': 47, ']': 48, '}': 48,
                        '\\': 49, '|': 49, ';': 51, ':': 55, "'": 50, '"': 31,
                        ',': 54, '<': 54, '.': 55, '?': 45
                    }
                    if char in special_char_codes:
                        # Press the corresponding special character key
                        if char in ['.', '-', "'"]:
                            print("Special character no shift")
                            write_report(NULL_CHAR * 2 + chr(special_char_codes[char]) + NULL_CHAR * 5)
                            write_report(NULL_CHAR * 8)
                        else:
                            print("Special character with shift")
                            write_report(chr(2) + NULL_CHAR + chr(special_char_codes[char]) + NULL_CHAR * 5)
                            write_report(NULL_CHAR * 8)
                        write_report(NULL_CHAR * 8)
                        print(f"Typed {char} with ASCII value {special_char_codes[char]}")
        # Add a small delay between lines
        time.sleep(0.1)

# Delay for a few seconds to ensure the system recognizes the keyboard
time.sleep(3)


# Checks if the setting to execute on project start up is true
def check_execute_script_setting():
    with open('/var/www/duck/ductor/settings.json', 'r') as file:
        settings = json.load(file)

    if settings.get('execute_script') and settings.get('duck_file'):
        duck_file_path = os.path.join(os.path.dirname(__file__)+"/duckScripts/", settings['duck_file'])
        with open(duck_file_path, 'r') as file:
            text_to_type = file.read()
            type_text(text_to_type)


app = Flask(__name__)


@app.route('/')
def settings():
    return render_template('settings.html')

@app.route('/save_settings', methods=['POST'])
def save_settings():
    settings = {
        'execute_script': False,
        'duck_file': ''
    }

    if 'execute_script' in request.form:
        settings['execute_script'] = True

    if 'duck_file' in request.form:
        settings['duck_file'] = request.form['duck_file']

    with open('settings.json', 'w') as file:
        json.dump(settings, file)

    return jsonify({'message': 'Settings saved successfully'})


if __name__ == '__main__':

    check_execute_script_setting()

    app.run(host='0.0.0.0', port=5000)
