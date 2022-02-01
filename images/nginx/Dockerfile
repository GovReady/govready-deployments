FROM nginx:alpine

ARG HOST_ADDRESS
ARG APP_DOCKER_PORT

COPY nginx.conf /etc/nginx/nginx.conf
RUN \
   sed -i -e "s|test.example.com|$HOST_ADDRESS|" /etc/nginx/nginx.conf \
   && sed -i -e "s|app:8000|app:$APP_DOCKER_PORT|" /etc/nginx/nginx.conf \
   && mkdir -p /etc/pki/tls/certs /etc/pki/tls/private


ARG NGINX_CERT
ARG NGINX_KEY

COPY ${NGINX_CERT}* /etc/pki/tls/certs/
COPY ${NGINX_KEY}* /etc/pki/tls/private/
COPY docker-entrypoint.sh /etc/opt/docker-entrypoint.sh

RUN if [ "$NGINX_CERT" = "" ]; then \
    apk add --no-cache --update openssl \
    && openssl req -newkey rsa:4096 \
    -x509 \
    -sha256 \
    -days 3650 \
    -nodes \
    -out /etc/pki/tls/certs/cert.pem \
    -keyout /etc/pki/tls/private/key.pem \
    -subj "/C=US/ST=State/L=Locality/O=Organization/OU=Organizational Unit/CN=$HOST"; \
  else \
    mv /etc/pki/tls/certs/"$(basename $NGINX_CERT)" /etc/pki/tls/certs/cert.pem \
    && mv /etc/pki/tls/private/"$(basename $NGINX_KEY)" /etc/pki/tls/private/key.pem; \
  fi
