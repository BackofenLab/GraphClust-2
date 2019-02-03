**Workflow flavors**

In this directory you can find the alternative pre-configurations of GraphClust-2 as flavors tailored for different use-case scenarios.

- Preconfigured flavors of the workflow
    - The *MotifFinder* workflow flavor targets identifying a handful of local signals/motifs under the likely presence of noise and sequence context.
    - The pre-configured *main* workflows perform best for clustering and partitioning a set of RNA sequences with quasi defined structure boundary signals (e.g. ncRNAs or data from genomic screenings with tools such as CMfinder or RNAz screens). Usually up to 3 rounds of clustering, depending on the size of input and classes, would be enough to identify the homologs. 
    - For large datasets with thousands of sequences, further iterations of clustering can be helpful. The *sub-workflow* based flavors are recommended for such cases available under [extra-workflows/with-subworkflow/](./extra-workflows/with-subworkflow/)   
- Auxiliary workflows
    - The [auxiliary workflows](./auxiliary-workflows/) provide alternative ways to cluster genomic data beyond the classic FASTA input.

**Configuring the workflows**

Please proceed with the interactive tour named `GraphClust workflow step by step`, available under `Help->Interactive Tours` and also check the references.
An intuitive tutorial highlighting the use-case scenarios and the few parameters that can be adapted according to the scenarios will be provided soon here.
