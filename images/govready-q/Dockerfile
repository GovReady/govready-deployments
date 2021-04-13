# Ubuntu 20.04 focal-20210119
FROM ubuntu:focal-20210119

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
  gunicorn

# Install GovReady application.
WORKDIR /opt

ARG VERSION
ARG GIT_URL
RUN git clone --depth 1 --branch ${VERSION} ${GIT_URL}

WORKDIR /opt/govready-q

# Install Python requirements.
RUN pip3 install --no-cache-dir -r requirements.txt

# Upgrade gevent (regularly check if this is still necessary)
RUN pip3 install gevent==21.1.2

# Fetch vendor resources.
RUN ./fetch-vendor-resources.sh

# Copy config files
COPY config/gunicorn.conf.py /etc/opt/gunicorn.conf.py

# Copy utility scripts
COPY dockerfile_exec.py first_run.sh docker_exec_prod.sh docker_exec_prod_email_notifications.sh docker_exec_write_environment.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker_exec*.sh

# This directory must be present for the AppSource created by our
# first_run script. The directory only has something in it if
# the container is launched with --mount.
# --mount type=bind,source="$(pwd)",dst=/mnt/q-files-host
RUN mkdir -p /mnt/q-files-host
 
# Set the startup script.
CMD [ "dockerfile_exec.py" ]
