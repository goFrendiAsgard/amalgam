#!/bin/sh
set -e
sudo rm -Rf myproject

# Setup ubuntu
sudo -E zaruba please setupUbuntu

# Initialize project
mkdir -p myproject
cd myproject
zaruba please initProject

# Import external repo
zaruba please addSubrepo url="https://github.com/state-alchemists/fibonacci-clock" prefix="fibo"
zaruba please initSubrepos
zaruba please pullSubrepos

# Create FastAPI Service
zaruba please makeFastService location=myservice
# Create module
zaruba please makeFastModule location=myservice module=mymodule
# Create custom route (optional)
zaruba please makeFastRoute location=myservice module=mymodule url=/hello
# Create event/RPC handler (optional)
zaruba please makeFastEventHandler location=myservice module=mymodule event=myEvent
zaruba please makeFastRPCHandler location=myservice module=mymodule event=myRPC
# Create CRUD
zaruba please makeFastCRUD location=myservice module=mymodule entity=book fields=title,author,synopsis

# Create Service Task
zaruba please makeServiceTask location=fibo

# Create Docker Task
zaruba please makeDockerTask image=rabbitmq

# Run services
zaruba please run autostop

# Or run services as container (press ctrl + c first)
zaruba please runContainer autostop
zaruba please removeContainer

# Setup kubernentes client
zaruba please setupKubeClient

# Push images
zaruba please setKwarg key=dockerImagePrefix::default value=stalchmst
zaruba please pushImage

# Make helm charts
zaruba please makeHelmCharts

# Create helm deployments
zaruba please makeServiceDeployment location=fibo
zaruba please makeServiceDeployment location=myservice

# Update environment
zaruba please updateEnv

# Helm apply
zaruba please helmApply kubeContext=docker-desktop

# Helm destroy
zaruba please helmDestroy kubeContext=docker-desktop