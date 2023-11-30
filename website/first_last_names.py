import sqlite3

global first_names, last_names
first_names = []
last_names = []


def load_names():
    try:
        sqliteConnection = sqlite3.connect('website\database.db')
        cursor = sqliteConnection.cursor()

        sqlite_select_Query = """SELECT first_name,last_name from User"""
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        for i in record:
            first_names.append(i[0])
            last_names.append(i[1])

        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
