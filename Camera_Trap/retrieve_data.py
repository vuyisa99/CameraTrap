import sqlite3

def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")

def readBlobData(empId):
    try:
        sqliteConnection = sqlite3.connect('CameraTrapRecords.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_fetch_blob_query = """SELECT * FROM CameraTrapRecords WHERE id = ?"""
        cursor.execute(sql_fetch_blob_query, (empId,))
        record = cursor.fetchall()
        for row in record:
            print("Id = ", row[0], "timestamp = ", row[1])
            Id = row[0] 
            timestamp = row[1]
            photo = row[7]
            #resumeFile = row[3]

            print("Storing image and timestamp on disk \n")
            photoPath = "/home/vuyisa/Documents/images/" + f'image{Id}.jpg'
            #resumePath = "E:\pynative\Python\photos\db_data\\" + name + "_resume.txt"
            writeTofile(photo, photoPath)
            #writeTofile(resumeFile, resumePath)

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")

readBlobData(64)