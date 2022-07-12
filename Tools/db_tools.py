import sqlite3

def setup_logs_table(connection):
    cursed_obj = connection.cursor()
    cursed_obj.execute(f"""CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project TEXT,
    entry_type TEXT,
    work_value INT,
    rest_value INT,
    time_started DATE,
    time_stopped DATE,
    comments TEXT)""")

def insert_log(connection, project, entry_type, work_value, rest_value, time_started="0", time_stopped="0", comments="", print_output=False):
    try:
        cursed_obj = connection.cursor()
        if time_started != "0":
            sqlite_insert_with_param = """INSERT INTO logs
                          (project, entry_type, work_value, rest_value, time_started, comments) 
                          VALUES (?, ?, ?, ?, ?, ?);"""
            data_tuple = (project, entry_type, work_value, rest_value, time_started, comments)
        else:
            sqlite_insert_with_param = """INSERT INTO logs
                          (project, entry_type, work_value, rest_value, time_stopped, comments) 
                          VALUES (?, ?, ?, ?, ?, ?);"""
            data_tuple = (project, entry_type, work_value, rest_value, time_stopped, comments)
        cursed_obj.execute(sqlite_insert_with_param, data_tuple)
        connection.commit()
        if print_output: print("Python Variables inserted successfully into logs table")

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    # finally:
    #     if sqliteConnection:
    #         sqliteConnection.close()
    #         print("The SQLite connection is closed")


def check_db_tables(connection, print_activity = False):
    if print_activity: print('Checking if proper tables exist')
    setup_logs_table(connection)

def create_connection(db_file):
    """ create a database connection to a database that resides
        in the memory
    """
    conn = None;
    try:

        conn = sqlite3.connect(db_file)
        #conn = sqlite3.connect(":memory:")
        #print(f'sql version: {sqlite3.version}')
    except sqlite3.Error as e:
        print(e)
    finally:
        return conn


def close_connection(connection):
    cursed_obj = connection.cursor()
    cursed_obj.close()
