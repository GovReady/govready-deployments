# Ubuntu 20.04 focal-20201106
FROM ubuntu:focal-20201106

# Expose the port that `manage.py runserver` uses by default.
EXPOSE 8000

# Update package list.
RUN apt-get update
ENV DEBIAN_FRONTEND=noninteractive

# Set up the locale.
RUN apt-get install -y locales && \
  echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && \
  dpkg-reconfigure locales && \
  update-locale LANG=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV LANGUAGE=en_US:en

# Set up the timezone.
RUN apt-get install -y --no-install-recommends tzdata && \
  ln -fs /usr/share/zoneinfo/UTC /etc/localtime && \
  dpkg-reconfigure tzdata

# Install GovReady-Q prerequisites.
RUN apt-get -y install \
  unzip git curl jq \
  python3 python3-pip \
  python3-yaml \
  graphviz pandoc \
  gunicorn \
  supervisor

# Install GovReady application.
WORKDIR /opt
RUN git clone https://github.com/GovReady/govready-q.git
WORKDIR /opt/govready-q

## # Copy utility scripts
## COPY dockerfile_exec.sh first_run.sh .

# Install Python requirements.
RUN pip3 install --no-cache-dir -r requirements.txt

# Upgrade gevent
RUN pip3 install gevent==21.1.2

# Fetch vendor resources.
RUN ./fetch-vendor-resources.sh

# Copy config files
COPY config/gunicorn.conf.py /etc/opt/gunicorn.conf.py

# Copy utility scripts
COPY dockerfile_exec.py first_run.sh /usr/local/bin/

# This directory must be present for the AppSource created by our
# first_run script. The directory only has something in it if
# the container is launched with --mount.
# --mount type=bind,source="$(pwd)",dst=/mnt/q-files-host
RUN mkdir -p /mnt/q-files-host
 
# Set the startup script.
ENTRYPOINT [ "dockerfile_exec.py" ]
