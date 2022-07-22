"""
---------- Enigma Project - Version 0.0.1 ----------

Responsabilities:

manage machine resources
talk with the operational system
get user input
generate log
connect functions

-----------------------------------------------------
"""

import os
import time
import datetime
from threading import Thread
from decouple import config
# import psutil
from common.graphical_interface.vpgi import *


# Measure cpu times

# Measure cpu util

# Count working CPU cores

# Measure CPU frequencies

# Monitor RAM usage

# Monitor disk partitions

# Monitor disk usage

# Monitor network requests

# Monitor battery usage

# Run all checks

# current_time = datetime.datetime.now()
# current_time.strftime('%Y-%m-%d %H:%M:%S')


def threadGenerator(target_function, description, terminator_code=False):
    thread_start = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    thread_code = f"{description}{CURRENT_MACHINE}{thread_start}"
    thread_path = f"{MACHINE_TEMP_FOLDER}\\{thread_code}.txt"
    if terminator_code:
        with open(thread_path, 'w') as file:
            file.write('0')
        process_kwargs = {'is_alive_temp': thread_path}
    else:
        process_kwargs = {}
    running_processes[thread_code] = Thread(target=target_function, daemon=True, kwargs=process_kwargs)
    return thread_code


def threadStarter(target_thread, terminator_code=False):
    if terminator_code:
        thread_path = f"{MACHINE_TEMP_FOLDER}\\{target_thread}.txt"
        with open(thread_path, 'w') as file:
            file.write('1')
    running_processes[target_thread].start()


def threadKiller(target_thread):
    thread_path = f"{MACHINE_TEMP_FOLDER}\\{target_thread}.txt"
    with open(thread_path, 'w') as file:
        file.write('0')
    time.sleep(3)
    os.remove(thread_path)


def verifyRunningProcesses():
    for process in list(running_processes.keys()):
        if not running_processes[process].is_alive():
            threadKiller(process)
            print(f"Process terminated! Killing thread for: {process}")
            running_processes.pop(process, None)
        else:
            print(f"Process alive: {process}")


def main():

    get_user_input = threadGenerator(Interface, 'getuserinput', terminator_code=True)
    threadStarter(get_user_input, terminator_code=True)

    while True:
        try:
            verifyRunningProcesses()
            time.sleep(1)
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    running_processes = {}
    CURRENT_MACHINE = config('CURRENT_MACHINE')
    MACHINE_TEMP_FOLDER = config('MACHINE_TEMP_FOLDER')
    main()