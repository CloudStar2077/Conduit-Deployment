# Conduit-Container

This guide explains how to set up and run a legacy full-stack application consisting of a database, a Django backend, and an Angular frontend.

# Table of Contents

1. [Prerequisites](#Prerequisites) 
2. [Quickstart](#Quickstart) 
3. [Usage](#Usage)

## PREREQUISITES

- Docker (version 20.10 or higher) installed
- Git installed
- Python (version 3.6 or higher) installed

## Quickstart


- Clone Repository 
```bash
git clone git@github.com:CloudStar2077/Conduit-Container.git &&
cd Conduit-Container

 ```
Before building the docker image make changes to the following files.
```bash
mv example.env .env  # rename the example.env to .env
cd frontend/src/app/core/interceptors
mv example.api.config.ts api.config.ts # rename the example.api.config.ts to api.config.ts
```
In the `.env` you need to adjust some data, set the django_secret_key and Postgress_Password then add your Host IP to the Allowed_Hosts and to the API_BASE_URL. To generate a secret_key use 
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
 ``` 

- Build docker image
```bash
cd Conduit-Container/
docker compose build
```  
- Run the Container in Background
```bash
docker compose up -d
```
- Visit the Website and Login

Open a Webbroser and enter the destination
```bash
<HostIp>:8282
 ```

## Usage

In this Setup multi-stage-builds are used for the Dockerfiles, this ensures that the build environment is not included in the container, this keeps the storage space smaller and makes the deployments faster. There is a `Dockerfile` for the frontend and one for the backend. To prevent the backend from being directly accessible from the internet, which would pose a security risk, an Nginx reverse proxy is used. This acts as an intermediary, receiving incoming requests and forwarding them to the backend service. The settings for this are configured in the `nginx.conf`. For the Database there is a pre-built Docker image from the Docker Hub defined in the `docker-compose.yml`. The volume is persistent to prevent data loss. To enable the containers to communicate with each other, a network was also set up. The `entrypoint.sh` script automatically performs the Django database migrations when the container starts and then starts the server as the main process of the container. All backend package dependencies are defined in the `requirements.txt`. Since the Django development server is intended for development only and not suitable for production, Gunicorn is used as a WSGI server to efficiently handle multiple concurrent requests. The envoirement variables are stored in the `example.env`. To ignore all files that don’t belong in the container or repository, a `.dockerignore` and a `.gitignore` file are used.

- Clone the repository 
```bash
git clone git@github.com:CloudStar2077/Conduit-Container.git
cd Conduit-Container
  ```
Copy both, the `example.env` and `example.api.config.ts` then edit them with your data
```bash
cp example.env .env  # copy the example.env to .env
cd frontend/src/app/core/interceptors
cp example.api.config.ts api.config.ts conduit-container # copy the example.api.config.ts to api.config.ts
 ```
For Example ... 

| Variable               | Example Value                              | Description |
|------------------------|--------------------------------------------|------------|
| DJANGO_SECRET_KEY      | `g9!Qv4\$KL2@x8#pR7mZ!sw6^tF3&nH1cV5jY0uD8EA` | Secret key used by Django for cryptographic signing |
| POSTGRES_PASSWORD      | `Your_Secure_Password456!?`                     | Password for the PostgreSQL database |
| DJANGO_ALLOWED_HOSTS   | `localhost,127.0.0.1,backend,YOUR_IP`     | List of allowed hosts for Django |
| PORT                   | `8282`                                     | Public port exposed by the Docker container for the Angular frontend (accessible from the internet) |
| API_BASE_URL           | `http://YOUR_IP:8282/api`           | Public base URL for API requests |

> [!IMPORTANT]  
> Keep in mind not to commit your `.env` file

```bash
cd ../../../../../ # go back to project root
 ```
- Build and run Containers 
```bash
docker compose build && docker compose up -d
  ```
- Visit the Website and Login

Open a Webbroser and enter the destination
```bash
<HostIp>:8282
 ```
You can also use the regular docker commands for building and running the containers. Change in the directory of the application you want to start and then 

For example ...

- Build the Container
```bash
docker build -t angular_frontend -f Dockerfile .
 ```

- Run the Container
```bash
docker run -d \
  --name angular_frontend \
  -p 8282:8282 \
  --restart on-failure \
  angular_frontend:latest
 ```




