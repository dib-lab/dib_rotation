Workflows, Automation, and Repeatability
===

For everything we have done so far, we have copied and pasted a lot of commands
to accomplish what we want. This works! But can also be time consuming, and is
more prone to error. We will show you next how to put all of these commands into
a shell script.

A **shell script** is a text file full of shell commands, that run just as if you're
running them interactively at the command line.

## Writing a shell script

Let's put some of our commands from the quality trimming module into one script.

We'll call it `run_qc.sh`. The `sh` at the end of the tells you that this is a bash script.

First, cd into the `2020-NSURP` directory

```
cd ~/2020-NSURP
```

Now, use `nano` to create and edit a file called `run-qc.sh` 

`nano run-qc.sh` will open the file. Now add the following text:

```
cd ~/2020-NSURP
mkdir -p quality
cd quality

ln -s ~/2020-NSURP/raw_data/*.fastq.gz ./

printf "I see $(ls -1 *.fastq.gz | wc -l) files here.\n"

for infile in *_R1.fastq.gz
  do
    name=$(basename ${infile} _R1.fastq.gz)
    fastp --in1 ${name}_R1.fastq.gz  --in2 ${name}_R2.fastq.gz   --out1 ${name}_1.trim.fastq.gz --out2 ${name}_2.trim.fastq.gz  --detect_adapter_for_pe \
      --qualified_quality_phred 4  --length_required 31 --correction --json ${name}.trim.json --html ${name}.trim.html
  done

```

This is now a shell script that you can use to execute all of those commands in *one* go, including running `fastp` on all six samples!
Exit `nano` and try it out! 

Run:
```
cd ~/2020-NSURP
bash run-qc.sh
```

### Re-running the shell script

Suppose you wanted to re-run the script. How would you do that?

Well, note that the `quality` directory is created at the top of the script, and everything is executed in that directory. So if you remove the quality directory like so,

```
rm -rf quality
```

> The `-rf` here means that you'd like to remove the whole directory "recursively" (`r`) and that you'd like file deltion to happen *without* asking for permission for each file (`f`)


You can then do:
```
bash run-qc.sh
```

### Some tricks for writing shell scripts

#### Make it executable

You can get rid of the `bash` part of the command above with
some magic:

Put
```
#! /bin/bash
```
at the top of the file, and then run

```
chmod +x ~/2020-NSURP/run-qc.sh
```

at the command line.

You can now run
```
./run-qc.sh
```
instead of `bash run-qc.sh`.

You might be thinking, ok, why is this important? Well, you can do the same with R scripts and Python scripts (but put `/usr/bin/env Rscript` or `/usr/bin/env python` at the top, instead of `/bin/bash`). This basically annotates the script with the language it's written in, so you don't have to know or remember yourself.

So: it's not necessary but it's a nice trick.

You can also always *force* a script to be run in a particular language by specifying `bash <scriptname>` or `Rscript <Scriptname>`, too.

## Automation with Workflow Systems!

Automation via shell script is wonderful, but there are a few problems here.

First, you have to run the entire workflow each time and it recomputes everything every time.
If you're running a workflow that takes 4 days, and you change a command at the end, you'll have to manually go in and just run the stuff that depends on the changed command.

Second, it's very _explicit_ and not very _generalizable_. 
If you want to run it on a different dataset, you're going to have to change a lot of commands.

