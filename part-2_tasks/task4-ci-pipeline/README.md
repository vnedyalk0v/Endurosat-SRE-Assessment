# Task 4: CI Pipeline

## Overview

This task sets up a Continuous Integration (CI) pipeline for a simple Flask web application using GitHub Actions and Docker.

### Steps

1. **Create a Flask App**: A simple Flask app is created in the `webapp/` directory.
2. **Dockerize the App**: The app is containerized using a Dockerfile.
3. **Set Up CI Pipeline**: A GitHub Actions workflow is used to build and push the Docker image to DockerHub on every commit to the `main` branch.

### Requirements

- Python 3.9
- Docker
- GitHub Actions

### How to Run

1. Clone the repository.
2. The app can be run locally by navigating to `part-2_tasks/task4-ci-pipeline/webapp/` and running `docker build . -t ci-webapp` followed by `docker run -p 5000:5000 ci-webapp`.
3. CI will automatically trigger on commits to the main branch.
