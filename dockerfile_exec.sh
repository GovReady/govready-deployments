# This is the main entry point, i.e. process zero, of the
# Docker container.

set -euf -o pipefail # abort script on error

# Show the version immediately, which might help diagnose problems
# from console output.
echo "This is GovReady-Q."
cat VERSION

# Show filesystem information because the root filesystem might be
# read-only and other paths might be mounted with tmpfs and that's
# helpful to know for debugging.
echo
echo Filesystem information:
cat /proc/mounts | egrep -v "^proc|^cgroup| /proc| /dev| /sys"
echo

# Run checks.
./manage.py check --deploy

# Initialize the database.
./manage.py migrate
./manage.py load_modules

# Create an initial administrative user and organization
# non-interactively and write the administrator's initial
# password to standard output.
if [ ! -z "${FIRST_RUN-}" ]; then
	echo "Running FIRST_RUN actions..."
	./manage.py first_run --non-interactive
fi

# Write a file that indicates to the host that Q
# is now fully configured. It will still be a few
# moments before Gunicorn is accepting connections.
echo "done" > /tmp/govready-q-is-ready
echo "GovReady-Q is starting."
echo # gunicorn output follows

# Start the server.
exec supervisord -c /etc/opt/supervisord.ini -n
