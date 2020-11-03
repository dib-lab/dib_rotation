Taxonomic Discovery with Sourmash
===

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

## Workspace Setup

If you're starting a new work session on FARM, be sure to follow the instructions [here](04b_starting_a_work_session.md).
You can just do the part to enter a `tmux` session, since we'll be using a larger `srun` session than usual.


## Starting with sourmash

Sourmash doesn't have a big memory or CPU footprint, and can be run on most laptops. 
Below is a recommended `srun` command to start an interactive session in which to run the `srun` commands.

```
srun -p bmh -J sourmash24 -t 24:00:00 --mem=16gb -c 1 --pty bash
```

Let's install sourmash

```
conda activate dib_rotation
conda install -y sourmash
```

> Note: be sure you set up conda channels during the setup. If not, conda
> will not be able to find sourmash with this command. Instead, you would need
> to specify channels within the command, like so: `conda install -y -c conda-forge -c bioconda sourmash`

Next, let's create a directory in which to store our sourmash results

```
cd ~/2020_rotation_project
mkdir -p sourmash
cd sourmash
```

## What data to use?

We could run sourmash with our adapter trimmed or k-mer trimmed data.
In fact, doing so would make sourmash faster because there would be fewer k-mers in the sample.


We are currently comparing our sample against a database of trusted DNA sequences. 
If we have adapters or errors in our reads, these won't match to the assemblies in the database.
However, even though we very lightly trimmed our reads, there is a chance that we removed a very low abundance organism that was truly present in the sample. 

## Generate a sourmash signature

Next, let's make sourmash signatures from our reads. A signature is a compressed representation of the k-mers in the sequence. Using this data structure instead of the reads makes sourmash much faster.

