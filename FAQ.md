# Questions regarding setup:

1. Q: How can I stop a running docker instance of Galaxy-GraphClust?

   A: If you are runnig the container in interactive mode (i.e. docker run -i) use `Ctrl+C`. To stop ALL docker instances on your computer you can run this command in terminal: `sudo docker stop $(sudo docker ps -a -q)`

2. Q: In my Ubuntu host system the container is running but constantly reports error: `could not connect to server: Connection refused`

   A0: For Ubuntu users we recommend to use 16.04 LTS version which is deleivered with Kernel 4.2 or higher.
   
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
  
      
# Registration and Login: 
To have distinct history and workflows the Galaxy server requires each user to register for first access time. **By default anyone with access to the host network can register. No registration confirmation email will be sent to the given email.** So you can register with any custom (including non-existent) email address. There exist also a default Admin user [described here](https://bgruening.github.io/docker-galaxy-stable/users-passwords.html).  To change the default authorization settings please refer to the Galaxy Wiki section [Authentication](https://wiki.galaxyproject.org/Develop/Authentication) 

* To register (first time only):
    * On top right of the panel goto **User→Register**
    * Provide a custom email address and password, confirm your password and enter a public name

* To login:
    * On top right of the panel goto **User→Login**
    * Provide your registered email address and password

