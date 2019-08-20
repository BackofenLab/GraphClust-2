This workflow can be used for identifying structurally conserved candidates from sequences of orthologous regions that can for example be obtained Multiz alignemnts. This is an extension of the Motif-Finder flavor where in the last step the clusters are filtered according to the structure conservation analysis metrics EvoFold, RNAz and R-scape. In the future release the conservation analysis feature is planned to be merged as an integrated part of the primary MotifFinder workflow.

## Step-by-step guide for extraction locally conserved candidates
The genomic coordinates of a locus is the basic input we need to identify locally conserved structure candidates from the ortholog genomic regions. Below is an example of one way to perform the orthology procedure. Specifically we have used this to identify NEAT1 and other lncRNA candidates. 
1. locus coordinates: In UCSC genome browser hg38 human, search for NEAT1 then click on the desired (here the longest) isoform, open details in the page and extract the coordinates. Here we get 
    * "Position: hg38 chr11:65,422,798-65,445,540 Size: 22,743 Total Exon Count: 1 Strand: +"
2. MAF blocks: Either directly download the MAF blocks from the UCSC Table browser or as a better option go through the Galaxy-UCSC interface to dump the MAF blocks into your Galaxy history:
    a) Inside Galaxy, search for UCSC and click "UCSC Main table browser"
    b) Use the settings as the screenshot below, the position from previous step is entered. Make sure `Galaxy` is selected. Click on `get output` and `Send query to Galaxy` buttons. 
    ![](./tablebrowser-neat1.png)
    c) After a few seconds a new entry should appear inside your current Galaxy history prefixed `UCSC Main on Human: multiz100way`. This contains the MAF blocks for the selected locus.
    d) Use the `MAF-FASTA` auxiliary workflow to prepare the fasta files for GC2 input. If a subset of species is desired, you can select them within the workflow step1 options. If the lncRNA is located on the negative strand use `Reverse complement the sequences` otherwise stick to the fasta file prefixed `Text transformation on`.
    e) The first sequence of the fasta file  can be used as the reference human NEAT1 transcript (NEAT1_hg38.fasta). Alternatively one can extract the sequence from the Tabled browser for example. This sequence will be used in the next step to map the relative location of candidates to the hg38 coordinates, so it's important to cover the full locus and not be an spliced one.
3. Invoking motif-finder workflow: Now we have the NEAT1 locus coordinates(step-1) and the one sequence per species fasta sequence (step-2) from genomic alignments available. The motif-finder workflow can now be applied to cluster the data and identify the candidates. We have configured the `MotifFinder-lncRNA` workflow to additionally obtain the annotated genomic tracks as also shown in the paper. We are dealing with ortholog sequences that are quite long and tend to have high sequence similarities, therefore the automatically generated genomic track that is annotated and filtered by Evofold, RNAz and R-scape can be very useful to get an intuition about the distribution of reliable candidates and reduce false discoveries.
    a) Run the `MotifFinder-lncRNA` workflow.
    b) Pass the genmoic fasta file as `1: Input data`, it is prefixed `Text transformation` and is the output of MAF-FASTA from step-2.
    c) Pass `NEAT1_hg38.fasta` as `2: Loci reference sequence`
    d) In the step `14: Align GraphClust cluster` (one before the last), optionally replace the `transcript loci bed` default value of "chr1 0 100000 gene 0 +" with "chr11 65422798 65445540 NEAT1 0 +" and take care of using whitespaces and the strand sign. This would be used to convert the relative positions of the candidates to the genomic one in the ucsc track.
    e) Run the workflow. This might take some minutes or a few hours depending on the available back-end capacity.
    f) The summarized outputs would be `filtered-alignments-metrics.tsv` and `bed-cluster-locations.bed`. The bed file can be copied as a a UCSC browser custom track for example https://genome.ucsc.edu/cgi-bin/hgCustom .  Please do not copy the first row of numbered columns.
    e) The alignments and secondary structures are available to view and download under the collections output entries `Rscape-R2R`, `structure.png` and `alignment.png`. 