Remember from the [Quick Insights from Sequencing Data with sourmash](https://angus.readthedocs.io/en/2019/sourmash.html) tutorial that a k-mer size of 21 is approximately specific at the genus level, a 31 is at the species level, and 51 at the strain level. We will calculate our signature with all three k-mer sizes so we can choose which one we want to use later.

```
sourmash compute -o SRR1976948.sig --name SRR1976948 --scaled 2000 -k 21,31,51 --track-abundance ~/2020_rotation_project/raw_data/SRR1976948_*fastq.gz
```

You should see output that looks like this:

```
== This is sourmash version 3.5.0. ==
== Please cite Brown and Irber (2016), doi:10.21105/joss.00027. ==

setting num_hashes to 0 because --scaled is set
computing signatures for files: /home/ntpierce/2020_rotation_project/trim/SRR1976948_1.trim.fastq.gz,
 /home/ntpierce/2020_rotation_project/trim/SRR1976948_2.trim.fastq.gz
Computing signature for ksizes: [21, 31, 51]
Computing only nucleotide (and not protein) signatures.
Computing a total of 3 signature(s).
Tracking abundance of input k-mers.
... reading sequences from /home/ntpierce/2020_rotation_project/trim/SRR1976948_1.trim.fastq.gz
... /home/ntpierce/2020_rotation_project/trim/SRR1976948_1.trim.fastq.gz 14852158 sequences
... reading sequences from /home/ntpierce/2020_rotation_project/trim/SRR1976948_2.trim.fastq.gz
... /home/ntpierce/2020_rotation_project/trim/SRR1976948_2.trim.fastq.gz 14852158 sequences
calculated 1 signatures for 29704316 sequences taken from 2 files
saved signature(s) to SRR1976948.sig. Note: signature license is CC0.
```


The outputs file, `SRR1976948.sig` holds a representative subset of k-mers from our original sample, as well as their abundance information. 
The k-mers are "hashed", or transformed, into numbers to make selecting, storing, and looking up the k-mers more efficient.

## Sourmash gather

`sourmash gather` is a method for estimating the taxonomic composition of known sequences in a       metagenome.

Please go read through the sourmash documentation on [Breaking down metagenomic samples with gather  and lca](https://sourmash.readthedocs.io/en/latest/classifying-signatures.html#).
Check out Appendix A and B in this documentation for a good overview of how sourmash gather works.

`sourmash gather` gives strain-level specificity to matches in its output -- e.g. all strains that match any sequences (above a threshold) in your metagenome will be reported, along with the percent of each strain that matches. 
This is useful both to estimate the amount of your metagenome that is known, and to estimate the closest strain relative to the thing that is in your metagenome. 

Download the database:

```
mkdir -p ~/2020_rotation_project/databases/
cd ~/2020_rotation_project/databases/
curl -L https://osf.io/jgu93/download -o genbank-k31.sbt.zip
cd ~/2020_rotation_project/sourmash
```

### Run sourmash gather

First, let's run a quick search:

```
sourmash gather --num-results 10 SRR1976948.sig ~/2020_rotation_project/databases/genbank-k31.sbt.zip
```

> - the `--num-results 10` is a way of shortening the search. In this case, we ask for only the top  10 results
> By running `sourmash gather --help`, you can see all the options for the `gather` program.

Our sample is quite large, so the shortened search will still take a while.
We see an output that looks like this:

```
== This is sourmash version 3.5.0. ==
== Please cite Brown and Irber (2016), doi:10.21105/joss.00027. ==

selecting default query k=31.
loaded query: SRR1976948... (k=31, DNA)
loaded 1 databases.


overlap     p_query p_match avg_abund
---------   ------- ------- ---------
2.6 Mbp        0.8%   97.4%      18.6    LGHF01000260.1 Methanomicrobiales arc...
2.3 Mbp       13.9%   99.6%     383.6    LGFT01000012.1 Methanosaeta harundina...
2.3 Mbp        9.3%   99.9%     261.0    LGFZ01000006.1 Desulfotomaculum sp. 4...
2.3 Mbp        3.0%   99.8%      84.5    LGGX01000001.1 Candidate division TA0...
2.2 Mbp        0.3%   99.1%       8.7    LGFV01000060.1 Actinobacteria bacteri...
2.2 Mbp        0.5%   99.7%      13.3    LGGL01000207.1 Methanobacterium sp. 4...
2.2 Mbp        2.1%   97.5%      63.9    LGGF01000001.1 Desulfotomaculum sp. 4...
2.1 Mbp        0.2%   99.5%       6.4    LGGC01000327.1 Bacteroidetes bacteriu...
1.9 Mbp        1.1%   99.6%      36.0    LGGY01000264.1 Marinimicrobia bacteri...
1.9 Mbp        0.3%  100.0%      10.0    LGGM01000054.1 Clostridiales bacteriu...

found 10 matches total;
(truncated gather because --num-results=10)
the recovered matches hit 31.5% of the query
```

The two columns to pay attention to are `p_query` and `p_match`.
`p_query` is the percent of the metagenome sample that is
(estimated to be) from the named organism. `p_match` is the percent
of the database match that is found in the query.
These metrics` are affected by both evolutionary distance and by low coverage of the
organism's gene set (low sequencing coverage, or little expression).

These percentages are quite high in the `p_match` column...that's because the authors who originally analyzed this sample deposited metagenome-assembled genomes from this sample into GenBank. 

Now, let's run the full `gather` analysis:
This will take quite a while to run.
Since you're running this in a `tmux` session, you can close the session with `Ctrl-b, d` and later reopen it with `tmux attach` if you need to do some other things while it runs.

```
sourmash gather -o SRR1976948_x_genbank-k31.gather.csv SRR1976948.sig ~/2020_rotation_project/databases/genbank-k31.sbt.zip
```

>  `-o SRR1976948_x_genbank-k31.gather.csv` tells sourmash to output a csv with all the results (in addition to the standard printout).
> This csv can be used later to visualize our results.

When sourmash is finished running, it tells us that 94% of our sequence was unclassified; i.e. it doesn't match any sequence in the database.
This is common for metagenomics, particularly for samples that are sequenced from rare environments (like Alaskan oil reservoirs).

In the next lesson, we will work to improve the percent of sequence in the metagenome that is classifiable.

## Other Methods for Taxonomic Discovery and Classification

There are many tools, such as Kraken and Kaiju, that can do taxonomic classification of individual reads from metagenomes.
These seem to perform well (albeit with high false positive rates) in situations where you don’t necessarily have the genome sequences that are in the metagenome.
Sourmash, by contrast, can estimate which known genomes are actually present, so that you can extract them and map/align to them.
It seems to have a very low false positive rate and is quite sensitive to strains.

## Detecting contamination or incorrect data

sourmash `gather` taxonomic discovery can help uncover contamination or errors in your sequencing samples.
We recommend doing sourmash gather immediately after receiving your data from the sequencing facility.
If your environmental metagenome has a tremendous amount of mouse sequence in it... maybe the sequencing facility sent you the wrong data?

## Challenges: sourmash gather (optional)

### Gather with trimmed data

Above, we ran `sourmash gather` on our untrimmed data.
A large % of the sample did not contain sequence in any GenBank assembly.
A substantial proportion of this sequence could be due to k-mers with errors.
Run `sourmash gather` again on the adapter/ k-mer trimmed data.
How much less of the sequence is unclassifiable when the errors and adapters are removed?
How many species are no longer detected after k-mer and error trimming?

### Gather at different ksizes

The genbank reference databases for signatures of ksize k=21 and k=51 are available for download.

k=21
```
cd ~/2020_rotation_project/databases/
curl -L https://osf.io/dm7n4/download -o genbank-k21.sbt.zip
```

k=51
```
cd ~/2020_rotation_project/databases/
curl -L https://osf.io/2uvsc/download -o genbank-k51.sbt.zip
```

How do you expect the gather results to differ for each? Why?
You can run these with `--num-results 10` to save time.

### Explore Gather parameters

By running `sourmash gather --help`, you can see all the options for the `gather` program.

#### scaled

The `scaled` option provides a chaces to downample the query to the specified scaled factor.

```
  --scaled FLOAT        downsample query to the specified scaled factor
```

Try running gather with a `scaled` value of 50000. How do the results change, and why?

#### base pair threshold for matches

The `threshold-bp` option lets you only find matches that have at least this many base pairs in common (default 50,000 bp)

Increasing the threshold makes gather quicker (at the expense of losing some of the smaller matches):```
--threshold-bp 10000000
```
What happens if you run gather with the threshold above?

Decreasing the threshold will take more time, but be more thorough. A threshold of 0bp does an exhaustive search for all matches

```
--threshold-bp 0
```

The full gather took quite a long time on our samples, so there's no need to run this one!
But do keep it in mind as a way to make sure we get absolutely **all** of the matches we can get using gather.
