#!/bin/sh
set -e
sudo rm -Rf myproject

# Setup ubuntu
sudo -E zaruba please setupUbuntu
zaruba please setupPyenv

# Initialize project
rm -Rf myProject # NOTE: for do.sh only
mkdir -p myproject
cd myproject
zaruba please initProject

# Import external repo
zaruba please addSubrepo subrepo.url="https://github.com/state-alchemists/fibonacci-clock" subrepo.prefix="fibo"
zaruba please initSubrepos
zaruba please pullSubrepos

# Create FastAPI Service
zaruba please makeFastService generator.service.location=myservice
# Create module
zaruba please makeFastModule generator.service.location=myservice generator.module.name=mymodule
# Create custom route (optional)
zaruba please makeFastRoute generator.service.location=myservice generator.module.name=mymodule generator.url=/hello
# Create event/RPC handler (optional)
zaruba please makeFastEventHandler generator.service.location=myservice generator.module.name=mymodule generator.event.name=myEvent
zaruba please makeFastRPCHandler generator.service.location=myservice generator.module.name=mymodule generator.event.name=myRPC
# Create CRUD
zaruba please makeFastCRUD generator.service.location=myservice generator.module.name=mymodule generator.crud.entity=book generator.crud.fields=title,author,synopsis

# Create Service Task
zaruba please makeServiceTask generator.service.location=fibo

# Create Docker Task
zaruba please makeDockerTask generator.docker.image=rabbitmq

# Run services
zaruba please run autostop # NOTE: for do.sh, we need to add "autostop" argument

# Or run services as container (press ctrl + c first)
zaruba please runContainer autostop # NOTE: for do.sh, we need to add "autostop" argument
zaruba please removeContainer

# Setup kubernentes client
zaruba please setupKubeClient

# Push images
zaruba please setProjectValue variable.name=dockerImagePrefix::default variable.value=stalchmst
zaruba please pushImage

# Make helm charts
zaruba please makeHelmCharts

# Create helm deployment values
zaruba please makeServiceDeployment generator.service.location=fibo
zaruba please makeServiceDeployment generator.service.location=myservice

# Update environment
zaruba please updateEnv

# Helm apply
zaruba please helmApply kube.context=docker-desktop

# Helm destroy
zaruba please helmDestroy kube.context=docker-desktop