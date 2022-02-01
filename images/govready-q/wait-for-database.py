import os
import re
import socket
import time

host, port = os.environ['DATABASE_CONNECTION_STRING'].split('@')[-1].split('/')[0].split(':')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect((host, int(port)))
        s.close()
        print("Database is available.  Proceeding to next step")
        break
    except socket.error:
        print('Waiting for Database to come up')
        time.sleep(0.1)
