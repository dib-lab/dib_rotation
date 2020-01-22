In the [previous lesson](09_assembling_a_nbhd.md), we saw that our neighborhood query + PLASS assembly approach increased the number of amino acid sequences over those in our query by XX%.
What do these amino acid sequences encode? 
Are they strain variants (e.g. a few amino acids different) from those that were already in the query, or do they add new functionality?
In this lesson, we will annotate the amino acid sequences in our PLASS assembly and in the GenBank assembly, and then compare the encoded functions.

As with most things in bioinformatics, there are many ways to annotate amino acid sequences. 
We will be using `kofamscan`, a tool that uses hidden markov models built from KEGG orthologs to assign KEGG ortholog numbers to new amino acid sequences.
Hidden markov models work well for protein annotation because they weight the importance of each amino acid in determining the final assignment.
Look at the figure below.

![](_static/rpsg_logo_image.png)

This figure is a logo depicting the PFAM HMM for rpsG. 
rpsG encodes 30S ribosomal protein S7, and it is a highly conserved protein. 
The HMM was built from hundreds of rpsG protein sequences. 
At each position of the protein, the logo depicts the liklihood of seeing a specific amino acid.
The larger the amino acid is in the logo, the more likely it is to be observed at that position. 
In positions where no amino acid is visible, it is less important which amino acid occurs there.
This encoding is more flexible than something like Hamming distance or BLAST because it incorporates biological importance of amino acid positionality.
This approach works well on novel amino acid sequences that are not closely related to anything currently housed in databases.

kofamscan is a tool released by the KEGG that includes HMMs built from each KEGG ortholog. 
Using kofamscan, we can assign KEGG orthologs to our amino acid sequences. 
This allows us to take advantage of KEGG pathway information to determine if any pathways are more complete in our neighborhood than in our query.

## Running kofamscan













> **Side note - using prokka to generate amino acid sequences from nucleotide sequences**    
>
> So far, we've been using the amino acid sequences from GenBank.   
> What if we were working with a genome or bin that did not have   
> that did not have amino acid sequences associated with it yet?    
> We can generate amino acid sequences from nucleotide sequences,   
> as well as first-pass annotations, using a tool called `prokka`.  
> We can use conda to install prokka: `conda install prokka`  
> To run prokka on a bin derived from a metagenome, use:  
> ```
> prokka {input} --outdir {outdir} --prefix {bin} --metagenome --force --locustag {bin}
> ```
