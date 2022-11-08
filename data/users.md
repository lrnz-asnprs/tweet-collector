# Users Data

Laurenz add some notes here please on what has been done in the process from the fake_news_claim.json to user objects!


### Fetching Users Following Data (on HPC)
See the sbatch job output file for details on the different runs.

TRUE USERS
- Slurm Job_id=85401 Name=users_following Ended, Run time 07:31:50, COMPLETED, ExitCode 0 (DETAILS: FETCHED 0-2000 indexes)
- Slurm Job_id=85545 Name=users_following Ended, Run time 06:45:16, COMPLETED, ExitCode 0 (DETAILS: 2000-4000 indexes)
- Slurm Job_id=85560 Name=users_following Ended, Run time 03:22:31, COMPLETED, ExitCode 0 (DETAILS: FETCHED THE LAST - 4000-5000 indexes)



FAKE USERS
- Slurm Job_id=85818 Name=users_following Ended, Run time 22:28:43, CANCELLED, ExitCode 0 (DETAILS: indexes 2500 (think check file.out - 4500 - had to cancel as tile was running out and it would not finish another batch.)


#### Notes
-  5000 true users fetched with no issues encountered (runs 85401, 85545, 855560).

### Fetching Recent Tweets (on HPC)
See the sbatch job output file for details on the different runs.

TRUE USERS
- Slurm Job_id=85544 Name=recent_tweets Ended, Run time 16:30:35, CANCELLED, ExitCode 0 (DETAILS: FETCHED index 0-400 - Then got stuck with the second bulk as a thread never finished its job - worker stuck - before we added return statement.)
- Slurm Job_id=85559 Name=recent_tweets Ended, Run time 05:48:37, CANCELLED, ExitCode 0 (NOTE: Fetched indexes 400-2200 was cancelled for the last fetches as it was fetching 3200 recent tweets for all of them. We decided to lower this to 1000 to begin with. This run was fetching recent tweets from true users.)

FAKE USERS
- Slurm Job_id=85601 Name=recent_tweets Ended, Run time 01:10:02, COMPLETED, ExitCode 0 (indexes 0-1000 - Fake Users - 22-10-22)
- Slurm Job_id=85681 Name=recent_tweets Ended, Run time 06:07:00, COMPLETED, ExitCode 0 (indexes 1000-5000 Fake Users - 23-10-22)
- Slurm Job_id=85802 Name=recent_tweets Ended, Run time 22:47:16, CANCELLED, ExitCode 0 (indexes 5000-7900 - got stuck at user 2998 Thus fetching forward to index 7900 not getting the last 100 in that batch)
- Slurm Job_id=85946 Name=recent_tweets Ended, Run time 04:10:43, COMPLETED, ExitCode 0 (index 7900-9900 completed)



#### Notes
Date: 20-22 October
- Encountered several issues on the with rate limit (hitting request limit) as there were keys (the laai elevated key) that had run out of tweets - reach the monthly limit. This resulted in a thread worker never finishing and making the 
- The first 2200 users fetched (i.e., jobs 85544, 85559) we fetched with getting all recent tweets (3200). This was changed on the 22 of october to budget or fetching so that we are able to get recent tweets for all the buckets in our dataset. The reasoning here is that fetching 3200*25k = ~65m tweets (our monthly limit with all bearer_tokens and keys is 3.6M (three academic, three elevated))

