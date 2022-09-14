# EASE Fall School 2022

**TODOs**

* Introductory text about the fall school, docker, jupyter
* Add directory for the other lectures and create a readme at least, if they don't use docker
* Add Windows Docker install
* Add Mac Docker install
* Don't use docker desktop for linux, on windows there's no other option though

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

</details>

<details>
    <summary>Windows</summary>
Docker on Windows needs a Linux kernel, this is solved with Windows Subsystem for Linux (WSL). And since we are running the robot simulation as an OpenGL application in the Docker container, we also need proper x-forwarding back to the Windows display to visualize it.

* Activate Windows Subsystem for Linux
  * Press the `Windows` key, type `features` and execute `Turn Windows Features on or off`
  * Scroll down to `Windows Subsystem for Linux` and check the box
* Upgrade to WSL2, it's got important functionality
  * Check, if your CPU is capable of WSL2 with the Powershell command `systeminfo` and look for 'System Type' (in your machines language, e.g. 'Systemtyp' in german). it must be an x64-based architecture. If it's not, use the Virtualbox VM instead.
  * [WSL2 upgrade installer download](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi)
  * [WSL2 upgrade documentation](https://docs.microsoft.com/en-us/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package)
* Install the Ubuntu 20.04 distribution
  * Open Powershell **as administrator**
  * if you already have an Ubuntu 20.04 distro installed on you machine, save it with `wsl --export Ubuntu-20.04 <some path and filename where you want to export it to>.tar`, then remove it from wsl with `wsl --unregister Ubuntu-20.04`. You can import it back later with `wsl –import <Image Name you choose> <Directory to store and run the image> <Directory location of the exported .tar file>`. [source](https://4sysops.com/archives/export-and-import-windows-subsystem-for-linux-wsl/)
  * `wsl --set-default-version 2` to set WSL2 as default
  * `wsl --list --online` shows all available Linux distribution that can be installed
  * `wsl --install -d Ubuntu-20.04` because Ubuntu 20.04 is that we're working with.
  * this may take a while...
  * `wsl --list --version` checks the installed distributions. Make sure that Ubuntu-20.04 is among them. Otherwise install it again. If that doesn't work, check if Hardware Virtualization is enabled in the BIOS and try again.
  * upgrade to WSL 2
    
  * In Powershell: `wsl` should get you into the Ubuntu-20.04 system
    * Update package references with `sudo apt update`
    * Install updates with `sudo apt upgrade`
    * Install opengl with `sudo apt install mesa-utils`
* install docker desktop
  * [installer download](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe)
  * [documentation](https://docs.docker.com/desktop/install/windows-install/)
  * restart your PC to install the system updates
  * run Docker Desktop **as administrator** and wait. Launching Docker for the first time takes long.

* **TODO: install and setup xLaunch and configure xhost access and DISPLAY setup**
* install xMing
  * [documentation](http://www.straightrunning.com/XmingNotes/)
  * [installer download](https://sourceforge.net/projects/xming/files/Xming/6.9.0.31/Xming-6-9-0-31-setup.exe/download)

* download this repository as zip and unzip it
* open Powershell **as administrator**
* Copy the path to the unzipped repository
* navigate to that directory and into a specific `DayX` with `cd <the path that you copied>`
* in Powershell, execute `docker compose --file <the docker-compose yml file name for Windows> up`
* wait for the image to be downloaded and executed
* copy the 127.x.x.x URL and put it into your favourite browser

</details>

<details>
    <summary>Mac</summary>

- **Write install guide explicitly** 

https://docs.docker.com/desktop/install/mac-install/ 

</details>

## Cleaning up docker images

Docker can clutter your machine a lot, especially when you build your own images. Use the following commands to get rid uf unused images and containers.
```
docker image prune
docker container prune
```

## Getting the Lecture's docker container

1. Download this repo as zip and unpack it
2. Open the terminal (bash, powershell, etc.) and change-directory (`cd`) to the repo
3. Navigate to `DayX` (e.g. `Day1`)
4. Execute `docker-compose --file docker-compose-<your OS specific suffix> up` and wait for the image to be pulled
      (for Windows users it's `docker compose ...` without the dash)
5. copy the URL from the terminal into your favourite browser
