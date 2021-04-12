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

# Start server
echo "[ + ] Starting server"
python3 manage.py send_notification_emails forever