You can read more about using workflow systems to streamline data-intensive biology in our preprint [here](https://www.biorxiv.org/content/10.1101/2020.06.30.178673v1).

## Snakemake

Snakemake is one of several workflow systems that help solve these problems. 

If you want to learn snakemake, we recommend working through a tutorial, such as the one [here](https://hackmd.io/7k6JKE07Q4aCgyNmKQJ8Iw?view). It's also worth checking out the snakemake documentation [here](https://snakemake.readthedocs.io/en/stable/).

Here, we'll demo how to run the same steps above, but in Snakemake.

First, let's install snakemake in our conda environment:
```
conda install -y snakemake-minimal
```

We're going to automate the same set of commands for trimming, but in snakemake.

Open a file called `Snakefile` using `nano`:

```
nano Snakefile
```

Here is the command we would need for a single sample, `CSM7KOJE`
```
rule all:
    input:
        "quality/CSM7KOJE_1.trim.fastq.gz",
        "quality/CSM7KOJE_2.trim.fastq.gz"

rule trim_reads:
    input:
        in1="raw_data/CSM7KOJE_R1.fastq.gz",
        in2="raw_data/CSM7KOJE_R2.fastq.gz",
    output:
        out1="quality/CSM7KOJE_1.trim.fastq.gz",
        out2="quality/CSM7KOJE_2.trim.fastq.gz",
        json="quality/CSM7KOJE.fastp.json",
        html="quality/CSM7KOJE.fastp.html"
    shell:
        """
        fastp --in1 {input.in1}  --in2 {input.in2}  \
        --out1 {output.out1} --out2 {output.out2}  \
        --detect_adapter_for_pe  --qualified_quality_phred 4 \
        --length_required 31 --correction \
        --json {output.json} --html {output.html}
        """
```

We can run it like this:
```
cd ~/2020-NSURP
snakemake -n
```
> the `-n` tells snakemake to run a "dry run" - that is, just check that the input files exist and all files specified in rule `all` can be created from the rules provided within the Snakefile).

you should see "Nothing to be done."

That's because the trimmed files already exist!

Let's fix that:

```
rm quality/CSM7KOJE*.trim.fastq.gz
```

and now, when you run `snakemake`, you should see the fastp being run. Yay w00t! Then if you run `snakemake` again, you will see that it doesn't need to do anything - all the files are "up to date".


### Running all files at once

Snakemake wouldn't be very useful if it could only trim one file at a time, so let's modify the Snakefile to run more files at once:

```
SAMPLES = ["CSM7KOJE", "CSM7KOJ0"]
rule all:
    input:
        expand("quality/{sample}_1.trim.fastq.gz", sample=SAMPLES)
        expand("quality/{sample}_2.trim.fastq.gz", sample=SAMPLES)

rule trim_reads:
    input:
        in1="raw_data/{sample}_R1.fastq.gz",
        in2="raw_data/{sample}_R2.fastq.gz",
    output:
        out1="quality/{sample}_1.trim.fastq.gz",
        out2="quality/{sample}_2.trim.fastq.gz",
        json="quality/{sample}.fastp.json",
        html="quality/{sample}.fastp.html"
    shell:
        """
        fastp --in1 {input.in1}  --in2 {input.in2}  \
        --out1 {output.out1} --out2 {output.out2}  \
        --detect_adapter_for_pe  --qualified_quality_phred 4 \
        --length_required 31 --correction \
        --json {output.json} --html {output.html}
        """
```
Try another dryrun:
```
snakemake -n
```

Now actually run the workflow:
```
snakemake -j 1
```
> the `-j 1` tells snakemake to run a single job at a time. You can increase this number if you have access to more cpu (e.g. you're in an `srun` session where you asked for more cpu with the `-n` parameter).

Again, we see there's nothing to be done - the files exist! 
Try removing the quality trimmed files and running again.

```
rm quality/*.trim.fastq.gz
```

### Adding an environment

We've been using a conda environment throughout our modules. 
We can export the installed package names to a file that we can use to re-install all packages in a single step (like on a different computer). 
```
conda env export -n nsurp-env -f ~/2020-NSURP/nsurp-environment.yaml
```

We can use this environment in our snakemake rule as well!

```
SAMPLES = ["CSM7KOJE", "CSM7KOJ0"]

rule all:
    input:
        expand("quality/{sample}_1.trim.fastq.gz", sample=SAMPLES)
        expand("quality/{sample}_2.trim.fastq.gz", sample=SAMPLES)

rule trim_reads:
    input:
        in1="raw_data/{sample}_R1.fastq.gz",
        in2="raw_data/{sample}_R2.fastq.gz",
    output:
        out1="quality/{sample}_1.trim.fastq.gz",
        out2="quality/{sample}_2.trim.fastq.gz",
        json="quality/{sample}.fastp.json",
        html="quality/{sample}.fastp.html"
    conda: "nsurp-environment.yaml"
    shell:
        """
        fastp --in1 {input.in1}  --in2 {input.in2}  \
        --out1 {output.out1} --out2 {output.out2}  \
        --detect_adapter_for_pe  --qualified_quality_phred 4 \
        --length_required 31 --correction \
        --json {output.json} --html {output.html}
        """
```

Here, we just have a single environment, so it was pretty easy to just run the Snakefile while within our `nsurp-env` environment. Using conda environment with snakemake becomes more useful as you use more tools, because it helps to keep different tools (which likely have different software dependencies) in separate conda environments.

Run snakemake with `--use-conda` to have snakemake use the conda environment for this step.
```
snakemake -j 1 --use-conda
```


## Why Automate with Workflow Systems?

Workflow systems contain powerful infrastructure for workflow management that can coordinate runtime behavior, self-monitor progress and resource usage, and compile reports documenting the results of a workow.
These features ensure that the steps for data analysis are minimally documented and repeatable from start to finish. 
When paired with proper software management, fully-contained workows are scalable, robust to software updates, and executable across platforms, meaning they will likely still execute the same set of commands with little investment by the user after weeks, months, or years.

Check out our [workflows preprint](https://www.biorxiv.org/content/10.1101/2020.06.30.178673v1) for a guide.
