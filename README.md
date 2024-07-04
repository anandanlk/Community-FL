# Community-FL

# Proof of Concept: A Community-Based Collaborative Federated Learning Development and Automation Framework

## Architecture

![Architecture](https://github.com/anandanlk/Community-FL/blob/master/Architecture.png)
![Workflow] (https://github.com/anandanlk/Community-FL/blob/master/Workflow.png)

# I. Community FL Portal

- The Community FL Portal has four services named frontend, backend, database and jupyter-lab-extension.

Install Python 3.12 and create virtual environment.
Install the requirements for the backend and frontend using requirements.txt files in their respective directory.

## Backend and Database

The backend is developed using Python - FastAPI. This module is containerized and posted in dockerhub named anandanlk/communityfl_backend:latest. This runs on port 8088. It can be customized using .env file. The ORGINS and database url. For our poc, we have used MongoDB container as a dependent service with backend service.

## Frontend

The frontend is developed using reactjs. The backend url can be configured using .env file. This module is containerized and posted in dockerhub named anandanlk/communityfl_frontend:latest. This runs on port 3000.

## Jupyter Add-on

Instructions to customize Community Portal URL and add the extention to Jupyter lab:
Assumes the Jupyter Lab is installed in your computer.

1. Navigate to backend/jupyter-lab-extension
2. Execute the command 'npm install'
3. Configure URL in Package.json
4. Execute the command 'npx tsc'
5. Execute the command 'npm run build'
6. Execute the command 'jupyter labextension install .'
7. Launch the Jupyter lab

The backend, frontend and mongodb containers can be build and deployed using our docker-compose file using docker-compose-local.yml. It can be directly deployed from the Docker hub using docker-compose.yml.

The bstart and fstart can be used to start the backend and frontend servers locally but ensure to set proper execution method using chmod and also ensure a local mongodb is running and configured in the .env file. Also ensure to confire the required url and ports in backend and fronend .env files.

Note: If you building your own docker container, Buildx tool can be used to build images for both x86 and arm based archotecture and to push it to the dockerhub.

# II. Services and Docker Containers to run Decentralized FL Training.

> **_Please note:_** This project utilizes Federated Learning source code based on the repository mentioned in the Acknowledgments section.

## Description:

- This project provides a virtual research environment for community-based collaborative Federated Learning.
- Our FL workflows include 12 training rounds of federated learning based on MNIST dataset.
- Since we focus on Decentralized Federated learning scenario, our CWL workflow randomly selects one of the clients to act as the aggregator for each training round, updating the global model from the received client weights.

> **_Please note:_** We are not responsible for any use or misuse of the code or its consequences. For example we are not responsible for any expenses if you are using your own AWS or GCP account while using this demo nor for any security concerns.

- Changes needed:

  - Creating docker images for client training based on `Dockers_source_code/client_training`, `Dockers_source_code/client_registration` and pushing them to your docker hub to conduct any experiments.
  - Change the docker compose file `docker_compose_files/decentralized_compose.yml` with the name of your docker images
  - If you would like to use our Terraform template to create clients (nodes), Change the terraform template of the communication server based on your own aws configuration and your own name for the `Dockers_source_code/communication_server` docker image created. Feel free to follow your own template or manual process.

- FL clients state before running the experiment:

  - Clients that want to participate in the FL experiments should be running the docker compose file `docker_compose_files/decentralized_compose.yml`.

- Experiment Setup:
  Assuming you have already forked/cloned the Git repository. The data and 'client_compose.yml' files are available at https://github.com/anandanlk/Compose. This is public repo. Use Curl command to download these files in your clients.

Note: If you building your own docker container, Buildx tool can be used to build images for both x86 and arm based archotecture and to push it to the dockerhub.

## Acknowledgements

This project uses code from the following sources:

- A Kontomaris, Chronis (2023) CWL-FLOps: A Novel Method for Federated Learning Operations at Scale [https://github.com/CWL-FLOps/DecentralizedFL-CWL]

- Shaoxiong Ji. (2018, March 30). A PyTorch Implementation of Federated Learning. Zenodo. [http://doi.org/10.5281/zenodo.4321561](http://doi.org/10.5281/zenodo.4321561)

# III. Experiment Instructions:

1. Launch Jupyter Lab and Click Community FL Add on
2. Register in the portal (Create all types of users)
3. Follow the instruction in the portal and connect few Clients to the portal
4. Reserve/Advance Reserve the clients
5. Use the downloaded reserved_clients.json file in the Decentralized-FL\CWL_Workflow\find_clients_updated.py
6. Ensure you installed 'cwltool==3.1.20230127121939' and Initiate the CWL Training using the command 'time cwltool --enable-ext --parallel decentralizedFL.cwl decentralized_input.yml '
7. Unreserve the reserved clients in the portal.
