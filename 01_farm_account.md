High Performance Computing (HPC) refers to computers that have more capability than a typical personal computer 
(i.e. most desktops and laptops). 
Many research problems we encounter when analyzing sequencing data require more resources than we have available on our laptops.
For this, we use large, remote compute systems that have more resources available. 

Most universities have access to an HPC (or cluster) that has a large amount of hard drive space to store files, RAM for computing tasks, and CPUs for processing.
Other options for accessing large computers include NSF XSEDE services like Jetstream and paid services like Amazon Web Services or Google Cloud.
We will use the UC Davis [Farm](https://wiki.cse.ucdavis.edu/support/systems/farm) Cluster during this rotation.

## Getting an account on Farm

To be able to use Farm, you need to sign up for an account. 
Farm requires key file authentication.
Key files come in pairs like the locks and keys on doors. 
The private key file is the first file, and it is like the key to a door. 
This file is private and should never be shared with anyone (do not post this file on GitHub, slack, etc.). 
The public key file is the second file, and it is like the lock on a door.
It is publicly viewable, but cannot be "unlocked" without the private key file. 

We need to generate a key file pair in order to create a farm account. 

Open the `Terminal` application or the Terminal emulator you installed in the [first_lesson](00_getting_started.md).

Change directories into the `.ssh` folder.
This folder is where key file pairs are typically stored.

```
cd ~/.ssh
```

If this command does not work, create your own `ssh` folder and `cd` into it:
```
mkdir -p ~/.ssh
cd ~/.ssh
```

Then, generate the keyfile pair by running:
```
ssh-keygen
```

Follow the prompts on the screen. If prompted for a password, you can hit `Enter` on your keyboard to avoid setting one.

Two files will be created by this command. 
These files should have the same prefix.
The file that ends in `.pub` is the public key.

### [The account request form](https://wiki.cse.ucdavis.edu/cgi-bin/index2.pl)

Next, navigate to [this page](https://wiki.cse.ucdavis.edu/cgi-bin/index2.pl).
From the first drop down menu (Which cluster are you applying for an account on?), select `FARM/CAES`.
From the second drop down menu (Who is sponsoring your account?), select `Brown, C. Titus`.
Then, upload your public key file to the page. 
Submit the form. 
If the cluster admins and Titus approve your account, you will now have farm access!
Don't loose the key file pair you just made. 
You will need the private key file each time you log into farm.


## Connecting to a remote computer 

Once you have a farm account, we will use the command `ssh` to connect to farm. 
`ssh` stands for "secure shell". 

To connect to your account on farm, type:

```
ssh -i ~/.ssh/your_keyfile_name username@farm.cse.ucdavis.edu
```

If you are successful, you will see a message that looks something like this:

```
Welcome to Ubuntu 18.04.3 LTS (GNU/Linux 4.15.0-70-generic x86_64)

1 updates could not be installed automatically. For more details,
see /var/log/unattended-upgrades/unattended-upgrades.log

*** System restart required ***
A transfer node, c11-42, is available for rsync, scp, gzip
From outside the Farm cluster use port 2022 to access the transfer node.
 ssh -p 2022 username@farm.cse.ucdavis.edu
 scp -P 2022 src username@farm.cse.ucdavis.edu:/destination

   REMINDER: Farm does not back up user data. Please ensure your data is backed up offsite.

 *** Dec 04 2019:
 * 2:10pm - Service restored. Please report any issues to help@cse.ucdavis.edu.


   Email help@cse.ucdavis.edu for help with Farm.

Downtime scheduled for the first Wednesday of Oct and April.  The next downtime is Wednesday April 1st at 11:59pm.

If interested in contributing to farm, the rates for 5 years are:
  $ 1,000 per 10TB, served from redundant servers with compression
  $ 8,800 per parallel node (256GB ram, 32 cores/64 threads, 2TB /scratch)
  $17,500 per GPU node (Nvidia Telsa V100, dual Xeon 4114, 2TB /scratch)
  $22,700 per bigmem node (1TB ram, 48 cores/96 threads, 2TB /scratch)

Last login: Thu Jan  2 17:01:36 2020 from 76.105.143.194
Module slurm/19.05.3 loaded
Module openmpi/4.0.1 loaded
username@farm:~$
```

When you first login to farm, you will be in your home directory.
This is where you will write your files and run the majority of your commands. 

When you are done using farm, you can exit your ssh connection with the `exit` command.

```
exit
```
