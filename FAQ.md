# Questions regarding setup:

1. Q: How can I stop a running docker instance of Galaxy-GraphClust?

   A: If you are runnig the container in interactive mode (i.e. docker run -i) use `Ctrl+C`. To stop ALL docker instances on your computer you can run this command in terminal:
`docker stop $(docker ps -a -q)`

2. Q: In my Ubuntu host system the container is running but constantly reports error: `could not connect to server: Connection refused`

   A: Docker manager is tightly coupled with the host Linux kernel. Under certain Linux kernel the docker storage system might fail. 
   Please proceed with the following commands or contact you administrator:

  ```
  sudo apt update; sudo apt upgrade;
  sudo apt-get install linux-image-extra-$(uname -r)  linux-image-extra-virtual
  sudo modprobe aufs
  sudo service docker stop
  sudo rm -rf /var/lib/docker/overlay*
  sudo service docker restart
  ```
