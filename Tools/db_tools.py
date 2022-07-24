from datetime import datetime
import sqlite3


def gen_stat_query(work_type, start_date, end_date, project="None") -> str:
    if 'work' in work_type:
        if project == 'None':
            # query = "SELECT datetime(time_started,'unixepoch'), project, work_value, rest_value, entry_type " \
                # "FROM logs WHERE datetime(time_started, 'unixepoch') " \
            query = "SELECT time_started, project, work_value, rest_value, entry_type " \
                "FROM logs WHERE time_started " \
                f"BETWEEN '{start_date}' AND '{end_date}' AND entry_type LIKE '{work_type}'"
        else:
            # query = "SELECT datetime(time_started,'unixepoch'), project, work_value, rest_value, entry_type " \
                # "FROM logs WHERE datetime(time_started, 'unixepoch') " \
            query = "SELECT time_started, project, work_value, rest_value, entry_type " \
                "FROM logs WHERE time_started " \
                f"BETWEEN '{start_date}' AND '{end_date}' AND project LIKE '%{project}%' AND entry_type LIKE '{work_type}'"
    elif 'rest' in work_type:
        if project == 'None':
            # query = "SELECT datetime(time_started,'unixepoch'), project, work_value, rest_value, entry_type " \
                # "FROM logs WHERE datetime(time_started, 'unixepoch') " \
            query = "SELECT time_started, project, work_value, rest_value, entry_type " \
                "FROM logs WHERE time_started " \
                f"BETWEEN '{start_date}' AND '{end_date}' AND entry_type LIKE '{work_type}'"
        else:
            # query = "SELECT datetime(time_started,'unixepoch'), project, work_value, rest_value, entry_type " \
                # "FROM logs WHERE datetime(time_started , 'unixepoch') " \
            query = "SELECT time_started, project, work_value, rest_value, entry_type " \
                "FROM logs WHERE time_started " \
                f"BETWEEN '{start_date}' AND '{end_date}' AND project LIKE '%{project}%' AND entry_type LIKE '{work_type}'"
    return query


def get_stats(connection, start_date, end_date, project="None"):
    cursed_obj = connection.cursor()

    # Get Work Stats
    if project == 'None':
        print('Getting Stats for All Projects')
        query = gen_stat_query('work', start_date, end_date)
    else:
        print(f'Getting Stats for Project: {project}')
        query = gen_stat_query('work', start_date, end_date, project=project)


    time_worked = 0
    for i in cursed_obj.execute(query):
        time_worked += i[2]
    t_w = time_worked

    if time_worked > 60:
        t = ""
        t_h = time_worked // 60
        t_m = time_worked % 60
        time_worked = f'{t_h} Hour(s) and {t_m} Minutes'
    else:
        t = " (Min)"
    if project == 'None': 
        print(f'All Projects Worked{t}: {time_worked}')
    else:
        print(f'{project} Project Worked{t}: {time_worked}')

    connection.commit()
    # Get Rest Stats
    if project == 'None':
        query = gen_stat_query('rest', start_date, end_date)
    else:
        query = gen_stat_query('rest', start_date, end_date, project)

    # print(f'query: {query}')
    time_rested = 0
    for i in cursed_obj.execute(query):
        time_rested += i[3]
    t_r = time_rested
    connection.commit()

    if project == 'None': 
        print(f'All Projects Rest Time (Min): {time_rested}')
    else:
        print(f'{project} Project Rest Time (Min): {time_rested}')

    total_time = t_w + t_r
    if total_time > 60:
        t = ""
        t_h = total_time // 60
        t_m = total_time % 60
        total_time = f'{t_h} Hour(s) & {t_m} Minutes'
    else:
        t = " (Min)"

    if project == 'None': 
        print(f'All Projects Total Time{t}: {total_time}')
    else:
        print(f'{project} Project Total Time{t}: {total_time}')


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
    comments TEXT, entry_id TEXT)""")


def update_log(connection, cur_time):
    try:
        cursed_obj = connection.cursor()
        query = "SELECT id, time_started FROM logs WHERE id=(SELECT MAX(ID) FROM logs);"
        entry = cursed_obj.execute(query).fetchall()
        e_id = list(zip(*entry))[0]
        # need to update stop time by id
        query = f"UPDATE logs SET time_stopped = '{cur_time}' WHERE id = '{e_id[0]}'" 
        cursed_obj.execute(query)
        connection.commit()
    except sqlite3.Error as error:
        print("Failed to get latest entry table", error)

    

def insert_log(connection, project, entry_type, work_value, rest_value, time_started="0", time_stopped="0", comments="", entry_id="", print_output=False):
    try:
        cursed_obj = connection.cursor()
        sqlite_insert_with_param = """INSERT INTO logs
                        (project, entry_type, work_value, rest_value, time_started, time_stopped, comments, entry_id) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""
        data_tuple = (project, entry_type, work_value, rest_value, time_started, time_stopped, comments, str(entry_id))
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
