# About
This is a docker-compose single node implementation.  It is not distributed in nature and is not meant as a scalable solution.  It is meant to get the stack up and running for demo or small scale deployments.


## Dependencies
Make sure you have the following installed:
- `docker` (Make sure the engine is running after the install)
- `docker-compose`


## Configuration File
| Key                               | Required | Description                                                                                                           | Default message                                                                                      |
| --------------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| HOST_ADDRESS                      | ✔     | GovReady-Q's public address as would be entered in a web browser. |
| ALLOWED_HOSTS                     | ❌    | GovReady-Q's approved list of host names provided as an array. If not provided, will default to HOST_ADDRESS. |
| HOST_PORT_HTTPS                   | ✔     | GovReady-Q's public address HTTPS port; defaults to 443 |
| HOST_PORT_HTTP                    | ❌    | GovReady-Q's public address HTTP port; defaults to 80 |
| ADMINS                            | ✔    | Administrator accounts. Ex: `[{"username": "username", "email":"first.last@example.com", "password": "REPLACEME"}]`     | Will auto-create an admin, you need to find it in the logs docker-compose logs                       |
| BRANDING                          | ❌    | Full file path to GovReady-Q branding directory                                                                       | GovReady default branding will be used.                                                              |
| DATABASE_CONNECTION_STRING        | ❌    | Database connection string: `<db_connector>://<name>:<password>@<host>:<port>/<db_name>`                                | Will create a Postgres server in the docker-compose deployment for you.  It will not have snapshots. |
| MOUNT_FOLDER                      | ❌    | Mount folder to put artifacts, logs, etc.                                                                             | Current directory                                                                                    |
| GIT_URL                           | ❌    | GovReady-Q Github Repo                                                                                                | Defaults to https://github.com/GovReady/govready-q.git                                               |
| MAILGUN_API_KEY                   | ❌    | Mailgun is used to submit an incoming email from notifications.                                                       | No default provided.                                                                                 |
| NGINX_CERT                        | ❌    | Full file path to Nginx cert.pem                                                                                      | Defaults to self signed                                                                              |
| NGINX_KEY                         | ❌    | Full file path to Nginx key.pem                                                                                       | Defaults to self signed                                                                              |
| EMAIL_DOMAIN                      | ❌    | Domain of the Email Server.                                                                                           | No default provided.                                                                                 |
| EMAIL_HOST                        | ❌    | Host of Email Server.                                                                                                 | No default provided.                                                                                 |
| EMAIL_PORT                        | ❌    | Port of Email Server.                                                                                                 | No default provided.                                                                                 |
| EMAIL_PW                          | ❌    | Password for the User for of Email Server.                                                                            | No default provided.                                                                                 |
| EMAIL_USER                        | ❌    | User for the Email Server.                                                                                            | No default provided.                                                                                 |
| GR_PDF_GENERATOR                  | ❌    | PDF generator binary name.                                                                                            | Default is to disable this feature                                                                          |
| GR_IMG_GENERATOR                  | ❌    | IMG generator binary name.                                                                                            | Default is to disable this feature                                                                         |
| PERSIST_STACK                     | ❌    | Persist stack between runs.                                                                                           | Default is False |
| PROXY_AUTHENTICATION_USER_HEADER  | ❌    | Proxy Authentication User header.                                                                                     | No default provided.                                                                                 |
| PROXY_AUTHENTICATION_EMAIL_HEADER | ❌    | Proxy Authentication Email header.                                                                                    | No default provided.                                                                                 |
| SECRET_KEY                        | ✔     | Django Secret                                                                                                         |                                                                                   |
| VERSION                           | ❌    | GovReady-Q version/tag                                                                                                | Defaulting to latest release                                                                         |

To build an empty configuration file use `python run.py init` at the root of the project.

## Local Docker Database

A local Docker container running PostgreSQL will automatically be added when the `configuration.json` file's `DATABASE_CONNECTION_STRING` is set to `""`.

The local database running in Docker container is persisted between deploys in a Docker Volume called `govready-q_postgres-data` to preserve data.

The Docker container running the default PostgreSQL is Alpine Linux. The PostgreSQL configuration files located in the `/postgres-data` directory (e.g., `/postgres-data/postgresql.conf`).

#### Wipe Local Docker Database Volume
- Remove existing docker build - then:
- `docker volume rm govready-q_postgres-data`

## Local Host Database

It is also possible to connect Docker-ized GovReady-Q instance to a PostgreSQL database instance running on HOST machine (i.e., not in Docker) following the below instructions.

This configuration provides a persistent Postgres database on the Host machine that is used by a GovReady deployment running withing docker containers on the host machine.

(Instructions for Ubuntu 18.04. Adjust appropriately for your OS.)

For additional information see https://www.postgresql.org/docs/current/static/auth-pg-hba-conf.html.

### Step 1 - Configure postgresql.conf

Modify the Host's Postgres configuration file `/etc/postgresql/10/main/postgresql.conf` to instruct Postgres to listen on the Host machine's IP address, Host name, etc.:

```
listen_addresses = 'localhost, ip_address, domain_name'
```

Example:

```
listen_addresses = 'localhost, 10.1.0.10'
```

### Step 2 - Configure pg_hba.conf

Modify Host's Postgres configuration file `/etc/postgres/10/main/pg_hba.conf` to permit connection from the GovReady-Q instance running in the docker container by allowing a connection from the IP address the Host perceives for the docker container.

GovReady-Q's docker compose network is configured with the IP address `172.32.0.0/24`. (If you deployed GovReady using Docker-Compose, the IP address will be that of the Docker-Compose network bridge. If you deployed GovReady using a single container, the IP address will be that of the container's IP address.)

Configure `pg_hba.conf` to permit connections from the perceived IP address of docker network (or container):

```
host all all 172.32.0.0/24 password
local all postgres peer
...
```

### Step 3 - Restart Postgres

Restart Postgres:

```
sudo service postgresql stop
sudo service postgresql start
```

### Step 4 - Configure GovReady Deployment configuration.json

Modify GovReady's docker deployment configuration file `configuration_mantech.json` to have Postgres database connection string that includes the Host IP address running the Postgres instance.

`"DATABASE_CONNECTION_STRING": "postgres://username:password@host/dbname",`

Example:

`"DATABASE_CONNECTION_STRING": "postgres://govready-q:s&kerjkDKW231@10.1.0.10/govreadydb",`

### Step 5 - Restart GovReady container stack

Restart GovReady stack appropriately.


# BACKUP POSTGRES DATABASE

1. Look up password in file `/home/govready-q/local/environment.json`.
1. Run: `pg_dump postres -U example_user -h localhost > <file_path>/pg_dump_<date>.sql`

## Remote Database

It is also possible to connect Docker-ized GovReady-Q instance to a PostgreSQL database instance running on a different machine (i.e., remote database) following the below instructions.

This configuration provides a persistent Postgres database on the Host machine that is used by a GovReady deployment running withing docker containers on the host machine.

## Viewing Logs

When a `Server Error (500)` appears the will almost always be written to the log file in the `govready-q_app_1` container and can be accessed from the following `tail` command on the HOST machine:

```
tail <path_to>/govready-deployments/volumes/govready-q/logs/gunicorn.error.log
```

This file can also be reached from the GovReady-Q container (govready-q_app_1):

```
sudo docker exec -it govready-q_app_1 tail /var/log/gunicorn.error.log
```

The STDOUT of the GovReady-Q as it runs can be viewed by attaching in a terminal to the GovReady-Q container via the command (for example):

```
sudo docker attach govready-q_app_1
```