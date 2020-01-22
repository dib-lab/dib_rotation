In the [previous lesson](08_bin_completion_with_spacegraphcats.md), we observed that querying our metagenome with a *de novo* assembled genome returned a neighborhood XX% larger than the query.
Now we will assemble our query neighborhood and determine whether it contains additional amino acid sequences that were not in our query.

## But wasn't assembly a problem?

Yes! As we discussed last lesson, *de novo* assembly and binning are often part of the problem -- 
assemblers don't pick a path when they're faced with too many options, and output small, fragmented contigs instead.
Look at the graphic below. 
It depicts some common structures in cDBGs that can lead to breaks in contigs.

![](_static/assembly_unknown.png)

A lot of variation that occurs in sequences occurs at the *nucleotide* level. 
This is in part attributable to [third base pair wobble](https://www.tandfonline.com/doi/full/10.1080/15476286.2017.1356562),
which leads to [silent variation in nucleotide sequences](https://www.nature.com/articles/s41592-019-0437-4) that confounds nucleotide assembly.
One way to circumvent assembly problems that arise from sequence variation is to assemble in amino acid space.
Amino acid assemblers translate nucleotide reads into amino acid space, and then find overlaps between the translated amino acid sequences to assemble open reading frames.
In the context of metagenomes, this results in many more assembled open reading frames that can then be analyzed for their functional potential.

We will use the [PLASS](https://www.nature.com/articles/s41592-019-0437-4) amino acid assembler to assemble our query neighborhood. 
Then, we will compare the proteins we assembled with PLASS to those in the original query. 

## Running PLASS and formatting the output

First, start an srun session

```
srun -p bmh -J plass -t 24:00:00 --mem=8gb -c 1 --pty bash
```

Then, we can install PLASS into our `dib_rotation` environment.

```
conda activate dib_rotation
conda install plass
```
Now we can run PLASS!

```
cd ~/2020_rotation_project
mkdir -p plass
cd plass
ln -s SRR1976948_k31_r1_search_oh0/*.reads.fa.gz .
plass assemble *.reads.fa.gz query_nbhd_plass.fa
```

When PLASS finishes, we have to do quite a bit of formatting. 

First, PLASS adds `*` to the end of each amino acid sequence to indicate stop codons.
Most tools don't recognize this as a valid amino acid encoding, so we have to remove this character.
We'll download a script and then run it to remove this stop codon.

```
wget https://raw.githubusercontent.com/spacegraphcats/2018-paper-spacegraphcats/master/pipeline-base/scripts/remove-stop-plass.py
remove-stop-plass.py query_nbhd_plass.fa
```

Next, PLASS also outputs identical amino acid sequences when the underlying nucleotide sequences that led to the amino acid sequences are different.
These are redundant and we don't need them, so we can remove them using a tool called CD-HIT.
CD-HIT clusters sequences at a user-specified identity, and selects a representative sequence for each cluster.
In our case, we can cluster at 100% identity and that will reduce the number of amino acid sequences in our final output file.

First, install CD-HIT. Make sure you're in your `dib_rotation` environment.
If you're not, run `conda activate dib_rotation`.

```
conda install cdhit
```

Then run CD-HIT

```
cd-hit -c 1 -i  query_nbhd_plass.fa.nostop.fa -o  query_nbhd_plass.cdhit.fa
```

PLASS outputs sequences with unique identifiers, but they're not unique before the first space that occurs in the header.
Many programs truncate amino acid (or any fasta sequence names) at the first space, so we need to make the headers unique before the first space occurs. 

```
wget https://raw.githubusercontent.com/dib-lab/dib_rotation/master/scripts/format_plass_headers.py
format_plass_headers.py query_nbhd_plass.cdhit.fa query_nbhd_plass.clean.fa
```

## Comparing amino acid sequences in our neighborhood to those in the query

Let's compare the amino acid sequences in our neighborhood to those in the query.

First, download amino acid sequences in the query. 
Not every GenBank record has translated amino acid sequences, but because ours does, we can use them.

```
cd ~/dib_rotation/plass
wget ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/001/508/995/GCA_001508995.1_ASM150899v1/GCA_001508995.1_ASM150899v1_protein.faa.gz
```

There are many, many ways that we could compare the amino acid sequences between the two sequences. 
