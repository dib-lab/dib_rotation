Until now, we've performed general pre-processing steps on our sequencing data;
sequence quality analysis and trimming usually occur at the start of any sequencing data analysis pipeline.
Now we will begin performing analysis that makes sense for metagenomic sequencing data. 

We are working with a sample from an Alaskan Oil Reservoir named SB1. 
We know from reading the [Hu et al. paper](https://mbio.asm.org/content/7/1/e01669-15) that this sample contains bacteria and archaea. 
However, let's pretend that this is a brand new sample that we just got back from our sequencing core. 
One of the first things we often want to do with new metagenome sequencing samples is figure out their approximate species composition. 
This allows us to tap in to all of the information known about these species and relate our community to existing literature. 

We can determine the approximate composition of our sample using `sourmash`. 

## Introduction to sourmash

Please read [this tutorial](https://angus.readthedocs.io/en/2019/sourmash.html) for an introduction to how sourmash works. 

tl;dr (but actually please read it): sourmash breaks nucleotide sequences down into small pieces, and then searches for those small pieces in databases.
This makes it really fast to make comparisons. Here, we will compare our metagenome sample against a pre-prepared database that contains all microbial sequences in GenBank

## Starting with sourmash

Sourmash doesn't have a big memory or CPU footprint, and can be run on most laptops. 
Below is a recommended `srun` command to start an interactive session in which to run the `srun` commands.

```
srun -p bmh -J sourmash24 -t 04:00:00 --mem=10gb -c 1 --pty bash
```

Let's install sourmash

```
conda activate dib_rotation
mamba install -y sourmash
```
(we actually already did this in the very beginning, but it doesn't hurt to
rerun conda installs!)

Next, let's create a directory in which to store our sourmash results

```
cd ~/2020_rotation_project
mkdir -p sourmash
cd sourmash
```

Then we can link in our raw data.
We could run sourmash with our adapter trimmed or k-mer trimmed data.
In fact, doing so would make sourmash faster because there would be fewer k-mers in the sample.
We are comparing our sample against a database of trusted DNA sequences. 
If we have adapters or errors in our reads, these won't match to the assemblies in the database.
However, even though we very lightly trimmed our reads, there is a chance that we removed a very low abundance organism that was truly present in the sample. 

```
ln -s ~/2020_rotation_project/raw_data/*fastq.gz ./
```

We need to generate a signature using sourmash. 
A signature is a compressed representation of the k-mers in the sequence.
Using this data structure instead of the reads makes sourmash much faster.

```
sourmash sketch dna -p scaled=1000,k=21,k=31,k=51,abund SRR1976948_*fastq.gz --name SRR1976948 -o SRR1976948.sig
```

> - `sourmash sketch dna` creates a signature file
> - `-p scaled=1000,k=21,k=31,k=51,abund` are the creation parameters of the signature file 
> - `SRR1976948_*fastq.gz --name SRR1976948` creates a single signature from multiple files
> - `-o SRR1976948.sig` outputs the signature to the designated name `SRR1976948.sig`

The outputs file, `SRR1976948.sig` holds a representative subset of k-mers from our original sample, as well as their abundance information.
The k-mers are "hashed", or transformed, into numbers to make selecting, storing, and looking up the k-mers more efficient.
In addition, these techniques remove the necessity to trim the raw fasta files before processing as the likelihood of finding a matching erroneous hash is statistically **extremely** unlikely.

To quickly peak at a signature file, database, or collection created by sourmash. Use:

```
sourmash sig summarize SRR1976948.sig
```

This will output:

```
== This is sourmash version 4.8.5. ==
== Please cite Brown and Irber (2016), doi:10.21105/joss.00027. ==

** loading from 'SRR1976948.sig'
path filetype: MultiIndex
location: SRR1976948.sig
is database? no
has manifest? yes
num signatures: 3
** examining manifest...
total hashes: 3007375
summary of sketches:
   1 sketches with DNA, k=21, scaled=1000, abund      838571 total hashes
   1 sketches with DNA, k=31, scaled=1000, abund      1006183 total hashes
   1 sketches with DNA, k=51, scaled=1000, abund      1162621 total hashes
```

## Sourmash gather

Sourmash provides several methods for estimating the composition of known sequences in a metagenome. `sourmash gather` is the primary technique ([ref](https://www.biorxiv.org/content/10.1101/2022.01.11.475838)) -
it gives strain-level specificity to matches in its output -- e.g. all strains that match any sequences (above a threshold) in your metagenome will be reported, along with the percent of each strain that matches. 
This is useful both to estimate the amount of your metagenome that is known, and to estimate the closest strain relative to the thing that is in your metagenome. 

Download a pre-built [sourmash database](https://sourmash.readthedocs.io/en/latest/databases.html#gtdb-r08-rs214-genomic-representatives-85k):

```
curl -JLO https://farm.cse.ucdavis.edu/~ctbrown/sourmash-db/gtdb-rs214/gtdb-rs214-reps.k31.lca.json.gz
```

And then run `gather`

```
sourmash gather SRR1976948.sig gtdb-rs214-reps.k31.lca.json.gz -o SRR1976948_gather.csv
```

> - `sourmash gather` is the taxonomic profiler of sourmash
> - `SRR1976948.sig` is the input signature file
> - `gtdb-rs214-reps.k31.lca.json` is the database we are gathering our taxonomic profile from!
> - `-o SRR1976948_gather.csv` is a csv output file with our results

We see an output that looks like this:

```
== This is sourmash version 4.8.5. ==
== Please cite Brown and Irber (2016), doi:10.21105/joss.00027. ==

selecting default query k=31.
loaded query: SRR1976948... (k=31, DNA)
--
loaded 85205 total signatures from 1 locations.
after selecting signatures compatible with search, 85205 remain.

Starting prefetch sweep across databases.
Prefetch found 245 signatures with overlap >= 50.0 kbp.
Doing gather to generate minimum metagenome cover.

overlap     p_query p_match avg_abund
---------   ------- ------- ---------
2.5 Mbp        5.3%  100.0%     157.0    GCA_003451675.1 Candidatus Atribacteria bacterium, ASM345167v1
2.5 Mbp        0.3%   99.6%       9.5    GCA_003446605.1 Anaerolineaceae bacterium, ASM344660v1
2.5 Mbp        2.1%  100.0%      64.1    GCA_003513005.1 Desulfotomaculum sp., ASM351300v1
2.5 Mbp        2.5%   99.2%      76.3    GCA_002503885.1 Methanoculleus marisnigri, ASM250388v1
2.3 Mbp        0.2%   76.6%       7.6    GCF_002752635.1 Mesotoga sp. Brook.08.105.5.1 strain=Brook.08....
2.2 Mbp        0.4%   84.9%      12.4    GCF_001316325.1 Methanobacterium formicicum JCM 10132 strain=J...
2.1 Mbp        0.1%   65.4%       4.5    GCA_002305765.1 Deltaproteobacteria bacterium UBA1386, ASM2305...
2.1 Mbp       12.4%  100.0%     448.3    GCA_001509375.1 Methanosaeta harundinacea, ASM150937v1

.
.
.

50.0 kbp       0.0%    1.4%       3.6    GCA_021372725.1 Chloroflexi bacterium, ASM2137272v1
50.0 kbp       0.0%    1.7%       1.2    GCF_004366375.1 Halanaerobium congolense strain=DSMZ 11287, AS...
50.0 kbp       0.0%    1.2%       1.4    GCF_011174675.1 Bacteroidales bacterium M08MB strain=M08MB, AS...
found less than 50.0 kbp in common. => exiting

found 135 matches total;
the recovered matches hit 49.0% of the abundance-weighted query.
the recovered matches hit 7.8% of the query k-mers (unweighted).

WARNING: final scaled was 10000, vs query scaled of 1000
```

The first column estimates the amount of sequences in our metagenome that are contained in the matching genome, while the second column estimates the amount of the match that is contained within our metagenome.
These percentages are quite high in the `p_match` column...that's because the authors who originally analyzed this sample deposited metagenome-assembled genomes from this sample into GenBank. 

When sourmash is finished running, it tells us that ~50% of our sequence was unclassified; i.e. it doesn't match any sequence in the database.
This is common for metagenomics, particularly for samples that are sequenced from rare environments (like Alaskan oil reservoirs).

## Sourmash taxonomy

A secondary technique to further analyzing the gather output and confirm our findings is the `sourmash tax` command.

Download a prepared lineage dataset:

```
curl -JLO https://farm.cse.ucdavis.edu/~ctbrown/sourmash-db/gtdb-rs214/gtdb-rs214.lineages.csv.gz
```

Run `sourmash tax` with the gather output we just made from the metagenome signature. 

```
sourmash tax metagenome -g SRR1976948_lca_gather.csv -t gtdb-rs214.lineages.csv.gz --output-format kreport
```

The third line of this output correlates to the previous gather output with ~50% of out metagenome unclassified.

```
== This is sourmash version 4.8.5. ==
== Please cite Brown and Irber (2016), doi:10.21105/joss.00027. ==

loaded 1 gather results from 'SRR1976948_lca_gather.csv'.
loaded results for 1 queries from 1 gather CSVs
Starting summarization up rank(s): strain, species, genus, family, order, class, phylum, superkingdom
31.94   2410420000      0       D               d__Bacteria
17.03   1285339999      0       D               d__Archaea
51.03   3850760000      3850760000      U               unclassified

.
.
.

```


In the next lesson, we will work to improve the percent of sequence in the metagenome that is classifiable.

## Final Thoughts

There are many tools like Kraken and Kaiju that can do taxonomic classification of individual reads from metagenomes; 
these seem to perform well (albeit with high false positive rates) in situations where you don’t necessarily have the genome sequences that are in the metagenome. 
Sourmash, by contrast, can estimate which known genomes are actually present, so that you can extract them and map/align to them. 
It seems to have a very low false positive rate and is quite sensitive to strains.

## Bonus (optional) sourmash fun

Above, we ran `sourmash gather` on our untrimmed data.
50% of the sample did not contain sequence in any GTDB assembly. 
A substantial proportion of this sequence could be due to errors.
Run `sourmash gather` again on your adapter and k-mer trimmed data.
How much less of the sequence is unclassifiable when the errors and adapters are removed?
How many species are no longer detected after k-mer and error trimming?

Also, we only used one type of database that was created with a specific set of parameters.
How does the gather output change with the database type and different parameters? Use curl, summarize, and gather to answer.
