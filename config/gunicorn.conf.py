import multiprocessing
bind = '0.0.0.0:8000'
# workers = multiprocessing.cpu_count() * 2 + 1 # recommended for high-traffic sites
# set workers to 1 for now, because the secret key won't be shared if it was auto-generated,
# which causes the login session for users to drop as soon as they hit a different worker
workers = 1
worker_class = 'gevent'
keepalive = 10
