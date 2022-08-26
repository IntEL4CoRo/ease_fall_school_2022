# ease_fall_school_2022

**WIP**

Introductory text about the fall school, docker, jupyter

## Docker Setup

### Linux

Install utility software first
```
sudo apt-get update
sudo apt-get install \
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
sudo apt-get install docker-compose
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

Check if the docker service is active: 
```
sudo systemctl restart docker.service
```

### Windows
- **Write install guide explicitly** 
https://docs.docker.com/desktop/install/windows-install/

### Mac
- **Write install guide explicitly** 
https://docs.docker.com/desktop/install/mac-install/

## Getting the Lecture's docker container

1. Download this repo as zip and unpack it
2. Open the terminal (bash, powershell, etc.) and change-directory to the repo (right-click in the unzipped repository)
3. Navigate to `Day1`
4. Execute `docker-compose up` and wait for the image to be pulled
