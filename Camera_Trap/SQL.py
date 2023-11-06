import sqlite3

# Connect to or create the database (change the filename as needed)
conn = sqlite3.connect('CameraTrapRecords.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table to store sensor data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS CameraTrapRecords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME,
        temperature REAL,
        humidity REAL,
        latitude REAL,
        longitude REAL,
        category_name TEXT NOT NULL,
        image BLOB NOT NULL
    )
''')

# Commit changes and close the database connection
conn.commit()
conn.close()