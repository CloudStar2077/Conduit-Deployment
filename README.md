# Conduit-Deployment

This guide explains how to Setup a CI/CD pipeline with GitHub Actions and GitHub Container Registry

# Table of Contents

1. [Prerequisites](#Prerequisites) 
2. [Quickstart](#Quickstart) 
3. [Usage](#Usage)

## Prerequisites

- SSH
- Docker (version 20.10 or higher) installed
- Git installed

## Quickstart

- Clone Repository 
```bash
git clone git@github.com:CloudStar2077/Conduit-Deployment.git &&
cd Conduit-Deployment
 ```
Before you can start the Workflow you first have to generate a SSH Github-Actions-Key on your server and add it to the authorized_keys file.
```bash
ssh-keygen -t ed25519 -C "github-actions-key" -f ~/.ssh/github-actions-key && cat ~/.ssh/github-actions-key.pub >> ~/.ssh/authorized_keys
 ```
Set file permissions 
```bash
chmod 700 ~/.ssh                                  
chmod 600 ~/.ssh/authorized_keys
chmod 600 ~/.ssh/github-actions-key
chmod 644 ~/.ssh/github-actions-key.pub
 ```
Then add your GitHub Actions private key and all other sensitive values in the GitHub UI. This includes the private SSH GitHub Actions key `(SSH_PRIVATE_KEY)`, the server user `(SSH_USER)`, the server IP `(SSH_HOST)`, the Personal Access Token `(GHCR_TOKEN)`, the GitHub username `(GHCR_USERNAME)`, as well as application variables such as `DJANGO_SECRET_KEY`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `DJANGO_ALLOWED_HOSTS`, `PORT`, and `API_BASE_URL`(Host IP).
Create a Personal Access Token (PAT) with the permissions `read:packages` and `write:packages`. Also add a separate Deploy Key to the repository to allow pushing from the server to GitHub.
Finally, set the repository's workflow permissions to Read and Write.
```bash
Github Settings --> Developer Settings --> Personal acces tokens
Github Repository Settings --> Deploy Keys
Github Repository Settings --> Secrets --> Actions --> New repository secret
Github Repository Settings --> Actions --> General --> Workflow Permissions
```


To start the Workflow 
```bash
git commit --allow-empty -m "trigger workflow" && git push origin main  
 ```
In the GitHub Actions UI, you can check if the workflow run was successful ✅.

Visit the Conduit Website and Login.

Open a Webbroser and enter the destination
```bash
<HostIp>:<HostPort>
 ```

## Usage

- Clone the repository 

```bash
git clone git@github.com:CloudStar2077/Conduit-Deployment.git &&
cd Conduit-Deployment
  ```

This project uses the `deployment.yml` a fully automated CI/CD pipeline based on GitHub Actions, which is triggered with every push to the main branch. The pipeline is composed of two back-to-back jobs.
Before the first use, several prerequisites had to be configured. A dedicated SSH key (`github-actions-key`) was generated on the production server, and its public key was added to the servers `authorized_keys` file. This allows the GitHub Actions runner to establish a passwordless SSH connection to the server.
```bash
ssh-keygen -t ed25519 -C "github-actions-key" -f ~/.ssh/github-actions-key && cat ~/.ssh/github-actions-key.pub >> ~/.ssh/authorized_keys
 ```
For authentication via SSH through GitHub Actions, the permissions of the `.ssh` folder as well as the private and public keys must be set correctly, as SSH rejects insecure file permissions.
```bash
chmod 700 ~/.ssh    
chmod 600 ~/.ssh/authorized_keys
chmod 600 ~/.ssh/github-actions-key
chmod 644 ~/.ssh/github-actions-key.pub
 ```

For access to the GitHub Container Registry, a Personal Access Token (PAT) with the permissions `read:packages` and `write:packages` was also created. 
All sensitive values were then stored as GitHub Secrets in the repository. These include the private SSH github-actions-key (`SSH_PRIVATE_KEY`), the server user (`SSH_USER`), the server IP (`SSH_HOST`), the registry token (`GHCR_TOKEN`), the GitHub username (`GHCR_USERNAME`), as well as all application variables such as `DJANGO_SECRET_KEY`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `DJANGO_ALLOWED_HOSTS`, `PORT`, and the `API_BASE_URL`(Host IP).
```bash
Github Settings --> Developer Settings --> Personal acces tokens
Github Repository Settings --> Deploy Keys
Github Repository Settings --> Secrets --> Actions --> New repository secret
```
<img width="1137" height="915" alt="2026-04-13_19-42" src="https://github.com/user-attachments/assets/4190ec6a-f715-4112-a75b-ecebe5717628" />

Additionally the repository's workflow permissions were set to Read and Write so that the Github_Token can be used for authentication with the GitHub Container Registry. 
```bash
Github Repository Settings --> Actions --> General --> Workflow Permissions
```

Job 1 – Build & Push

In the first job, the Docker images for the backend and frontend are built directly on the GitHub Actions runner and then pushed to the GitHub Container Registry (`ghcr.io`).
During build time, the frontend image receives the API URL as a build argument sourced from the GitHub Secrets. In the frontend Dockerfile, a `sed` command replaces the placeholder `http://YOUR-IP:YOUR-PORT/api` in `api.config.ts` with the actual URL before Angular compiles the application. This ensures that no sensitive configuration values are stored in the repository.

Job 2 – Deploy

The second job handles deployment to the production server and only starts after Job 1 has completed successfully.
Using the SSH connection, the latest version of the repository is first pulled onto the server. Afterwards, the `.env` file is regenerated using the GitHub Secrets. Then the previously built images are pulled from the container registry, and the application is started in detached mode using Docker Compose.
If any step fails, the workflow stops with an error, and the deployment is not executed.

This architecture ensures that the build process does not take place on the production server. The production server is only responsible for running the finished containers.
Separating the build and runtime environments increases system stability, reduces the resource load on the production server, improves security, and enables reproducible deployments.

To start the Workflow go by 
```bash
git commit --allow-empty -m "trigger workflow" && git push origin main   # --allow-empty is used because there are noch changes in the repo
 ```
In the GitHub Actions UI, you can check if the workflow run was successful. ✅

- Visit the Website and Login

Open a Webbroser and enter the destination
```bash
<HostIp>:<HostPort>
 ```
