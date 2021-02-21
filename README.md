# Amalgam

In this tutorial, we will explore how Zaruba might help you to:

* Create monorepo
* Clone existing project into your monorepo
* Create messagebus-ready CRUD Fastapi service
* Create tasks to run docker/services
* Run tasks

> 💀 __Amalgam:__ _​[countable, usually singular]_ amalgam (of something) (formal) a mixture or combination of things

# How it looks like

## Install go and git

Installing Zaruba is basically cloning it's repository and perform compilation.  In order to do that, you need `git` and `golang` to be installed in your computer.

```sh
sudo apt-get install git golang
```

## Install Zaruba

```sh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/state-alchemists/zaruba/master/install.sh)"
```

The installation script will clone zaruba's repository to your `~/.zaruba` and perform compilation.  It will also try to create symlink to `/usr/bin/zaruba` (that's why it needs root access).

You are encouraged to have a look at [the installation script](https://raw.githubusercontent.com/state-alchemists/zaruba/master/install.sh) in order to know see what really going on.

## Update Zaruba

This tutorial was tested by using `zaruba v0.3.0`. To show your current zaruba version, you can invoke `zaruba please showVersion`

```sh
zaruba please update
```

## Getting your machine ready

Currently zaruba only support ubuntu, for other operating system, you can install: `docker`, `python`, `pipenv`, and `netcat`.

```sh
sudo -E zaruba please setupUbuntu
zaruba please setup pyEnv
```

## Rock on

Now let's try to run the commands.

```sh

# Setup ubuntu
sudo -E zaruba please setupUbuntu

# Initiating monorepo project
mkdir myproject
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
zaruba please run

# Or run services as container (press ctrl + c first)
zaruba please runContainer
zaruba please removeContainer

# Setup kubernentes client
zaruba please setupKubeClient

# Push images
zaruba please setKwarg key=dockerImagePrefix::default value=stalchmst
zaruba please pushImage

# Make helm charts
zaruba please makeHelmCharts

# Create helm deployment values
zaruba please makeServiceDeployment location=fibo
zaruba please makeServiceDeployment location=myservice

# Update environment
zaruba please updateEnv

# Helm apply
zaruba please helmApply kubeContext=docker-desktop

# Helm destroy
zaruba please helmDestroy kubeContext=docker-desktop
```

Now you should have `rabbitmq`, `fibo`, and `myservice` running. All at once, just like [the three prime evils](https://diablo.fandom.com/wiki/Prime_Evil#The_Three_Brothers).

![Zaruba in action](amalgam-run.png)

This repo contains all generated tasks, so you can have a look and see what's going on.

# Setup Ubuntu

# Initialize Project

# Import External Repo

# Create FastAPI Service

# Create FastAPI Module

# Create FastAPI CRUD

# Create FastAPI Service Task

# Create Docker Task

# Run Services

# Run Services as Containers

# Setup Kubernentes Client

# Push Images

# Create Helm Charts

# Create Helm Deployment Values

# Deploy Helm