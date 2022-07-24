from datetime import datetime, timedelta
import os
import subprocess
import sys
import argparse
import time
import hashlib

from sys import platform
from Tools import db_tools as _db
from Tools import misc as _utilities

# j_TODO : Look into this for Linux notification
#libnotify-bin

def main():
    parser = argparse.ArgumentParser(description='A tutorial of argparse!')
    parser.add_argument("-p", '--project', type=str, help="'p' Variable is "\
                            "for setting which project")
    parser.add_argument("-c", '--comment', type=str, help="'c' Variable is "\
                            "for what this session is about")
    parser.add_argument("-t", '--time', type=str, help="'t' Variable is for "\
                        "setting a custom work time, you must use 'r' for "\
                        "rest time to use this, value takes int and it is "\
                            "default by minute")
    parser.add_argument("-r", '--rest', type=str, help="'r' Variable is "\
                        "with 't' or '--time', this is the rest time or "\
                        "break after work time, value takes int and it "\
                            "is default by minute")
    parser.add_argument('--stats', type=str, help="'--stats' needs date "\
                        "range yyyy/mm/dd or \"today\" or \"week\" you "\
                        "can add -1 to week to get previous")
    parser.add_argument("--h", action="store_const", const=10,
                        help="This is the 'h' variable")

    args = parser.parse_args()
    p = args
    if p.project is None or p.project is type(None): p.project=""
    if p.comment is None or p.comment is type(None): p.comment=""
    if p.stats is None or p.stats is type(None): p.stats=""
    if p.time is None or p.time is type(None): p.time=""
    if p.rest is None or p.rest is type(None): p.rest=""
    if len(p.rest) > 0 and p.time == "":
        print('You must use Time with Rest')
        exit
    if len(p.time) > 0 and p.rest == "":
        print('You must use Rest with Time')
        exit
    h = args.h

    # Beginning SQL Check
    conn = _db.create_connection('work_logs.db')
    _db.check_db_tables(conn)

    # Defaults
    if len(p.time) > 0:
        work_value = int(p.time)
        rest_value = int(p.rest)
    else:
        work_value = 25
        rest_value = 8
    
    # If stats is called analytical functionality begins instead of primary
    if(len(p.stats) > 0):
        a_inf = p.stats
        if ',' in a_inf:
            a_inf = a_inf.split(',')
            if(len(p.project) > 0):
                _db.get_stats(conn, start_date=a_inf[0], end_date=a_inf[1])
            else:
                _db.get_stats(conn, start_date=a_inf[0], end_date=a_inf[1], project=p.project)
        elif p.stats == 'today':
            # j_TODO : have a better solution for getting todays date and adding extra day for end day
            start_day = datetime.today().strftime('%Y-%m-%d')
            res = (datetime.strptime(start_day, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
            end_day = datetime.strptime(res, "%Y-%m-%d")
            ed_str = end_day.strftime("%Y-%m-%d")
            if(len(p.project) > 0):
                _db.get_stats(conn, start_date=start_day, end_date=ed_str, project=str(p.project))
            else:
                _db.get_stats(conn, start_date=start_day, end_date=ed_str)
    else:
        # Start main functionality
        if(len(p.project) > 0):
            # print(f'p = {p.project} type({type(p.project)}) = len: {len(p.project)}')
            run_timer(conn, work_value, rest_value, p.project, comment=p.comment)
        else:
            run_timer(conn, work_value, rest_value, comment=p.comment)
        
    # Cleanup
    _db.close_connection(conn)


# Run Timer based on Project, if no Project specified use "General"
def run_timer(connection, work_time, rest_time, project_used="", comment=""):

    if(len(project_used) > 0):
        print(f'Starting Timer for project: {project_used}')

        # Work
        start_time = _utilities.get_current_time()
        entry_id = hashlib.md5(start_time.encode())
        _db.insert_log(connection, project_used, 'work', work_time, \
                rest_time, time_started=start_time, \
                    comments=comment, entry_id=entry_id)
        countdown(m=work_time, msg='Work Session Ended')
        _db.update_log(connection, _utilities.get_current_time())

        # Break
        run_prompt('Time to take a Break, Work')
        start_time = _utilities.get_current_time()
        entry_id = hashlib.md5(start_time.encode())
        _db.insert_log(connection, project_used, 'rest', work_time, \
                rest_time, time_started=start_time, entry_id=entry_id)
        countdown(m=rest_time, msg='Break Session Ended')
        _db.update_log(connection, _utilities.get_current_time())
        run_prompt('Break')
    else:
        print('Starting Timer for General Work')
        _db.insert_log(connection, project_used, 'work', work_time, \
                 rest_time, time_started=str(_utilities.get_current_time()), \
                    comments=comment)
        countdown(m=work_time, msg='Work Session Ended')
        run_prompt('Time to take a Break, Work')
        _db.insert_log(connection, project_used, 'rest', work_time, \
                rest_time, time_stopped=str(_utilities.get_current_time()))
        countdown(m=rest_time, msg='Break Session Ended')
        run_prompt('Break')


# Run proper script based on OS
def run_prompt(notification):
    if platform == "linux" or platform == "linux2":
        subprocess.call([sys.executable, "./Tools/linux_prompt.py", "-m", \
                notification])
    elif platform == "darwin":
        # OS X
        print('This program is not currently compatible with Macs')
    elif platform == "win32":
        # Windows...
        subprocess.call([sys.executable, "./Tools/win_prompt.py", "-m", \
                notification])


# Countdown Timer
def countdown(m, h=0, s=0, msg=""):

    # Calculate the total number of seconds
    total_seconds = h * 3600 + m * 60 + s

    # While loop that checks if total_seconds reaches zero
    # If not zero, decrement total time by one second
    while total_seconds > 0:

        # Timer represents time left on countdown
        timer = timedelta(seconds = total_seconds)
       
        # Prints the time left on the timer
        print(timer, end="\r")

        # Delays the program one second
        time.sleep(1)

        # Reduces total time by one second
        total_seconds -= 1
    print(msg)


main()
