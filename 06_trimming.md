After [downloading and QCing sequencing data](05_starting_with_data.md), the next step in many pipelines is to adapter and error trim the reads.
However, deciding when and how to trim data is pipeline dependent. 
Below, we define a few types of trimming and explore a use cases and how trimming recommendations may change with different applications.
Although this project focuses on metagenomic sequencing, we include other applications in this discussion.
## Types of trimming

+ **Adapter and barcode trimming**: Adapter sequences are added to a sample library to aid in the physical process of sequencing.
They are ubiquitous within a certain chemistry, and so are present across all sequenced samples. 
Barcodes are unique nucleotide sequences used to identify a specific sample when multiple samples are sequenced in a single lane.
+ **Quality trimming**
+ **K-mer trimming**

## When and how to trim?

Trimming is a balance of removing artificial or incorrect nucleotides and retaining true nucleotides in sequencing data. 
What to trim and when to trim therefore change with the sequencing application. 
+ **Single-species genomic sequencing for assembly**
+ **Single-species genomic sequencing for variant calling**
+ **RNA-sequencing**
+ **Metagenome taxonomic discovery from reads**
+ **Metagenome *de novo* assembly**
+ **Metagenome read mapping**
