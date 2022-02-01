# Ubuntu 20.04 focal-20210119
FROM ubuntu:focal-20210119

# Expose the port that `manage.py runserver` uses by default.
EXPOSE 8000

# Update package list.
RUN apt-get update
ENV DEBIAN_FRONTEND=noninteractive

# Add dos2unix for Windows support of deployments for the CRLF issues
RUN apt-get update && apt-get install -y dos2unix netcat

# Set up the locale.
RUN apt-get update && apt-get install -y locales && \
  echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && \
  dpkg-reconfigure locales && \
  update-locale LANG=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV LANGUAGE=en_US:en

# Set up the timezone.
RUN apt-get update && apt-get install -y --no-install-recommends tzdata && \
  ln -fs /usr/share/zoneinfo/UTC /etc/localtime && \
  dpkg-reconfigure tzdata

# Install GovReady-Q prerequisites.
RUN apt-get update && apt-get -y install \
  unzip git curl jq \
  python3 python3-pip \
  python3-yaml \
  graphviz pandoc \
  gunicorn

# Install GovReady application.
WORKDIR /opt

ARG VERSION
ARG GIT_URL
# Defaults to latest Release if Tag/Branch not provided
RUN if [ "$VERSION" = "" ]; then \
        git -c versionsort.suffix=- ls-remote --tags --sort=v:refname $GIT_URL | tail --lines=1 | cut --delimiter='/' \
         --fields=3 | egrep -o '[v0-9\.]+' > /tmp/version.txt; \
    else \
        echo $VERSION > /tmp/version.txt; \
  fi
RUN git clone --depth 1 --branch $(cat /tmp/version.txt) ${GIT_URL} govready-q
RUN find . -type f -print0 | xargs -0 dos2unix

WORKDIR /opt/govready-q


# Install Python requirements.
RUN pip3 install --no-cache-dir -r requirements.txt
ARG DB_ENGINE
RUN if [ "$DB_ENGINE" = "mysql" ]; then \
        apt-get update && apt-get install -y libmysqlclient-dev \
        && pip3 install --no-cache-dir -r requirements_mysql.txt; \
  fi

ARG GR_PDF_GENERATOR
ARG GR_IMG_GENERATOR
RUN if [ "$GR_PDF_GENERATOR" = "wkhtmltopdf" ] || [ "$GR_IMG_GENERATOR" = "wkhtmltopdf" ]; then \
        apt-get update &&  apt-get -y install wget \
        && wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb \
        && apt install -y ./wkhtmltox_0.12.6-1.focal_amd64.deb; \
  fi

# Upgrade gevent (regularly check if this is still necessary)
RUN pip3 install gevent==21.1.2

# Install NLP tools
RUN pip3 install -U spacy
RUN python3 -m spacy download en_core_web_sm
# Optionally install larger spaCY english model
# RUN python3 -m spacy download en_core_web_lg
# Optionally install largest spaCY english vector model
# RUN python3 -m spacy download en_vectors_web_lg


# Template files
ARG BUILD_FILE_BRANDING
COPY *${BUILD_FILE_BRANDING} /tmp/

# Copy config files
COPY config/gunicorn.conf.py /etc/opt/gunicorn.conf.py
COPY wait-for-database.py /etc/opt/wait-for-database.py

# Copy utility scripts
RUN mkdir /tmp/scripts/
COPY first_run.sh docker_exec_prod.sh docker_exec_prod_email_notifications.sh docker_exec_write_environment.sh /tmp/scripts/
RUN find /tmp/scripts -type f -print0 | xargs -0 dos2unix
RUN cp /tmp/scripts/* /usr/local/bin/ && rm -rf /tmp/scripts/

RUN chmod +x /usr/local/bin/docker_exec*.sh

# This directory must be present for the AppSource created by our
# first_run script. The directory only has something in it if
# the container is launched with --mount.
# --mount type=bind,source="$(pwd)",dst=/mnt/q-files-host

#RUN if [ -d "/opt/govready-q/frontend" ]; then \
#    apt-get install -y nodejs npm && \
#    npm install yarn --global && \
#    cd /opt/govready-q/frontend && \
#    yarn && \
#    npm run-script build && \
#    cd -; \
#fi

RUN if [ -d "/opt/govready-q/frontend" ]; then \
    curl -sL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get update && \
    apt-get install nodejs && \
    npm install yarn --global && \
    cd /opt/govready-q/frontend && \
    yarn && \
    npm run-script build && \
    cd -; \
fi
