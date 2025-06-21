# How to run PostgreSQL in as a container on Docker or Podman on your machine

## Download container image

Docker
```sh
docker pull docker.io/library/postgres:17.5-alpine
```
Podman
```sh
podman pull docker.io/library/postgres:17.5-alpine
```

## Create postgresql instant based on the downloaded image

Docker
```sh
docker run -d --name peer2peerpayment -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:17.5-alpine
```

Podman
```sh
podman run -d --name peer2peerpayment -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:17.5-alpine
```

## Stop the container

Docker
```sh
docker container stop peer2peerpayment
```

Podman
```sh
podman container stop peer2peerpayment
```
## Start after first initilizations
Docker
```sh
docker container start peer2peerpayment
```
Podman
```sh
podman container start peer2peerpayment
```
## Check for running containers
Docker
```sh
docker ps
```
Podman
```sh
podman ps
```
## How to access psql inside the postgresql container

Docker
```sh
docker exec -it peer2peerpayment psql -h localhost -U postgres
```
Podman
```sh
podman exec -it peer2peerpayment psql -h localhost -U postgres
```

### Create Database inside psql
```sh
CREATE DATABASE PEER2PEERPAY;
```