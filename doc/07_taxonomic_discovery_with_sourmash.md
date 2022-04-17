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
srun -p bmh -J sourmash24 -t 24:00:00 --mem=16gb -c 1 --pty bash
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
ln -s ~/2020_rotation_project/raw_data/*fastq.gz .
```

We need to generate a signature using sourmash. 
A signature is a compressed representation of the k-mers in the sequence.
Using this data structure instead of the reads makes sourmash much faster.

```
sourmash sketch -o SRR1976948.sig --name SRR1976948 -p scaled=2000,k=21,k=31,k=51,abund SRR1976948_*fastq.gz
```

The outputs file, `SRR1976948.sig` holds a representative subset of k-mers from our original sample, as well as their abundance information. 
The k-mers are "hashed", or transformed, into numbers to make selecting, storing, and looking up the k-mers more efficient.

## Sourmash gather

Sourmash provides several methods for estimating the composition of known sequences in a metagenome. `sourmash gather` is the primary technique ([ref](https://www.biorxiv.org/content/10.1101/2022.01.11.475838)) -
it gives strain-level specificity to matches in its output -- e.g. all strains that match any sequences (above a threshold) in your metagenome will be reported, along with the percent of each strain that matches. 
This is useful both to estimate the amount of your metagenome that is known, and to estimate the closest strain relative to the thing that is in your metagenome. 

Download and unzip the sourmash database:

```
curl -L https://osf.io/4f8n3/download -o genbank-k31.lca.json.gz
gunzip genbank-k31.lca.json.gz
```

And then run `gather`

```
sourmash gather -o SRR1976948_gather.csv SRR1976948.sig genbank-k31.lca.json
```

We see an output that looks like this:

```
== This is sourmash version 3.0.1. ==
== Please cite Brown and Irber (2016), doi:10.21105/joss.00027. ==

loaded 1 LCA databases. ksize=31, scaled=10000
selecting specified query k=31
loaded query: SRR1976948... (k=31)

overlap     p_query p_match
---------   ------- --------
2.5 Mbp       0.2%   96.9%      unassigned Methanomicrobiales archaeon 53_19
2.4 Mbp       0.2%   99.2%      Methanobacterium sp. 42_16
2.3 Mbp       0.2%  100.0%      Desulfotomaculum sp. 46_80
2.3 Mbp       0.2%  100.0%      unassigned Actinobacteria bacterium 66_15
2.1 Mbp       0.2%   97.7%      Desulfotomaculum sp. 46_296
2.1 Mbp       0.2%   99.0%      Methanosaeta harundinacea
2.0 Mbp       0.2%   99.0%      unassigned Marinimicrobia bacterium 46_43
1.9 Mbp       0.2%  100.0%      unassigned Bacteroidetes bacterium 38_7
1.9 Mbp       0.2%   55.1%      unassigned Thermotogales bacterium EBM-48
```

The first column estimates the amount of sequences in our metagenome that are contained in the match, while the second column estimates the amount of the match that is contained within our metagenome.
These percentages are quite high in the `p_match` column...that's because the authors who originally analyzed this sample deposited metagenome-assembled genomes from this sample into GenBank. 

When sourmash is finished running, it tells us that 94% of our sequence was unclassified; i.e. it doesn't match any sequence in the database.
This is common for metagenomics, particularly for samples that are sequenced from rare environments (like Alaskan oil reservoirs).

In the next lesson, we will work to improve the percent of sequence in the metagenome that is classifiable.

## Final Thoughts

There are many tools like Kraken and Kaiju that can do taxonomic classification of individual reads from metagenomes; 
these seem to perform well (albeit with high false positive rates) in situations where you don’t necessarily have the genome sequences that are in the metagenome. 
Sourmash, by contrast, can estimate which known genomes are actually present, so that you can extract them and map/align to them. 
It seems to have a very low false positive rate and is quite sensitive to strains.

## Bonus (optional) sourmash lca gather

Above, we ran `sourmash lca gather` on our untrimmed data. 
94% of the sample did not contain sequence in any GenBank assembly. 
A substantial proportion of this sequence could be due to errors.
Run `sourmash lca gather` again on your adapter and k-mer trimmed data.
How much less of the sequence is unclassifiable when the errors and adapters are removed?
How many species are no longer detected after k-mer and error trimming?
