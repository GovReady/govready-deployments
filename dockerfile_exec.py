#!/usr/bin/env python3

import re
import signal
import subprocess
from subprocess import DEVNULL, PIPE, STDOUT
import sys
import time

################################################################
#
# main()
#
################################################################

def main():
    # Gracefully exit on control-C
    signal.signal(signal.SIGINT, lambda signal_number, current_stack_frame: sys.exit(0))

    # check for demo argument
    if len(sys.argv)<2 or sys.argv[1] != "demo":
        # if no demo argument, print help and exit
        print(help_message_1())
        sys.exit(0)
    else:
        # if demo argument, start server; print welcome banner and version
        print(help_message_0(), flush=True)
        with open('VERSION') as f:
            print(f.read(), flush=True)

        # run checks
        print("running some checks...", flush=True)
        subprocess.run(['./manage.py', 'check', '--deploy'], capture_output=True)
        print("... done running some checks.\n", flush=True)

        # initialize the database
        print("initializing database...", flush=True)
        subprocess.run(['./manage.py', 'migrate'], capture_output=True)
        subprocess.run(['./manage.py', 'load_modules'], capture_output=True)
        print("... done initializing database.\n", flush=True)

        # create an initial administrative user and organization
        # non-interactively and write the administrator's initial
        # password to standard output.
        print("setting up system and creating demo user...", flush = True)
        p = subprocess.run(['./manage.py', 'first_run', '--non-interactive'], capture_output=True)
        print("... done setting up system and creating demo user.\n", flush = True)

        m = re.search('\n(Created administrator account.+)\n', p.stdout.decode('utf-8'))
        if m:
            print(m.group(1) + "\n", flush = True)


        # start the server
        print("starting GovReady server...", flush = True)
        p = subprocess.Popen(['gunicorn', '--config', '/etc/opt/gunicorn.conf.py', 'siteapp.wsgi'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        print("GovReady-Q is running.\nVisit http://localhost:8000/ with your browser.\nLog in with the administrator credentials above.\nHit control-C to exit.", flush=True)

        # sleep while GovReady runs
        while True:
            time.sleep(1)

        # won't reach here
        sys.exit(0)

################################################################
#
# help messages
#
################################################################

def help_message_0():
    return """\

<<<<<<<<<<<<<<<< WELCOME TO GOVREADY >>>>>>>>>>>>>>>>

This is GovReady-Q."""
# end of help_message_0()

def help_message_1():
    return """\

<<<<<<<<<<<<<<<< WELCOME TO GOVREADY >>>>>>>>>>>>>>>>

Thank you for trying out GovReady-Q on Docker.

In order to run in demonstration mode, GovReady-Q needs you to start the container with port forwarding enabled.

Use this command to start GovReady-Q in detached mode, with port forwarding enabled:

  docker run --rm -p 8000:8000 govready-demo demo

Some startup messages will be printed, and then you'll be prompted to visit http://localhost:8000/ in your browser.

To see options for a richer demo experience, including sample data, persistent data, and production-oriented demos, visit:

https://github.com/GovReady/govready-docker

For more information about GovReady and its products and services, visit:

https://govready.com/
"""
# end of help_message_1()

################################################################
#
# start execution
#
################################################################

main()
