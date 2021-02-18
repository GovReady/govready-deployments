#!/usr/bin/env python3

import re
import requests
import signal
import subprocess
from subprocess import DEVNULL, PIPE, STDOUT
import sys
import time

################################################################
#
# helpers
#
################################################################

def run_optionally_verbose(args, verbose_flag):
    p = subprocess.run(args, capture_output=True)
    if verbose_flag:
        print("COMMAND:{}\nSTDOUT:\n{}\nSTDERR:\n{}".format(p.args, p.stdout.decode('utf-8'), p.stderr.decode('utf-8')))
    return p

################################################################
#
# main()
#
################################################################

def main():
    # Gracefully exit on control-C
    signal.signal(signal.SIGINT, lambda signal_number, current_stack_frame: sys.exit(0))

    # set up args dict
    args = {}

    # check for verbose argument
    args['verbose'] = False
    if "-v" in sys.argv:
        args['verbose'] = True
    if "--verbose" in sys.argv:
        args['verbose'] = True
    if "verbose" in sys.argv:
        args['verbose'] = True

    # check for help argument
    args['help'] = False
    if "help" in sys.argv:
        args['help'] = True

    # check for demo argument
    args['demo'] = False
    if "demo" in sys.argv:
        args['demo'] = True

    # act on help or NOT demo arguments, or start demo
    if args['help']:
        print(help_message_3())
        sys.exit(0)
    elif not args['demo']:
        print(help_message_1())
        sys.exit(0)
    else:
        # if demo argument, start server; print welcome banner and version
        print(help_message_0(), flush=True)
        with open('VERSION') as f:
            print(f.read(), flush=True)
        if args['verbose']:
            p = run_optionally_verbose(['git', 'rev-parse', 'HEAD'], False)
            print("govready-q commit hash = " + p.stdout.decode('utf-8'), flush=True)

        # run checks
        print("running some checks...", flush=True)
        run_optionally_verbose(['./manage.py', 'check', '--deploy'], args['verbose'])
        print("... done running some checks.\n", flush=True)

        # initialize the database
        print("initializing database...", flush=True)
        run_optionally_verbose(['./manage.py', 'migrate'], args['verbose'])
        run_optionally_verbose(['./manage.py', 'load_modules'], args['verbose'])
        print("... done initializing database.\n", flush=True)

        # create an initial administrative user and organization
        # non-interactively and write the administrator's initial
        # password to standard output.
        print("setting up system and creating demo user...", flush=True)
        p = run_optionally_verbose(['./manage.py', 'first_run', '--non-interactive'], args['verbose'])
        print("... done setting up system and creating demo user.\n", flush=True)

        m = re.search('\n(Created administrator account.+)\n', p.stdout.decode('utf-8'))
        if m:
            print(m.group(1) + "\n", flush=True)

        # start the server
        print("starting GovReady server...", flush=True)
        p = subprocess.Popen(['gunicorn', '--config', '/etc/opt/gunicorn.conf.py', 'siteapp.wsgi'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        if args['verbose']:
            print("Running gunicorn, check logs for output.")
        # "extra-verbose" is not currently implemented, but this code might useful some day
        # note that any timeout here delays the next section, "wait for server to come alive"
        if 'extra-verbose' in args:
            try:
                outs, errs = p.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                outs, errs = None, None
            print("COMMAND:{}\nSTDOUT (first 5 seconds):\n{}\nSTDERR (first 5 seconds):\n{}\n".format(p.args, outs, errs))

        # wait for server to come alive
        while True:
            p = subprocess.run(['curl', 'http://localhost:8000'], capture_output=True)
            if p.returncode == 0:
                if args['verbose']:
                    print("Got curl return code = 0", flush=True)
                break
            if args['verbose']:
                print("Checking for server - curl return code = {}, continuing to poll...".format(p.returncode), flush=True)
            time.sleep(1)

        # let user know they're good to go
        print(help_message_2(), flush=True)

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

### Help Message 0 ###

def help_message_0():
    return """\

<<<<<<<<<<<<<<<< WELCOME TO GOVREADY >>>>>>>>>>>>>>>>

This is GovReady-Q."""
# end of help_message_0()

### Help Message 1 ###

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

### Help Message 2 ###

def help_message_2():
    return """\
GovReady-Q is running.
Visit http://localhost:8000/ with your browser.
Log in with the administrator credentials above.
Hit control-C to exit."""

### Help Message 3 ###

def help_message_3():
    return """\

# WELCOME TO GOVREADY

## Print this help message

```
    docker run --rm govready-demo help
```

## Create Documentation Files

*not yet implemented*
```
    docker run --rm -v `pwd`:/docs govready-demo help docs
```

## Create Helper Scripts

*not yet implemented*
```
    docker run --rm -v `pwd`:/docs govready-demo help helpers
```

## Run Commands

### Print basic help

```
    docker run govready-demo
```

### Run demo, with port forwarding, but without persistence

```
    docker run --rm -p 8000:8000 govready-demo demo
```

### Run demo, with port forwarding, with volume mounts for persistence (UNIX-style `pwd`)
```
    docker run --rm -p8000:8000 \\
    -v `pwd`/log:/var/log \\
    -v `pwd`/config:/etc/opt \\
    -v `pwd`/local:/opt/govready-q/local \\
    govready-demo demo
```

## Build Commands

### Remove and rebuild image

    docker rmi govready-demo ; docker build --tag govready-demo .

### Alternate build for debugging

    docker build --tag govready-demo --progress plain --no-cache .

"""
# end of help_message_3()

################################################################
#
# start execution
#
################################################################

main()
