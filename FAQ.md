# Questions regarding setup:

1. Q: How can I stop a running docker instance of Galaxy-GraphClust?

   A: If you are runnig the container in interactive mode (i.e. docker run -i) use `Ctrl+C`. To stop ALL docker instances on your computer you can run this command in terminal:
`sudo docker stop $(sudo docker ps -a -q)`

2. Q: In my Ubuntu host system the container is running but constantly reports error: `could not connect to server: Connection refused`

   A0: Minimum supported Linux kernel is 4.2, please get your kernel by running `uname -r`
   For e.e.g if you have Ubuntu 14.04 you can upgrade the kernel from 3.X to 4.2 version by this command.
   ```
   # For Ubuntu 14.04 with kernel 3.x
   sudo apt-get install linux-generic-lts-wily
   # Reboot the system and continue with A1
   ```
   
   A1: Docker manager is tightly coupled with the host Linux kernel. Under certain Linux kernel the docker storage system might fail. 
   Please proceed with the following commands or contact you administrator:

  ```
  sudo apt update; sudo apt upgrade;
  sudo apt-get install linux-image-extra-$(uname -r)  linux-image-extra-virtual
  sudo modprobe aufs
  sudo service docker stop
  sudo rm -rf /var/lib/docker/overlay*
  sudo service docker restart
  ```
  For more information please check Docker documentation: https://docs.docker.com/engine/userguide/storagedriver/aufs-driver/
  
  
