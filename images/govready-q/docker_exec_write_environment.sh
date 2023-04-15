#!/usr/bin/env bash

echo "[ + ] Setting up environment"
mkdir -p local
cat << EOF > local/environment.json
{
	"debug": ${DEBUG-false},
	"host": "$(echo "${HOST_ADDRESS}:${HOST_PORT_HTTPS}" )",
	"host_http": "$(echo "${HOST_ADDRESS}:${HOST_PORT_HTTP}" )",
	"secret-key": $(echo ${SECRET_KEY-} | jq -R .),
	"syslog": $(echo ${SYSLOG-} | jq -R .),
	"govready_admins": ${ADMINS-[]},
	"govready_users": ${GOVREADY_USERS-[]},
	"static": "static_root",
	"db": $(echo ${DATABASE_CONNECTION_STRING-} | jq -R .),
	"allowed_hosts": ${ALLOWED_HOSTS-[]},
	"govready-url": "$(echo "https://${HOST_ADDRESS}:${HOST_PORT_HTTPS}" )",
	"oidc": ${OIDC-\{\}},
	"okta": ${OKTA-\{\}}
}
EOF

function set_env_setting {
	# set_env_setting keypath value
	cat local/environment.json \
	| jq ".$1 = $(echo $2 | jq -R .)" \
	> /tmp/new-environment.json
	cat /tmp/new-environment.json > local/environment.json
	rm -f /tmp/new-environment.json
}

# Add email parameters.
if [[ ! -z "${EMAIL_HOST-}" ]]; then
	set_env_setting email.host "$EMAIL_HOST"
	set_env_setting email.port "$EMAIL_PORT"
	set_env_setting email.user "$EMAIL_USER"
	set_env_setting email.pw "$EMAIL_PW"
	set_env_setting email.domain "$EMAIL_DOMAIN"
fi
if [[ ! -z "${MAILGUN_API_KEY-}" ]]; then
	set_env_setting mailgun_api_key "$MAILGUN_API_KEY"
fi

# Overridden branding.
if [[ ! -z "${BRANDING-}" ]]; then
    ls /tmp
    name=$(basename "$BRANDING" | cut -d. -f1)
    unzip "/tmp/$name" -d "/opt/govready-q/$name"
	set_env_setting branding "$name"
fi

# Enterprise login settings.
if [[ ! -z "${PROXY_AUTHENTICATION_USER_HEADER-}" ]]; then
	set_env_setting '["trust-user-authentication-headers"].username' "$PROXY_AUTHENTICATION_USER_HEADER"
	set_env_setting '["trust-user-authentication-headers"].email' "$PROXY_AUTHENTICATION_EMAIL_HEADER"
fi

# PDF Generator settings.
if [[ ! -z "${GR_PDF_GENERATOR-}" ]]; then
	set_env_setting '["gr-pdf-generator"]' "$GR_PDF_GENERATOR"
fi

# Image Generator settings.
if [[ ! -z "${GR_IMG_GENERATOR-}" ]]; then
	set_env_setting '["gr-img-generator"]' "$GR_IMG_GENERATOR"
fi