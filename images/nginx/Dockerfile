FROM nginx:alpine

ARG HOST

COPY nginx.conf /etc/nginx/nginx.conf
RUN \
   sed -i -e "s|test.example.com|$HOST|" /etc/nginx/nginx.conf \
&& mkdir -p /etc/pki/tls/certs /etc/pki/tls/private

ARG NGINX_CERT
ARG NGINX_KEY

COPY *${NGINX_CERT} /etc/pki/tls/certs/cert.pem
COPY *${NGINX_KEY} /etc/pki/tls/private/key.pem

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
  fi

