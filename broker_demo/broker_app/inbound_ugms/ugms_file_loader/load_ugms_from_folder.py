# scan a folder. When new files are found in the folder, load them to the touchdown data store

import os
import sys
import time
import gzip
import uuid
import re
# from watchdog.events import RegexMatchingEventHandler
# from watchdog.observers import Observer
import psycopg2
import argparse



'''
load_ugms_from_folder.py

Scan a specified folder, looking for files of a specified pattern

For each one, call a specified function and check for success

If successful, carry out the specified archive instruction

parameters:
    scan_folder     default  .
    archive_flag    default - do nothing

'''

REGEXES = ['.+\.csv\Z', '.+\.csv\.gz\Z']
SLEEP_SECONDS = 1

previous_files_set = set([])

#DB

def connect_to_db(connect_string):
    print('db connect: ', connect_string, flush=True)

    # wait for detabase to be ready, then connect
    while True:
        try:
            conn = psycopg2.connect(connect_string)
            break
        except psycopg2.OperationalError as oe:
            print("waiting for db...", flush=True)
            time.sleep(1)

    print('db status: ', conn.status, flush=True)
    return conn


def wait_till_all_there(filename):

    # wait for newly-created file to be completely copied
    oldsize = -1
    while oldsize != os.path.getsize(filename):
        oldsize = os.path.getsize(filename)
        time.sleep(2)
        # try to open the file - will generate permission error. Reset the size so it keeps going
        try:
            f = open(filename, mode='r')
            f.close()
        except PermissionError:
            print('+', end='', flush=True)
            oldsize = -1
        print('.', end='', flush=True)
    
    time.sleep(10)
    print('*', flush=True)


def is_loaded(data_file_name):

    # check if the filename has been loaded
    print('checking...', flush=True)
    cur = conn.cursor()
    cur.execute("SELECT file_name FROM files_loaded WHERE file_name = '{}'".format(data_file_name))
    is_loaded = cur.fetchone()
    cur.close()
    print('loaded' if is_loaded else 'new', flush=True)

    return is_loaded


def load_the_file(file_to_load, data_file_name, file_uuid):
    print('loading...', flush=True)
    cur = conn.cursor()
    cur.copy_expert("COPY ugms_touchdown FROM STDIN WITH (FORMAT CSV, HEADER TRUE)", file_to_load)
    print('rows: ', cur.rowcount, flush=True)
    cur.close()

    print('recording...')
    cur = conn.cursor()
    cur.execute("INSERT INTO files_loaded (file_name, loaded_timestamp, file_uuid) VALUES ('{}', current_timestamp, '{}')".format(data_file_name, file_uuid))
    cur.close()
    conn.commit()
    

def load_to_db(filename):
    print(os.path.basename(filename), flush=True)
    wait_till_all_there(filename)

    # open the file, unzipping if necessary
    if os.path.splitext(filename)[1]=='.gz':
        print('unzipping...', flush=True)
        the_file = gzip.open(filename, mode='rb')
        the_file_name = os.path.splitext(os.path.basename(filename))[0]
    else:
        the_file = open(filename, mode='r')
        the_file_name = os.path.basename(filename)

    # unpick the incoming filename to recover uuid and original filename
    # filename is uuid_original-file-name
    filename_elements = the_file_name.split('_')
    file_uuid = filename_elements[0]
    data_file_name = '_'.join(filename_elements[1:])

    # check if file already loaded
    if not is_loaded(data_file_name):
        load_the_file(the_file, data_file_name, file_uuid)

    print('archiving...', end='', flush=True)
    the_file.close()
    # time.sleep(7)

    # move the file to archive folder
    # (actually, just delete it for now)
    # (need to wait till file is available - Docker has a lag)
    while True:
        try:
            os.remove(filename)
            break
        except OSError as oe:
            print('.', end='',  flush=True)
            time.sleep(1)
    print()
    print('done', flush=True)


def  scan_for_new_files(data_path):

    # iterate through files in folder and process them
    global previous_files_set
    current_files_set = set([])
    for file_regex in REGEXES:
        current_files_set = current_files_set.union(set([ff for ff in os.listdir(data_path) if re.match(file_regex, ff)]))
    new_files_set = current_files_set.difference(previous_files_set)

    for f in new_files_set:
        load_to_db(os.path.join(data_path, f))

    previous_files_set = current_files_set.copy()



# class UGMSFileHandler(RegexMatchingEventHandler):
 
#     def process(self, event):
#         # print(event.src_path, event.event_type)
#         load_to_db(os.path.abspath(event.src_path))

#     def on_created(self, event):
#         self.process(event)

#     def on_modified(self, event):
#         self.process(event)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='UGMS data loader')
    parser.add_argument('data_path', type=str, default='.' )
    parser.add_argument('connection', type=str)
    the_args = parser.parse_args()
    data_path = the_args.data_path
    print('data path: {}'.format(data_path))
    connect_string = the_args.connection

    conn = connect_to_db(connect_string)
    print('ugms data loader: listening for incoming ugms data files', flush=True)

    # note: watchdog doesn't work very well with docker containers in Windows so replaced with dumb code for now
    # observer = Observer()
    # observer.schedule(UGMSFileHandler(regexes=REGEXES), path=data_path)
    # observer.start()
    try:
        while True:
            scan_for_new_files(data_path)
            time.sleep(SLEEP_SECONDS)
    except KeyboardInterrupt:
        sys.exit
        # observer.stop()

    # observer.join()