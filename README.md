[![DOI](https://zenodo.org/badge/76652676.svg)](https://zenodo.org/badge/latestdoi/76652676)
[![Build Status](https://travis-ci.org/BackofenLab/docker-galaxy-graphclust.svg?branch=master)](https://travis-ci.org/BackofenLab/docker-galaxy-graphclust)
[![Docker Repository on Quay](https://quay.io/repository/bgruening/galaxy-graphclust/status "Docker Repository on Quay")](https://quay.io/repository/bgruening/galaxy-graphclust)

Galaxy GraphClust Flavor
========================

:whale: Galaxy Docker repository for GraphClust

# Requirements:

 - [Docker](https://docs.docker.com/installation/)
   A Docker client with the necessary user permissions is required for running the Galaxy GraphClust. Docker supports the three major desktop operating systems  Linux, Windows and Mac OSX. Please refer to Docker [installation guideline](https://docs.docker.com/installation/) for details.

- For Windows and Mac systems it is additinally possible to use [Kitematic](https://kitematic.com/) and launch Galaxy GraphClust Flavor from the OS graphical user interface.

- Alternative to launch the docker, having access to a Galaxy instance server preconfigured with the set of tools included in 'graphclust.yml' would be enough to run GraphClust Galaxy pipeline. (TODO: clarify this option) (TODO: mention Freiburg galaxy server?)

# Setup:

## From the command line (Linux/Windows/MacOS):

```
docker run -i -t -p 8080:80 backofenlab/docker-galaxy-graphclust
```

For more details about this command line or specific usage, please consult the
[`README`](https://github.com/bgruening/docker-galaxy-stable/blob/master/README.md) of the main Galaxy Docker image, on which the current image is based.

## Using Kitematic graphic interface (Windows/MacOS):
See [here below](#setup-using-kitematic-graphic-interfacewindowsmacos-setup-kitematic).

# Usage:

## To launch the Galaxy GraphClust pipeline:

### From command line:
* Inside your browser goto [http://localhost:8080/](http://localhost:8080/)



# Contributors

 - Milad Miladi
 - Eteri Sokhoyan
 - Bjoern Gruening

# Support & Bug Reports

You can file an [github issue](https://github.com/BackofenLab/docker-galaxy-graphclust/issues) or ask us on the [Galaxy development list](http://lists.bx.psu.edu/listinfo/galaxy-dev).
