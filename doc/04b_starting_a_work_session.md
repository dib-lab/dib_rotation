Starting a Work Session on FARM
===

Any time you log onto FARM to work on this project, follow these steps to get access to computing resources.

## 1. Enter a `tmux` session

This command creates a new `tmux` session:
```
tmux new -s dib
```
Note: *If you already created this session, and want to re-join it, use `tmux attach` instead.*

## 2. Get access to a compute node

When you log on to our `FARM` computing system, you'll be on a `login` node, which is basically a computer with very few resources. These login nodes are shared among all users on farm. 

If we run any computing on these login nodes, logging into and navigating farm will slow down for everyone else! Instead, the moment that we want to do anything substantial, we want to ask farm for a more capable comptuter. Farm uses a "job scheduler" to make sure everyone gets access to the computational resources that they need.

We can use the following command to get access to a computer that will fit our needs:
```
srun -p bmm -J dib-rotation -t 5:00:00 --mem=10G --pty bash
```

> -  `srun` uses the computer's job scheduler `SLURM` to allocate you a computer
> - `-p` specifies the job queue we want to use, and is specific to our `farm` accounts.
> - `-J dib-rotation` is the "job name" assigned to this session. It can be modified to give your session a more descriptive name, e.g. `-J download-data`
> - `-t` denotes that we want the computer for that amount of time (in this case, 3 hours).
> - `--mem` specifies the amount of memory we'd like the computer to have. Here we've asked for 10 Gigabytes (10G). 
> - `--pty bash` specified that we want the linux shell to be the `bash` shell, which is the standard shell we've been working wiht so far


Note that your home directory (the files you see) will be the same for both the login node and the computer you get access to. This is because both read and write from the same hard drives. So you can create files while in an `srun` session, and they'll still be there for you when you logout.

## 3. Activate your Conda Environment

Once you're in an `srun` session, activate your project environment to get access to the software you've installed

```
conda activate dib-rotation
```

## Leaving your tmux session

Exit tmux by `Ctrl-b`, `d`

## Reattaching to your tmux session


```
tmux attach
```

_Note: if you make more than one tmux session, you can see all session names by typing `tmux ls`, and then attaching to the right one with `tmux attach -t <NAME>`_
