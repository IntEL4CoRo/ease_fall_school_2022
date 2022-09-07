# EASE Fall School 2022

**TODOs**

* Introductory text about the fall school, docker, jupyter
* Add directory for the other lectures and create a readme at least, if they don't use docker
* Add Windows Docker install
* Add Mac Docker install
* don't use docker desktop for linux, on windows there's no other option though

## Enable Hardware-Virtualization

VT-x for intel, AMD-V for AMD chips

https://www.virtualmetric.com/blog/how-to-enable-hardware-virtualization


## Docker Setup

<details><summary>Linux</summary>

Install utility software first
```
sudo apt update
sudo apt install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

</details>

### Linux

Install utility software first
```
sudo apt update
sudo apt install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```
Get keyring and Docker's package references
```
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
Install docker-compose
```
sudo apt install docker-compose
```
#### Linux Postinstall ([troubleshoot here](https://docs.docker.com/engine/install/linux-postinstall/))
```
sudo groupadd docker # this may have already happened by installing docker
sudo usermod -aG docker $USER
newgrp docker # Or re-login to activate the changes in the usergroup
```
Test installation and postinstall with 
```
docker run hello-world
```
Allow docker to open x-Applications, like the robot simulator
```
xhost +local:docker
```
#### Troubleshoot when using docker:

When `docker run hello-world` doesn't work because of missing permissions, check
```
groups
```
and see if `docker` is listed. If it's not, check the *Linux Posinstall* above. If it is, re-login or reboot you machine to reset user permissions.

If `docker-compose up` (see below, when starting a lecture) complains about connectivity issues, restart the docker service and socket:
```
sudo systemctl restart docker.service
sudo systemctl restart docker.socket
```

If it still doesn't work, reinstall docker. First remove the current installation
```
sudo apt prune docker-compose
```
and start from the top. `docker-compose` installs all the other required docker packages to run the lecture.

### Windows
- **Write install guide explicitly** 
https://docs.docker.com/desktop/install/windows-install/

#### Install WSL2 (Windows Subsystem for Linux)
https://docs.microsoft.com/en-us/windows/wsl/install
* Open Powershell as administrator
* `wsl --install -d Ubuntu-20.04`
* [upgrade to WSL 2](https://docs.microsoft.com/en-us/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package)
* [install docker desktop](https://docs.docker.com/desktop/install/windows-install/#install-docker-desktop-on-windows)
* restart your PC to install the system updates
* run Docker Desktop **as administrator** and wait. Launching Docker for the first time takes long.
* in the meantime, install `xLauncher`
* TODO: how to set up xLauncher

* download this repository as zip and unzip it
* open Powershell **as administrator**
* Copy the path to the unzipped repository
* navigate to that directory with `cd <the path that you copied>`
* TODO: set DISPLAY Variable
* in Powershell execute `docker-compose up`
* wait for the image to be downloaded and executed
* copy the 127.x.x.x URL and put it into your favourite browser

### Mac
- **Write install guide explicitly** 
https://docs.docker.com/desktop/install/mac-install/

## Cleaning up docker images

Docker can clutter your machine a lot, especially when you build your own images. Use the following commands to get rid uf unused images and containers.
```
docker image prune
docker container prune
```

## Getting the Lecture's docker container

1. Download this repo as zip and unpack it
2. Open the terminal (bash, powershell, etc.) and change-directory to the repo (right-click in the unzipped repository)
3. Navigate to `Day1`
4. Execute `docker-compose up` and wait for the image to be pulled
