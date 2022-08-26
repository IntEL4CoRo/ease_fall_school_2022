# ease_fall_school_2022

**WIP**

Introductory text about the fall school, docker, jupyter

## Docker Setup

### Linux

- **mabe just do docker dektop**

```
sudo apt install docker.io
```

Troubleshoot when using docker:

Check if docker is active run: `sudo systemctl status docker`. If status is not active, activate it run: `sudo systemctl enable --now docker`

- To install docker-compose
```
sudo apt install docker-compose
```
- **ADD POSTINSTALL GUIDE**
Note: it is recommended to create docker group refer: https://docs.docker.com/engine/install/linux-postinstall/, However not mandatory.

- Allow docker to open x-Applications, like the robot simulator
`xhost +local:docker`

### Windows
- put link to install guide

### Mac
- put link to install guide

## Getting the Lecture's docker container

1. Download this repo as zip and unpack it
2. Open the terminal (bash, powershell, etc.) and change-directory to the repo (right-click in the unzipped repository)
3. Navigate to `Day1`
4. Execute `docker-compose up` and wait for the image to be pulled
