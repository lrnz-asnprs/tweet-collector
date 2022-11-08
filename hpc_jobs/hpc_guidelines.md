# HPC guidelines

check out hpc.itu.dk for overview and details about the cluster.


### Paths and Permissions
See Calculator here https://chmod-calculator.com/
To allow group to have full read write and execute permissions run inside the directory or specify for which dir you want to run it on.

```bash
chmod -R 770 .
```

to check the current permissions for a directory:

```bash
ls -ld dir_name 
```

### Move files from Local dir to HPC

The easiest way is to use a client with an interface like FileZilla (https://filezilla-project.org/). 

These are the steps to be taken:
- Download Filezilla and install it
- Open it and click on the icon on the top left corner
- Create a "new site" and fill the form on the right with our HPC credentials, see mine here:
- Then, when you double click on a site you created, you will be connected to the HPC (remember, you need to be on VPN or at ITU). Then, a panel will open in which you can navigate the directory structure of HPC. Just drag and drop to upload or download files
- You can create a directory for your project in your home directory where you will keep all data and code and upload/download stuff at will. We have a lot of storage, but remember that HPC is not backed up, so if a lightning strikes ITU, your data will be lost. It's unlikely, but I need to tell you as a disclaimer, for full transparency :)



### Running Notebooks on the HPC

http://hpc.itu.dk/software/jupyternotebook/


### To Watch the Current Queue of Jobs

To exit the view hit "ctrl + c". Preferable to have it open in an extra window.

```bash
watch squeue 
```

### To see instance of the current queue

```bash
squeue 
```

### To Run a Job in the Queue

- Move your script_to_run.job file to the parent directory of your project.
- Make sure to make the necessary changes to the your_file.job file specifying what python script to run and other params.


```bash
sbatch your_file.job
```



### Stopping a Job that is currently running

```bash
scancel insert_job_number
```

This is used to cancel a pending or running job or job step. It can also be used to send an arbitrary signal to all processes associated with a running job or job step.

