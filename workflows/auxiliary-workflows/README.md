**Auxiliary workflows**
- MAF-to-FASTA: Conversion of Multiz Alignment Format (MAF) file of a locus, e.g. from UCSC's table browser, to FASTA format for identifying structurally conserved elements in orthologous regions.
- MAF-to-FASTA-Collection: Conversion of Multiz Alignment Format (MAF) files of loci, e.g. from UCSC's table browser, to FASTA format for identifying structurally conserved elements in orthologous regions in a collection of loci separately and in parallel.
- Compute-SP-reactivity: Computing RNA structure reactivities from HTS structure probing experiments SHAPE/DMS, using Bowtie-2 and StructureFold.
- Cluster-conservation-filter: Filter clustering input or output genomic coordinates according to the conservation scores PhastCons/PhyoP
- Cluster-conservation-filter_and_align: Filter clustering input or output genomic coordinates according to the conservation scores PhastCons/PhyoP, and further align and predict a conserved element of each conserved region. As input, the accordingly ordered set of fasta sequences is also required.
