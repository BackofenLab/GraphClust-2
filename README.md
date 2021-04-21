<!---status GraphClust2:
* container:
[![DOI](https://zenodo.org/badge/76652676.svg)](https://zenodo.org/badge/latestdoi/76652676)
[![Build Status](https://travis-ci.org/BackofenLab/GraphClust-2.svg?branch=master)](https://travis-ci.org/BackofenLab/GraphClust-2)
[![Build Status](https://img.shields.io/docker/pulls/backofenlab/docker-galaxy-graphclust.svg)](https://hub.docker.com/r/backofenlab/docker-galaxy-graphclust)
* usegalaxy.eu: [![Build Status](https://build.galaxyproject.eu/job/usegalaxy-eu/job/workflow-testing/PYTHON=System-CPython-2.7,WORKFLOW=GraphClust2%2FGC-lite.ga/badge/icon)](https://build.galaxyproject.eu/job/usegalaxy-eu/job/workflow-testing/PYTHON=System-CPython-2.7,WORKFLOW=GraphClust2%2FGC-lite.ga/)
--->
 
GraphClust2
========================
GraphClust2 is a  workflow for scalable clustering of RNAs based on sequence and secondary structures feature. GraphClust2 is implemented within the Galaxy framework and consists a set of integrated Galaxy tools and flavors of the linear-time clustering workflow.


Table of Contents
=================
   * [GraphClust2](#graphclust2)
   * [Table of Contents](#table-of-contents)
   * [Availability](#availability)
      * [GraphClust2 on European Galaxy Server](#graphclust2-on-european-galaxy-server)
      * [GraphClust2 Docker <g-emoji class="g-emoji" alias="whale" fallback-src="https://github.githubassets.com/images/icons/emoji/unicode/1f433.png">🐳</g-emoji> Image](#graphclust2-docker-whale-image)
         * [Installation and Setup](#installation-and-setup)
            * [Requirements](#requirements)
         * [Running the docker instance](#running-the-docker-instance)
            * [Using graphic interface (Windows/MacOS)](#using-graphic-interface-windowsmacos)
      * [Installation on a Galaxy instance](#installation-on-a-galaxy-instance)
         * [Setup support](#setup-support)
      * [Demo instance](#demo-instance)
   * [Usage - How to run GraphClust2](#usage---how-to-run-graphclust2)
      * [Browser access to the server](#browser-access-to-the-server)
         * [Public server](#public-server)
         * [Docker instance](#docker-instance)
         * [Video tutorial](#video-tutorial)
         * [Interactive tours](#interactive-tours)
         * [Import additional workflows](#import-additional-workflows)
         * [Workflow flavors](#workflow-flavors)
            * [Workflows on the running server](#workflows-on-the-running-server)
      * [command line support (beta)](#command-line-support-beta)
      * [<a href="FAQ.md">Frequently Asked Questions</a>](#frequently-asked-questions)
   * [Workflow overview](#workflow-overview)
        * [Input](#input)
        * [Output](#output)
   * [Support &amp; Bug Reports](#support--bug-reports)
   * [References](#references)


# Availability 

## GraphClust2 on European Galaxy Server
GraphClust2 is accessible on European Galaxy server at:
* [https://graphclust.usegalaxy.eu](https://graphclust.usegalaxy.eu)

## GraphClust2 Docker :whale: Image 
It is also possible to run GraphClust2 as a stand-alone solution using a Docker container that is a pre-configured flavor of the official [Galaxy Docker image](https://github.com/bgruening/docker-galaxy-stable).
This Docker image is a flavor of the Galaxy Docker image customized for GraphClust2 tools, tutorial interactive tours and workflows.

### Installation and Setup
#### Requirements

For running GraphClust2 locally, the `Docker` client is required.
Docker supports the three major desktop operating systems  Linux, Windows and Mac OSX. Please refer to thw [Docker installation guideline](https://docs.docker.com/installation) for details.

A GUI client can also be used for Windows and Mac operation systems.
Please follow the graphical instructions for using Kitematic client [here](./kitematic.md).

**Hardware requirements:**
* Minimum 8GB memory
* Minimum 20GB free disk storage space, 100GB is recommended.

**Supported operating systems**

GraphClust2 has been tested on these operating systems:
* *Windows* : 10 using [Kitematic](https://kitematic.com/)
* *MacOSx*: 10.1x or higher using [Kitematic](https://kitematic.com/)
* *Linux*: Kernel 4.2 or higher, preferably with aufs support (see [FAQ](FAQ.md))


### Running the docker instance
From the command line:

```bash
docker run -i -t -p 8080:80 backofenlab/docker-galaxy-graphclust
```

For details about the docker commands please check the official guide [here](https://docs.docker.com/engine/reference/run/). Galaxy specific run options and configuration supports for computation grid systems are detailed in the Galaxy Docker [repository](https://github.com/bgruening/docker-galaxy-stable).

### Using graphic interface (Windows/MacOS)
Please check this [step-by-step guide](./kitematic/kitematic.md).

## Installation on a Galaxy instance
GraphClust2 can be integrated into any available Galaxy server. All the GraphClust2 tools and workflows needed to run the 
    GraphClust pipeline are listed in [workflows](./workflows/) and 
    [tools-list](./assets/tools/).

#### Setup support
In case you encountered problems please use the recommended settings, check the [FAQs](./FAQ.md) or contact us via [*Issues*](https://github.com/BackofenLab/GraphClust-2/issues) section of the repository.


## Demo instance
A running demo instance of GraphClust2 is available at http://192.52.32.222:8080/.
Please note that this instance is simply a Cloud instance of the provided Docker container, intended for rapid inspections and demonstration purposes. The computation 
capacity is limited and currently it is not planned to have a long-time availability. We recommend to follow instructions above. Please contact us if you prefer to keep this service available.

# Usage - How to run GraphClust2

## Browser access to the server
### Public server
Please register on our European Galaxy server [https://usegalaxy.eu](https://usegalaxy.eu) and use your authentication information to access the customized sub-domain [https://graphclust.usegalaxy.eu]. Guides and tutorial are available in the server welcome home page.

### Docker instance
After running the Galaxy docker, a web server is established under the host IP/URL and designated port (default 8080).
* Inside your browser goto IP/URL:PORT
* Following same settings as previous step
  * In the same (local) computer: [http://localhost:8080/](http://localhost:8080)
  * In other systems in the network: [http://HOSTIP:8080]()

### Video tutorial
You might find this [Youtube tutorial](https://www.youtube.com/watch?v=fJ6tUt_6uas) helpful to get a visually comprehensive introduction on setting-up and running GraphClust2. 


[![IMAGE ALT TEXT HERE](./assets/img/video-thumbnail.png)](https://www.youtube.com/watch?v=fJ6tUt_6uas)

### Interactive tours
Interactive Tours are available for Galaxy and GraphClust2. To run the tours please on top panel go to **Help→Interactive Tours** and click on one of the tours prefixed *GraphClust*. You can check the other tours for a more general introduction to the Galaxy interface.

### Import additional workflows

To import or upload additional workflow flavors (e.g. from [extra-workflows directory](./workflows/extra-workflows/)), on the top panel go to *Workflow* menu. On top right side of the screen click on "Upload or import workflow" button. You can either upload workflow from your local system or by providing the URL of the workflow. Log in is necessary to access into the workflow menu. The docker galaxy instance has a pre-configured *easy!* info that can be found by following the interactive tour. You can download workflows from the following links 

### Workflow flavors
The pre-configured flavors of GraphClust2 are provided and described inside the [workflows directory](./workflows/) 

#### Workflows on the running server
Below workflows can be directly accessed on the public server:
  * MotifFinder: [GraphClust-MotifFinder](https://graphclust.usegalaxy.eu/u/graphclust2/w/graphclust2--motiffinder)
  * Workflow main: [GraphClust_1r](https://graphclust.usegalaxy.eu/u/graphclust2/w/graphclust2--main-1r)
  * Workflow main, preconfigured for two rounds : [GraphClust_2r](https://graphclust.usegalaxy.eu/u/graphclust2/w/graphclust2--main-2r)

## command line support (beta)
Galaxy service is accessible via the Galaxy project `bioblend` API library. In the future we plan to provide a full integration of bioblend API for GraphClust2. Currently a beta support for running GraphClust2 via the CLI is available. The wrapper and setup template is available inside [CLI-workflow-executor](./CLI-workflow-executor) directory.


## [Frequently Asked Questions](FAQ.md) 

Workflow overview
===============================

The pipeline for clustering RNA sequences and structured motif discovery is a multi-step pipeline. Overall it consists of three major phases: a) sequence based pre-clustering b) encoding predicted RNA structures as graph features c) iterative fast candidate clustering then refinement

<img src="./assets/img/workflow_early.png" width="600"> ![GraphClust-2 workflow overview](./assets/img/figure-pipeline_zigzag.png) 


Below is a coarse-grained correspondence list of GraphClust2 tool names with each step:

|   Stage  | Galaxy Tool Name | Description|
| :--------------------: | :--------------- | :----------------|
|1 | [Preprocessing](https://graphclust.usegalaxy.eu/root?tool_id=toolshed.g2.bx.psu.edu/repos/rnateam/graphclust_preprocessing/preproc/0.5) | Input preprocessing (fragmentation)|
|2 | [fasta_to_gspan](https://graphclust.usegalaxy.eu/root?tool_id=toolshed.g2.bx.psu.edu/repos/rnateam/graphclust_fasta_to_gspan/gspan/0.4) | Generation of structures via RNAshapes and conversion into graphs|
|3 | [NSPDK_sparseVect](https://graphclust.usegalaxy.eu/root?tool_id=toolshed.g2.bx.psu.edu/repos/rnateam/graphclust_nspdk/nspdk_sparse/9.2.3) | Generation of graph features via NSPDK |
|4| [NSPDK_candidateClusters](https://graphclust.usegalaxy.eu/root?tool_id=toolshed.g2.bx.psu.edu/repos/rnateam/graphclust_nspdk/NSPDK_candidateClust/9.2.3) | min-hash based clustering of all feature vectors, output top dense candidate clusters|
|5| [PGMA_locarna](https://graphclust.usegalaxy.eu/?tool_id=toolshed.g2.bx.psu.edu/repos/rnateam/graphclust_prepocessing_for_mlocarna/preMloc/0.4),[locarna](https://graphclust.usegalaxy.eu/tool_runner?tool_id=toolshed.g2.bx.psu.edu/repos/rnateam/graphclust_mlocarna/locarna_best_subtree/0.4), [CMfinder](https://graphclust.usegalaxy.eu/?tool_id=toolshed.g2.bx.psu.edu/repos/rnateam/graphclust_cmfinder/cmFinder/0.4) | Locarna based clustering of each candidate cluster, all-vs-all pairwise alignments, create multiple alignments along guide tree, select best subtree, and refine alignment.|
|6| [Build covariance models](https://graphclust.usegalaxy.eu/root?tool_id=toolshed.g2.bx.psu.edu/repos/bgruening/infernal/infernal_cmbuild/1.1.0.2) |  create candidate model |
|7| [Search covariance models](https://graphclust.usegalaxy.eu/root?tool_id=toolshed.g2.bx.psu.edu/repos/bgruening/infernal/infernal_cmsearch/1.1.0.2) | Scan full input sequences with Infernal's cmsearch to find missing cluster members |
|8,9| [Report results](https://graphclust.usegalaxy.eu/?tool_id=toolshed.g2.bx.psu.edu/repos/rnateam/graphclust_postprocessing/glob_report/0.5) and [conservation evaluations](https://graphclust.usegalaxy.eu/?tool_id=toolshed.g2.bx.psu.edu/repos/rnateam%2Fgraphclust_aggregate_alignments/graphclust_aggregate_alignments/0.1) | Collect final clusters and create example alignments of top cluster members|


### Input
The input to the workflow is a set of putative RNA sequences in FASTA format. Inside the `data` directory you can find examples of the input format. The labeled datasets are based on Rfam annotation that are labeled with the associated RNA family.

### Output
The output contains the predicted clusters, where similar putative input RNA sequences form a cluster. Additionally overall status of the clusters and the matching of cluster elements is reported for each cluster. 


<!-- # Contributors

 - [Milad Miladi](https://github.com/mmiladi/)
 - [Eteri Sokhoyan](https://github.com/eteriSokhoyan)
 - [Bjoern Gruening](https://github.com/bgruening)
 -->


# Support & Bug Reports

You can file a [github issue](https://github.com/BackofenLab/GraphClust-2/issues) or find our contact information in the [lab page](http://www.bioinf.uni-freiburg.de/team.html?en).

# References
The manuscript is currently under prepration/revision. If you find this resource useful, please cite the zenodo DOI of the repo or contact us. 

* Miladi, Milad, Eteri Sokhoyan, Torsten Houwaart, Steffen Heyne, Fabrizio Costa, Bjoern Gruening, and Rolf Backofen. "GraphClust2: Annotation and discovery of structured RNAs with scalable and accessible integrative clustering." GigaScience, Volume 8, Issue 12, December 2019, giz150. doi: [https://doi.org/10.1093/gigascience/giz150](https://doi.org/10.1093/gigascience/giz150)
* Milad Miladi, Björn Grüning, & Eteri Sokhoyan. BackofenLab/GraphClust-2: Zenodo. http://doi.org/10.5281/zenodo.1135094
* GraphClust-1 methodology (S. Heyne, F. Costa, D. Rose, R. Backofen;
GraphClust: alignment-free structural clustering of local RNA secondary structures; Bioinformatics, 2012) available at http://www.bioinf.uni-freiburg.de/Software/GraphClust/

