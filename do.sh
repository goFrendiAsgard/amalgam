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
zaruba please makeFastApiService generator.fastApi.service.name=myService
# Create module
zaruba please makeFastApiModule generator.fastApi.service.name=myService generator.fastApi.module.name=myModule
# Create custom route (optional)
zaruba please makeFastApiRoute generator.fastApi.service.name=myService generator.fastApi.module.name=myModule generator.fastApi.url=/hello
# Create event/RPC handler (optional)
zaruba please makeFastApiEventHandler generator.fastApi.service.name=myService generator.fastApi.module.name=myModule generator.fastApi.event.name=myEvent
zaruba please makeFastApiRpcHandler generator.fastApi.service.name=myService generator.fastApi.module.name=myModule generator.fastApi.rpc.name=myRPC
# Create CRUD
zaruba please makeFastApiCrud generator.fastApi.service.name=myService generator.fastApi.module.name=myModule generator.fastApi.crud.entity=book generator.fastApi.crud.fields=title,author,synopsis

# Create Service Task
zaruba please makeStaticServiceTask generator.service.location=fibo
zaruba please makeFastApiServiceTask generator.service.location=myService

# Create Docker Task
zaruba please makeRabbitmqDockerTask generator.docker.container.name=myRmq

# Run services
zaruba please run -t # NOTE: for do.sh, we need to add "-t" argument

# Or run services as container (press ctrl + c first)
zaruba please runContainer -t # NOTE: for do.sh, we need to add "-t" argument
zaruba please removeContainer

# ==== Stop here if you don't want to deploy on kubernetes ====

# Setup kubernentes client
zaruba please setupKubeClient

# Push images
zaruba please setProjectValue variable.name=dockerImagePrefix::default variable.value=stalchmst
zaruba please pushImage

# Make helm charts
zaruba please initHelm

# Create helm deployment values
zaruba please makeHelmDeployment generator.service.name=fibo
zaruba please makeHelmDeployment generator.service.name=myService

# Update environment
zaruba please updateEnv

# Helm apply
zaruba please helmApply kube.context=docker-desktop

# Helm destroy
zaruba please helmDestroy kube.context=docker-desktop

rm -Rf ./.git # NOTE: For do.sh only