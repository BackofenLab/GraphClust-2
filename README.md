[![DOI](https://zenodo.org/badge/76652676.svg)](https://zenodo.org/badge/latestdoi/76652676)
[![Build Status](https://travis-ci.org/BackofenLab/docker-galaxy-graphclust.svg?branch=master)](https://travis-ci.org/BackofenLab/docker-galaxy-graphclust)
[![Docker Repository on Quay](https://quay.io/repository/bgruening/galaxy-graphclust/status "Docker Repository on Quay")](https://quay.io/repository/bgruening/galaxy-graphclust)

Galaxy-GraphClust
========================
Galaxy-GraphClust is a workflow for structural clustering of RNA secondary structures developed as an extension of GraphClust clustering pipeline inside the Galaxy framework. It consists of a set of integrated Galaxy tools and different flavors of clustering workflows built upon these tools.

:whale: Galaxy-GraphClust Docker Image
========================
This Docker image is a flavor of [Galaxy Docker image](https://github.com/bgruening/docker-galaxy-stable) customized by integrating Galaxy-GraphClust tools and workflows.


# Installation and Setup:
## Requirements:

 - [Docker](https://docs.docker.com/installation/)
   A Docker client with the necessary user permissions is required for running the Galaxy GraphClust. Docker supports the three major desktop operating systems  Linux, Windows and Mac OSX. Please refer to Docker [installation guideline](https://docs.docker.com/installation/) for details.

- For Windows and Mac systems it is additinally possible to use [Kitematic](https://kitematic.com/) and launch Galaxy GraphClust Flavor from the OS graphical user interface.

- Alternative to launch the docker, having access to a Galaxy instance server preconfigured with the set of tools included in 'graphclust.yml' would be enough to run GraphClust Galaxy pipeline. (TODO: clarify this option) (TODO: mention Freiburg galaxy server?)


## Running the Galaxy server
### From the command line (Linux/Windows/MacOS):

```
docker run -i -t -p 8080:80 backofenlab/docker-galaxy-graphclust
```

For more details about this command line or specific usage, please consult the
[`README`](https://github.com/bgruening/docker-galaxy-stable/blob/master/README.md) of the main Galaxy Docker image, on which the current image is based.

### Using Kitematic graphic interface (Windows/MacOS):
Please check this [step-by-step guide](./kitematic/kitematic.md).

# Usage - How to run Galaxy-GraphClust:

## Browser access to the server:
After running the Galaxy server, a web server is established under the host IP/URL and designated port.

* Inside your browser goto IP/URL:PORT
* Following same settings as previous step: 
    * In the **same local computer**: [http://localhost:8080/](http://localhost:8080/)
    * In **any computer with network connection to the host**: [http://HOSTIP:8080/]()
    
## Registration and Login: 
To have distinct history and workflows the Galaxy server requires each user to register for first access time. **By default anyone with access to the host network can register. No registration confirmation email will be sent to the given email.** So you can register with any custom (including non-existent) email address. To change the default authorization settings please refer to Galaxy Wiki [Authentication section](https://wiki.galaxyproject.org/Develop/Authentication) 

* To register (first time only):
    * On top right of the panel goto **User→Register**
    * Provide a custom email address and password, confirm your password and enter a public name

* To login:
    * On top right of the panel goto **User→Login**
    * Provide your registered email address and password

## Help
### Interactive tours
Interactive Tours are available for Galaxy and Galaxy-GraphClust. To run the tours please on top panel go to **Help→Interactive Tours** and click on one of the tours prefixed **GraphClust workflow**. You can check the other tours for a more general introduction to the Galaxy interface.


### Step-by-step guide to cluster a sample input data
todo

### Customize workflow steps
todo

### GraphClust pipeline overview
#### Graphical workflow editor
todo

# Contributors

 - [Milad Miladi](https://github.com/mmiladi/)
 - [Eteri Sokhoyan](https://github.com/eteriSokhoyan)
 - [Bjoern Gruening](https://github.com/bgruening/)


# Support & Bug Reports

You can file an [github issue](https://github.com/BackofenLab/docker-galaxy-graphclust/issues) or ask us on the [Galaxy development list](http://lists.bx.psu.edu/listinfo/galaxy-dev).
