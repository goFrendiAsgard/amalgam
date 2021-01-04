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

```sh
sudo apt-get install git golang
```

Installing Zaruba is basically cloning it's repository and perform compilation. 

In order to do that, you need `git` and `golang`.

## Install Zaruba

```sh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/state-alchemists/zaruba/master/install.sh)"
```

The installation script will clone zaruba's repository to your `~/.zaruba` and perform compilation. 

The installation script will also try to create symlink to `/usr/bin/zaruba`.

You are encouraged to see [the installation script](https://raw.githubusercontent.com/state-alchemists/zaruba/master/install.sh) to see what really going on.

## Getting your machine ready

```sh
sudo -E zaruba please setupUbuntu
```

Currently zaruba only support ubuntu, for other operating system, you can install: `docker`, `python`, `pipenv`, and `netcat`.

## Rock on

```sh
mkdir amalgam
cd amalgam

# Initiating monorepo project
zaruba please initProject

# Set and clone existing project to your monorepo
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

# Create Docker Task
zaruba please makeDockerTask image=rabbitmq

# Create Service Task
zaruba please makeServiceTask location=fibo
zaruba please makeServiceTask location=myservice

# Run services
zaruba please run
# Or run services as container (press ctrl + c first)
zaruba please runContainer
zaruba please removeContainer
# And push our images
# zaruba please setKwarg key=dockerRepo value=stalchmst
# zaruba please pushImage
```

Now you should have `rabbitmq`, `fibo`, and `myservice` running. All at once, just like [the three prime evils](https://diablo.fandom.com/wiki/Prime_Evil#The_Three_Brothers).