# About
This is a docker-compose implementation.  It is not distributed in nature and is not meant as a scalable/reliable solution.  It is meant to get the stack up and running for demo or small scale deployments.


## Dependencies
Make sure you have the following installed:
- `docker` (Make sure the engine is running after the install)
- `docker-compose`


## Configuration File
| Key                               | Required | Description                                                                                                           | Default message                                                                                      |
| --------------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| ADDRESS                           | ✔       | GovReady-Q's public address as would be entered in a web browser. Set with --address HOST:PORT (PORT optional if 443) | 
| ADMINS                            | ❌    | Administrator accounts. Ex: `[{"username": "username", "email":"first.last@example.com", "password": "REPLACEME"}]`     | Will auto-create an admin, you need to find it in the logs docker-compose logs                       |
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
| GR_PDF_GENERATOR                  | ❌    | PDF generator binary name.                                                                                            | Default is to disabled this feature                                                                          |
| GR_IMG_GENERATOR                  | ❌    | IMG generator binary name.                                                                                            | Default is to disabled this feature                                                                         |
| PROXY_AUTHENTICATION_USER_HEADER  | ❌    | Proxy Authentication User header.                                                                                     | No default provided.                                                                                 |
| PROXY_AUTHENTICATION_EMAIL_HEADER | ❌    | Proxy Authentication Email header.                                                                                    | No default provided.                                                                                 |
| SECRET_KEY                        | ✔       | Django Secret                                                                                                         |                                                                                   |
| VERSION                           | ❌    | GovReady-Q version/tag                                                                                                | Defaulting to latest release                                                                         |

To build an empty configuration file use `python run.py init` at the root of the project.

## Local Database
The local database is persisted in a Docker Volume called `onprem_pg-data`

#### Wipe
- Remove existing docker build - then:
- `docker volume rm onprem_pg-data`