# Users Data


Laurenz add some notes here please on what has been done in the process from the fake_news_claim.json to user objects!




### Fetching Users Following Data (on HPC)

- Slurm Job_id=85401 Name=users_following Ended, Run time 07:31:50, COMPLETED, ExitCode 0 (DETAILS: FETCHED 0-2000 indexes)
- Slurm Job_id=85545 Name=users_following Ended, Run time 06:45:16, COMPLETED, ExitCode 0 (DETAILS: 2000-4000 indexes)
- Slurm Job_id=85560 Name=users_following Ended, Run time 03:22:31, COMPLETED, ExitCode 0 (DETAIALS: FETCHED THE LAST - 4000-5000 indexes)

### Fetching Recent Tweets (on HPC)

See the sbatch job output file for details on the different runs.

- Slurm Job_id=85544 Name=recent_tweets Ended, Run time 16:30:35, CANCELLED, ExitCode 0 (DETAILS: FETCHED index 0-400 - Then got stuck with the second bulk as a thread never finished its job - worker stuck - before we added return statement.)
- Slurm Job_id=85559 Name=recent_tweets Ended, Run time 05:48:37, CANCELLED, ExitCode 0 (NOTE: Fetched indexes 400-2200 was cancelled for the last fetches as it was fetching 3200 recent tweets for all of them. We decided to lower this to 1000 to begin with)


