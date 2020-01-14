Until now, we've performed general pre-processing steps on our sequencing data;
sequence quality analysis and trimming usually occur at the start of any sequencing data analysis pipeline.
Now we will begin performing analysis that makes sense for metagenomic sequencing data. 

We are working with a sample from an Alaskan Oil Reservoir named SB1. 
We know from reading the [Hu et al. paper](https://mbio.asm.org/content/7/1/e01669-15) that this sample contains bacteria and archaea. 
However, let's pretend that this is a brand new sample that we just got back from our sequencing core. 
One of the first things we often want to do wtih new metagenome sequencing samples is figure out their approximate species composition. 
This allows us to tap in to all of the information known about these species and relate our community to existing literature. 

We can determine the approximate composition of our sample using `sourmash`. 

## Introduction to sourmash

Please read [this tutorial](https://angus.readthedocs.io/en/2019/sourmash.html) for an introduction to how sourmash works. 

tl;dr (but actually please read it): sourmash breaks nucleotide sequences down into small pieces.
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
conda install -y -c conda-forge -c bioconda sourmash
```

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
sourmash compute -o SRR1976948.sig --merge SRR1976948 --scaled 2000 -k 21,31,51 --track-abundance SRR1976948_*fastq.gz
```

The outputs file, `SRR1976948.sig` holds a representative subset of k-mers from our original sample, as well as their abundance information. 
The k-mers are "hashed", or transformed, into numbers to make selecting, storing, and looking up the k-mers more efficient.

## Sourmash XXX gather


## Final Thoughts

There are many tools like Kraken and Kaiju that can do taxonomic classification of individual reads from metagenomes; 
these seem to perform well (albeit with high false positive rates) in situations where you don’t necessarily have the genome sequences that are in the metagenome. 
Sourmash, by contrast, can estimate which known genomes are actually present, so that you can extract them and map/align to them. 
It seems to have a very low false positive rate and is quite sensitive to strains.
