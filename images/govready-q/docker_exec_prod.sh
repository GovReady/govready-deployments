#!/usr/bin/env bash
mkdir -p local
cat << EOF > local/environment.json
{
	"debug": ${DEBUG-false},
	"host": $(echo ${ADDRESS} | jq -R .),
	"https": ${HTTPS-false},
	"secret-key": $(echo ${SECRET_KEY-} | jq -R .),
	"syslog": $(echo ${SYSLOG-} | jq -R .),
	"govready_admins": ${ADMINS-[]},
	"static": "static_root",
	"db": $(echo ${DATABASE_CONNECTION_STRING-} | jq -R .)
}
EOF

#python3 install.py --non-interactive --docker
echo "[ + ] Running checks"
python3 manage.py check --deploy

echo "[ + ] Generating Static Files"
python3 manage.py collectstatic --noinput

echo "[ + ] Migrating Database"
python3 manage.py migrate
python3 manage.py load_modules
python3 manage.py first_run --non-interactive

# Start server
echo "[ + ] Starting server"
gunicorn --config /etc/opt/gunicorn.conf.py siteapp.wsgi