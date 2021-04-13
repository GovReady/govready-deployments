# About
This is a docker-compose implementation.  It is not distributed in nature is not meant as a scalable/reliable solution.


## Local Database
The local database is persisted in a Docker Volume called `onprem_simple_pg-data`


#### Wipe
- Remove existing docker build - then:
- `docker volume rm onprem_simple_pg-data`