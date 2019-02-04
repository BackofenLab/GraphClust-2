# Questions regarding setup and usage:

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
  sudo rm -rf /var/lib/docker/overlay2
  sudo service docker restart
  ```
  For more information please check Docker documentation: https://docs.docker.com/engine/userguide/storagedriver/aufs-driver/
 
3.  Q: After a few experiments and upgrades, lots of disk storage is occupied. How can I clean it up?

Docker takes a conservative approach for cleaning up unnecessary data objects. Below some solutions for cleaning up your hard disk is coming, ordered in the level of conservativeness:

* Using `docker system prune` command, manual [here](https://docs.docker.com/config/pruning/)
* Please make sure no unintended container instance is running on the background. You can get a list of all containers with `docker ps -a` and remove them if necessary with `docker rm ID-or-NAME`.
* The above steps do not remove the dangling and not needed images which usually take most of the space. You can use `docker images` to get a list of them, and `docker rmi image-ID` to remove individual images.
* To auto-remove a container after exiting, you can use `docker run --rm`.
* A detailed tutorial about these and further ways can be found here: [https://www.tecmint.com/remove-docker-images-containers-and-volumes/](https://www.tecmint.com/remove-docker-images-containers-and-volumes/)

4. Q: I would like to customize the workflow settings but there are so many parameters there. What can I do?

GraphClust2 workflow is collection of more than 15 tools which most of them can be slightly complex even on its own. We have provided the pre-configurations that we think would be needed by the users accroding to our own experience and the feedback from the GraphClust2 users and collaborators. 
Each tool wrapper is also supplemented with brief help descriptions for the arguments and/or external links to the tool's documentation. We are trying to extend the in-Galaxy help descriptions and Galaxy tutorials. The user's feedback is very appreciated. If you would like to customize the configurations and do not know how to start, we would recommend to start with adapting the first and last steps of the workflow. 

GraphClust2 takes a windowing approach for folding and clustering long input sequences. The windows size and overlapping ratio can be adapted to the user's expectation of the structure features. Starting with shorter  window-length (50-100nt) would be a good idea, if you are not sure that the structured element you are searching for is covering entire sequence or not. In this way the small elements like stem-loops should be identified, afterwards you may re-start by increasing the windows size to capture the complete structure.

In the last step `cluster_collection_report`, GraphClust2 assigns the elements to the best matching cluster and also aligns the best (top) matching entries of each cluster. `results_top_num` defines how many of the top entries to align, increasing the number would be a good idea to find covariations and identify a reliable conserved element. Usually aligning the top10-30 or higher would help to identify reliable structure conservations and covariations. The other parameter to consider is the covariance model hit criteria (E-value or bitscore). The E-value works very well (and designed for )specially for structured non-coding RNAs with defined boundaries, like sequences in the Rfam database.  We have found switching back to the CM-bit score option (option `Use CM score for cutoff`), to work better for identifying structured elements surrounded (within) a sequence context.
      
5. Q: The workflow runs forever on my computer. Isn't the liner run-time on of the highlighted remarks?

The apparent practical bottleneck of the workflow specially for local instances is the covariance model calibration. Specifically the `cmcalibrate` step integrated into the `cmbuild` Infernal wrapper. This calibration is necessary to compute a reliable E-value for the significance of a CM hit, but time-consuming for generating ~million bases of background sequences. 

We would suggest to use the instance on our European Galaxy server, where the cmbuild step is pre-configured to use multi-processors and also the server is supported by thousands of computing nodes. In the docker instance, by default, the calibration is performed on a single core. We would recommend to use ask your galaxy admin to configure the wrapper according to the backend hardware. Alternatively, you can reduce the length of random sequences (-L in cmbuild-cmcalibrate) wrapper. Please refer to the Infernal manual and also take care that the E-values might not be reliable anymore.  

# Registration and Login: 
To have distinct history and workflows the Galaxy server requires each user to register for first access time. **By default anyone with access to the host network can register. No registration confirmation email will be sent to the given email.** So you can register with any custom (including non-existent) email address. There exist also a default Admin user [described here](https://bgruening.github.io/docker-galaxy-stable/users-passwords.html).  To change the default authorization settings please refer to the Galaxy Wiki section [Authentication](https://wiki.galaxyproject.org/Develop/Authentication) 

* To register (first time only):
    * On top right of the panel goto **User→Register**
    * Provide a custom email address and password, confirm your password and enter a public name

* To login:
    * On top right of the panel goto **User→Login**
    * Provide your registered email address and password


3. Q: How can I do more rounds?

   A: To extend an existing workflow of GraphClust and add another round, you should run a workflow called Galaxy-Workflow-single_round_for_extension : [GraphClust_two](https://raw.githubusercontent.com/BackofenLab/docker-galaxy-graphclust/master/workflows/Galaxy-Workflow-single_round_for_extension.ga)
The inputs for this workflow are the files generated by the GraphClust workflow. The names of each input corresponds to the name of the produced  file, so you should just choose from a dropdown selection a needed file. Important parameter for this workflow is the **round number**, which must be specified in **NSPDK_cancidateCluster**, **pgma_graphclust** and **cluster_collection_report** tools. 


