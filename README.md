# EASE Fall School 2022

This guide is for the lectures that run in a virtualized enviroment, which are Day1, Day2 and Day4.

**TODOs**

* Introductory text about the fall school, docker, jupyter
* Add Mac Docker install (do we offer Docker for Mac?)

## Enable Hardware-Virtualization

Hardware Virtualization is a setting for your CPU, that enables it to run virtual operating systems on your host machine. Depending on your host system, the lectures of the Fall School run in Docker, the Windows Subsystem for Linux or a VirtualBox VM. All of these option use virtualization of another operating system underneath your existing one. We offer our software like that, such that we can ensure that it runs on a manifold of different systems. 

VT-x for intel, AMD-V for AMD chips

https://www.virtualmetric.com/blog/how-to-enable-hardware-virtualization

### Get into your BIOS

On Linux, shutdown the machine and boot after that (rebooting sometimes doesn't load the BIOS with fast-boot settings)

On Windows, go to the Windows menu (bottom left) > Power > hold the Shift-key while clicking Restart. It will reboot into a blue UI. Choose Troubleshoot, Change behaviour on boot, Restart. This prevents Windows from fast-booting.

When the mainboard prompts, press one of the suggested buttons (F2, F9, F12, DEL, etc.), or do so while it boots like once a second. Go to 'Advanced' and search for Hardware Virtualization, VT-x or AMD-V, something like that. The menus are different for every mainboard. Save and boot.

On Windows it offers some options for recovery, which is from the chosen troubleshoot before. Just ESC out of it.

## How do you want to do this?

Depending on your system, your choice may be limited. but we got you covered. These are the options we offer:

* Option 1: Docker image -- Linux native (tested with Debian)
* Option 2: WSL2 tar-ball import with pre-installed Docker -- Windows + WSL2 + VcXsrv (tested with Win10)
* Option 3: VirtualBox image -- fallback for any OS whatsoever

## Update the lecture's content

In any case, update the lecture content with `cd <path to the EASE repo>` and then `git pull`, to get the latest version. We're constantly adding new stuff, probably even a few moments before the lecture starts!

## Option 1: Docker Setup (recommended for Linux)

<details>
<summary>Linux</summary>

We're going to do x-forwarding with OpenGL later, which hasn't been tested with the Wayland display manager, but with x11. Check your display manager like this:
```
loginctl show-session $(awk '/tty/ {print $1}' <(loginctl)) -p Type | awk -F= '{print $2}'
```
If you want to switch to gdm3 (x11), [follow this guide](https://linuxconfig.org/how-to-enable-disable-wayland-on-ubuntu-20-04-desktop).

Install utility software before installing Docker
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
Start the docker daemon (`sudo dockerd` if you don't use systemctl, or use [this procedure](https://medium.com/geekculture/run-docker-in-windows-10-11-wsl-without-docker-desktop-a2a7eb90556d) to run dockerd automatically on boot)
```
sudo systemctl restart docker.service
sudo systemctl restart docker.socket
# or run 'sudo dockerd' if you don't use systemctl 
```
Test installation and postinstall.
```
docker run hello-world
```
Allow docker to open x-Applications, like the robot simulator
```
sudo apt install x11-xserver-utils # installs the utils to allow foreign displays
xhost +local:docker # allows x-forwarding for the 'docker' group
```
#### Troubleshoot when using docker:
When xhost can't open the Display, find it with
```
ps -u $(id -u) -o pid= \
    | xargs -I PID -r cat /proc/PID/environ 2> /dev/null \
    | tr '\0' '\n' \
    | grep ^DISPLAY=: \
    | sort -u
```
and set it with
```
export DISPLAY=:0 # or :1. Put this line in your ~/.bashrc file
```
    
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
If systemctl makes issues, try
```
sudo dockerd
```
or use [this procedure](https://medium.com/geekculture/run-docker-in-windows-10-11-wsl-without-docker-desktop-a2a7eb90556d) to run `dockerd` automatically on boot.
    
If it still doesn't work, reinstall docker. First remove the current installation
```
sudo apt prune docker-compose
```
and start from the top. `docker-compose` installs all the other required docker packages to run the lecture.

</details>

<details>
    <summary>Windows</summary>
    
    
Docker on Windows needs a Linux kernel, this is solved with Windows Subsystem for Linux (WSL). And since we are running the robot simulation as an OpenGL application in the Docker container, we also need proper x-forwarding back to the Windows display to visualize it. Check the [docker install](https://docs.docker.com/desktop/install/windows-install/) and [WSL with VcXsrv x-server](https://medium.com/javarevisited/using-wsl-2-with-x-server-linux-on-windows-a372263533c3) guides yourself if you want, this is the gist of it. 

#### Set up Ubuntu 20.04 with WSL2
    
* Activate Windows Subsystem for Linux
  * Press the `Windows` key, type `features` and execute `Turn Windows Features on or off`
  * Scroll down to `Windows Subsystem for Linux` and check the box
* Upgrade to WSL2, it's got important functionality
  * Check, if your CPU is capable of WSL2 with the Powershell command `systeminfo` and look for 'System Type' (in your machines language, e.g. 'Systemtyp' in german). it must be an x64-based architecture. If it's not, use the Virtualbox VM instead.
  * [WSL2 upgrade installer download](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi)
  * [WSL2 upgrade documentation](https://docs.microsoft.com/en-us/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package)
* Install the Ubuntu 20.04 distribution
  * Open Powershell **as administrator**
  * `wsl --set-default-version 2` to set WSL2 as default
  * `wsl --list --version` checks installed distributions, it should be empty
    * `wsl --export Ubuntu-20.04 ./Ubuntu2004Backup.tar` can export your existing Ubuntu 20.04 distro, if you already installed one and want to keep it. Then remove it from wsl with `wsl --unregister Ubuntu-20.04`. You can import it back later like this: `wsl --import backup C:\Users\test\Documents\Ubuntu2004Backup C:\Users\test\Documents\Ubuntu2004Backup.tar ` [which is explained here](https://4sysops.com/archives/export-and-import-windows-subsystem-for-linux-wsl/).
  * `wsl --list --online` shows all available Linux distribution that can be installed
  * `wsl --install -d Ubuntu-20.04` will open a window, which is the **Ubuntu shell** installing itself.
  * This may take a while...
  * In the Ubuntu shell, specify username and password when the install is done. Keep it simple, it's just for experimental purpose.
  * In the Powersehll: `wsl --list --version` checks the installed distributions. Make sure that Ubuntu-20.04 is among them. Otherwise install it again, the previous install may have been interrupted by something. If that still doesn't work, check **Enable Hardware-Virtualization** at the top of this readme.
  * `wsl --set-default Ubuntu-20.04` sets the fresh distro as default.
* Update the Ubuntu 20.04 distro and install OpenGL utils
  * Open the **Ubuntu shell** with `Windows`-key, 'Ubuntu', Enter.
  * `sudo apt update` updates package references
  * `sudo apt upgrade` installs updates. This may take a while...
  * `sudo apt install mesa-utils` installs OpenGL utilities to test the x-forwarding
  
    
Congratulations, you got yourself a Linux system running on Windows. 

#### Set up VcXsrv as x-server for OpenGL applications

VcXsrv is an X-server, that is able to visualize OpenGL application from remote connections. We use it, because the Docker container is a kind of headless machine that  can only render the robot-simulator internally, but can not visualize without a display to show it. VcXsrv is providing the display such that the Docker application can connect to that display. [This guide](https://medium.com/javarevisited/using-wsl-2-with-x-server-linux-on-windows-a372263533c3) is the foundation for ours.
    
* [Download and install VcXsrv](https://sourceforge.net/projects/vcxsrv/)
* Go to the installed folder, it should be in `C:\Program Files\VcXsrv`
* Right-click the `vcxsrv.exe` to `Create shortcut` to the desktop
* Configure the `VcXsrv.exe - Shortcut`
    * Go to the Desktop and right-click the shortcut, select `Properties` > `Shortcut` > `Target` and append the following to the existing entry:
    * ` :0 -ac -terminate -lesspointer -multiwindow -clipboard -wgl -dpi auto`
    * Then it should look somewhat like this: `"C:\Program Files\VcXsrv\vcxsrv.exe" :0 -ac -terminate -lesspointer -multiwindow -clipboard -wgl -dpi auto`
    * `OK` out of the window
* Execute the shortcut of VcXsrv. It appears that nothing happens. Check the tray icons in the bottom-right corner, there it should show it.
* Adjust Firewall settings
    * Since the display connection is something that Windows' Firewall classifies as dangerous, we need to allow that connection.
    * Open Firewall settings with `Windows`-key, 'firewall with advanced', enter
    ![fw-settings](https://user-images.githubusercontent.com/13121212/190249123-947acf13-17ed-4654-b78f-d0b160ef9303.PNG)

* Test the VcXsrv server
    * Open the **Ubuntu shell** with `Windows`-key, 'Ubuntu', Enter
    * `echo $'export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk \'{print $2}\'):0.0' >> ~/.bashrc`
      * This will automatically read the address of the VcXsrv display and set the environment variable `DISPLAY` to that address, every time you open the Ubuntu shell.
      * `source ~/.bashrc` to update the DISPLAY variable from our global changes
      * `echo $DISPLAY` to check if it is set to something like `127.xx.xx.xx:0.0`
    * `glxgears` will open up a windows with moving gears.
    * If that works, the VcXsrv OpenGL forwarding is set up successfully!
    * If `glxgears` is stuck for a long time or unable to find the display, check the `DISPLAY` variable in your Ubuntu shell and Firewall settings again.
    * If `glxgears` command couldn't be found, do `sudo apt install mesa-utils` to get it.

#### Install Docker
    
* Install docker desktop
  * [installer download](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe)
  * [documentation](https://docs.docker.com/desktop/install/windows-install/)
  * restart your PC to install the system updates
  * run Docker Desktop **as administrator**
    * Accept the license agreements
    * Wait for the status indicator to turn from yellow to green
      * If it turns to red, check **Enable Hardware-Virtualization** (at the beginning of this readme) to enable VMs in your BIOS settings
  
#### Run the lecture  
    
* Download this repository as zip and unzip it
* Open the `docker-compose-windows.yml` in Day1 to adjust the DISPLAY variable
    * In **Ubuntushell** check `echo $DISPLAY`
    * Copy-paste the resulting address as value for `DISPLAY` in the `docker-compose-windows.yml`
* Open Powershell **as administrator**
* Copy the path to the unzipped repository
* navigate to that directory and into a specific `DayX` with `cd <the path that you copied>`
* in Powershell, execute `docker compose --file ./docker-compose-windows.yml up`
* wait for the image to be downloaded and executed
* copy the '127.x.x.x:8888/some-authentication-token' URL and put it into your favourite browser

</details>

<details>
    <summary>Mac</summary>

Not tested, but [here's the install guide](https://docs.docker.com/desktop/install/mac-install/). Use on your own risk.

There's no guide to establish X-Forwarding out of the Docker container yet. Feel free to help us find a solution!

</details>

### Cleaning up Docker

Docker can clutter your machine a lot, especially when you build your own images. A container can hold you back from removing images that it uses, so remove the container first, then the image. We re-use the same Docker image between the different lectures, so it's only downloaded once. But each lecture runs it's own container, which prevents another lecture to re-use the same image. Use the following commands to clean up.
```
docker images          # lists images
docker container list  # lists containers

docker system prune     # clears unused containers, images, networks and volumes all at once, in a safe manner
docker container prune  # clears unused containers in a safe manner
docker image prune      # clears unused images in a safe manner

docker container stop <container id>  # stops the container

# These will destroy stuff, so be careful. You can easily rebuild it with docker-compose
docker container rm <container id>    # removes the container
docker image rm <image name>          # removes an image, if no container is using it
```

### Getting the Lecture's docker container

1. Download this repo as zip and unpack it, or use `git clone https://github.com/IntEL4CoRo/ease_fall_school_2022.git` if you have git installed.
2. Open the terminal (bash, powershell, etc.) and change-directory (`cd`) to the repo
3. Navigate to `DayX` (e.g. `Day1`)
4. Execute `docker-compose up` and wait for the image to be pulled
5. copy the URL from the terminal into your favourite browser

## Option 2: WSL2 image install (recommended for Windows)

Windows Subsystem for Linux manages Linux distributions (operating systems) on a Windows host machine. Running the lecture directly from WSL is way smoother that from Docker, at least for Windows host machines, because it utilized the GPU for rendering, while Docker only works on the CPU, for now. We prepared a WSL image, which is based on Ubuntu 20.04 and has all the necessary software preinstalled, so you can plug and play the lectures. 
    
### Import the WSL image into your WSL
Most of these steps are elaborated in the Docker setup for Windows, like VcXsrv, WSL2 and Firewall setup.
    
1. Enable Hardware Virtualization
2. [Download the WSL image](https://seafile.zfn.uni-bremen.de/f/ca86a4d578a94bafa592/)
3. [Install, configure and launch VcXsrv](https://medium.com/javarevisited/using-wsl-2-with-x-server-linux-on-windows-a372263533c3)
4. Enable Windows Subsystem for Linux in 'Turn Windows features on or off'
5. Reboot your system to install the change
6. Download and install [the WSL 2 update](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi)
7. Open Powershell **as administrator**
```
wsl --set-default-version 2
```
8. If it tells to enable virtualization, check the BIOS settings again to enable Hardware Virtualization (see also the beginning of this readme).
9. If you got any existing Ubuntu-20.04 distro installed, export it with
```
wsl --export Ubuntu-20.04 C:\Users\$env:UserName\Documents\Ubuntu-20.04-Backup.tar
```
Then remove it
```
wsl --unregister Ubuntu-20.04
```
10. Import the prepared distro into WSL from Powershell with 
```
wsl --import Ubuntu-20.04 C:\Users\$env:UserName\Documents\Ubuntu-20.04-FS C:\Users\$env:UserName\Downloads\UbuntuFS.tar 
```
11. Set the image as default with
```
wsl --set-default Ubuntu-20.04
```
12. Launch Ubuntu-20.04 from the windows menu and enter the password 'cram' for the username 'cram'.
13. Set Firewall to allow WSL comunication. Easiest by disabeling Firewall for public networks, but you can add a rule for WSL.
14. `glxgears` will test the x-forwarding to VcXsrv. If nothing happens, check the VcXsrv and Firewall setup.
    
## Option 3: Use the VirtualBox image (recommended for MacOS and unmentioned OS)
    
We tested the setup extensively with all our available capabilities, which exludes non-x64 CPUs, non-Debian Linux systems, Win11 and 8.1, MacOS and other unmentioned operating systems. This means, that the above mentioned options may not work for your specific machine. If you want to save yourself some time and trouble, use [this Virtualbox image](https://seafile.zfn.uni-bremen.de/d/0728fcdc7bb14db7819f/) and check out [this guide](https://cram-system.org/tutorials/demo/fetch_and_place) for how to configure it. Keep in mind though, that this VM will perform much worse and should only be used as a fallback. 
