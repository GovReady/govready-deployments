import multiprocessing
bind = '0.0.0.0:8000'
# workers = multiprocessing.cpu_count() * 2 + 1 # recommended for high-traffic sites
# set workers to 1 for now, because the secret key won't be shared if it was auto-generated,
# which causes the login session for users to drop as soon as they hit a different worker
workers = 1
worker_class = 'gevent'
keepalive = 10

# Access log - records incoming HTTP requests
accesslog = "/var/log/gunicorn.access.log"
# Error log - records Gunicorn server goings-on
errorlog = "/var/log/gunicorn.error.log"
# Whether to send Django output to the error log
capture_output = True
# How verbose the Gunicorn error logs should be
loglevel = "info"