High Performance Computing (HPC) refers to computers that have more capability than a typical personal computer 
(i.e. most desktops and laptops). 
Many research problems we encounter when analyzing sequencing data require more resources than we have available on our laptops.
For this, we use large, remote compute systems that have more resources available. 

Most univeristies have access to an HPC (or cluster) that has a large amount of hard drive space to store files, RAM for computing tasks, and CPUs for processing.
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
mkdir -p ssh
cd ssh
```

Then, generate the keyfile pair by running:
```
ssh-keygen –t rsa
```

Follow the prompts on the screen. If prompted for a password, you can hit `Enter` on your keyboard to avoid setting one.

Two files will be created by this command. 
These files should have the same prefix.
The file that ends in `.pub` is the public key.

Next, navigate to [this page](https://wiki.cse.ucdavis.edu/cgi-bin/index2.pl).
From the first drop down menu (Which cluster are you applying for an account on?), select `FARM/CAES`.
From the second drop down menu (Who is sponsoring your account?), select `Brown, C. Titus`.
Then, upload your public key file to the page. 
Submit the form. 
If the cluster admins and Titus approve your account, you will now have farm access!
Don't loose the key file pair you just made. 
You will need the private key file each time you log into farm.


## Connecting to a remote computer 
