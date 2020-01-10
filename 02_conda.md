[This tutorial](https://angus.readthedocs.io/en/2019/conda_tutorial.html) covers the basics of conda including a brief introduction to conda and why it is useful, installation and setup, creating environments, and installing software. 

These videos cover the material in the above tutorial: 
+ [video 1](https://www.youtube.com/watch?v=Ef1QwhELuMs)
+ [video 2](https://www.youtube.com/watch?v=MOlYlvBBa9c) (there were some technical issues with this recording...sorry!)

## Install miniconda

Log in to farm and run the following commands to install Miniconda. 
Follow the prompts on the screen and accept all default options. 

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

Miniconda is now installed, but we need to activate it to be able to use it.
```
source ~/.bashrc
```

You should now see `(base)` in front of your prompt, indicating that you are in the base environment.

## Configuring channels

Channels are the locations of the repositories (directories) online containing Conda packages. 
Upon Conda’s installation, Continuum’s (Conda’s developer) channels are set by default, so without any further modification, these are the locations where your Conda will start searching for packages.
We need to add other channels from which we will be installing software.

Channels in Conda are ordered. 
The channel with the highest priority is the first one that Conda checks, looking for the package you asked for. 
You can change this order, and also add channels to it (and set their priority as well).

If multiple channels contain a package, and one channel contains a newer version than the other one, the order of the channels’ determines which one of these two versions are going to be installed, even if the higher priority channel contains the older version.
```
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge
```

## Creating an environment

Now that we have conda installed and our channels configured, we are ready to create an environment.

```
conda create -y -n dib_rotation
```

This creates an empty environment named `dib_rotation`. 
To activate this environment, run:

```
conda activate dib_rotation
```

Your prompt should now start with `(dib_rotation)`.

We can now install software into our environment. 
Let's install sourmash, which we will use in a later lesson. 

```
conda install -y sourmash
```

## Deactivating and Exiting

If you would like to leave your environment, you can type `conda deactivate` and you will return to the base environment.

When you log out of farm by typing `exit`, when you end a `tmux` or `screen` session, or when an `srun` job ends, your environment will automatically be exited.
To restart the environment, you can run `conda activate dib_rotation`.
