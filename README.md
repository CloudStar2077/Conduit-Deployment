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
Before building the docker image

## Usage

The project uses a fully automated CI/CD pipeline based on GitHub Actions, which is triggered with every push to the main branch. The pipeline is composed of two back-to-back jobs.
Before the first use, several prerequisites had to be configured. A dedicated SSH key (`github-actions-key`) was generated on the production server, and its public key was added to the server’s `authorized_keys` file. This allows the GitHub Actions runner to establish a passwordless SSH connection to the server.
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
`Github Settings --> Developer Settings --> Personal acces tokens`. To enable `git pull` on the server, a separate Deploy Key was generated and added to the repository under `Github Repository Settings --> Deploy Keys`.
All sensitive values were then stored as GitHub Secrets in the repository. `Github Repository Settings --> Secrets --> Actions --> New repository secret`. These include the private SSH key (`SSH_PRIVATE_KEY`), the server user (`SSH_USER`), the server IP (`SSH_HOST`), the registry token (`GHCR_TOKEN`), the GitHub username (`GHCR_USERNAME`), as well as all application variables such as `DJANGO_SECRET_KEY`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `DJANGO_ALLOWED_HOSTS`, `PORT`, and `API_BASE_URL`.
Additionally the repository's workflow permissions were set to Read and Write so that the GITHUB_TOKEN can be used for authentication with the GitHub Container Registry. `Github Repository Settings --> Actions --> General --> Workflow Permissions`

```bash
git commit --allow-empty -m "trigger workflow" && git push origin main
 ```
 
Job 1 – Build & Push

In the first job, the Docker images for the backend and frontend are built directly on the GitHub Actions runner and then pushed to the GitHub Container Registry (`ghcr.io`).
During build time, the frontend image receives the API URL as a build argument sourced from the GitHub Secrets. In the frontend Dockerfile, a `sed` command replaces the placeholder `http://YOUR-IP:YOUR-PORT/api` in `api.config.ts` with the actual URL before Angular compiles the application. This ensures that no sensitive configuration values are stored in the repository.

Job 2 – Deploy

The second job handles deployment to the production server and only starts after Job 1 has completed successfully.
Using the SSH connection, the latest version of the repository is first pulled onto the server. Afterwards, the `.env` file is regenerated using the GitHub Secrets. Then, the previously built images are pulled from the container registry, and the application is started in detached mode using Docker Compose.
If any step fails, the workflow stops with an error, and the deployment is not executed.

This architecture ensures that the build process does not take place on the production server. The production server is solely responsible for running the finished containers.
Separating the build and runtime environments increases system stability, reduces the resource load on the production server, improves security, and enables reproducible deployments.
