from concurrent.futures import thread
import sys
import os
sys.path.append(os.getcwd())
import time
import datetime
from fake_collector.utils.TwythonConnector import TwythonConnector
from twython import TwythonRateLimitError
from fake_collector.utils.TwitterUser import TwitterUser
from typing import List
from multiprocessing import Process
from fake_collector.modules.user_profile_collector import UserProfileCollector
from fake_collector.modules.user_following_collector_v2 import UserFollowingCollectorV2
from fake_collector.modules.user_following_collector import UserFollowingCollector
from fake_collector.modules.user_recent_tweets_collector_v2 import UserLatestTweetsCollectorV2
from fake_collector.configs.directory_config import Directories
from fake_collector.utils.load_fake_true_users import load_all_true_users_df,load_all_fake_users_df, load_fake_users_by_goup_df, load_true_or_fake_df
import queue
import threading
import time
import pickle
import pandas as pd
import time

user_counter = 0
error_users = []

def add_user_recent_tweets(user_queue, app_type, recent_tweets):
    """
    Takes user queue as input, adds the corresponding following ID's to each user object, and returns the final list
    """

    print("In worker ", app_type)

    while True:
        
        try:

            user = user_queue.get()
            user_recent_tweets_collector = UserLatestTweetsCollectorV2(app_type=app_type)
            recent_tweets_user = user_recent_tweets_collector.get_user_timeline(user_id=user)
            if recent_tweets_user == -1:
                print(f"Close worker {app_type} due to rate limit")
                # put failed user back on the queue
                user_queue.put(user)
                user_queue.task_done()
                return
            recent_tweets[user] = recent_tweets.get(user) + recent_tweets_user
            user_queue.task_done()

            # Change global user counter var
            global user_counter
            user_counter += 1
            print("User done ", user)
            print("User count: ", user_counter)
        
        except:

            print("ERROR with user: ", user)
            user_queue.task_done()
            global error_users
            error_users.append(user)


# Load true or fake users
true_or_fake = "fake"

users_df = load_true_or_fake_df(users=true_or_fake)
# users_df = load_all_true_users()

# Split into batches
start_from_index = 0
users_df = users_df.iloc[start_from_index:]

max_users = 2 #2000
batch_size = 1 #500

def _batch_proccess(df, max_users, batch_size):
    for ndx in range(0, max_users, batch_size):
        yield users_df[ndx:min(ndx+batch_size,max_users)]

# Split df into batches
batches = _batch_proccess(users_df, max_users, batch_size)

# Iterate over batches
for batch in batches:    

    start = time.time()

    batch_user_ids = set(batch['user_id'])

    # Create dict for recent tweets
    recent_tweets = {user_id : [] for user_id in batch_user_ids}
    
    user_queue = queue.Queue()

    for app_type in ['laai_elevated', 'laai_academic', 'gugy_academic', 'gugy_elevated', 'luca_academic', 'luca_elevated']:
        worker = threading.Thread(target=add_user_recent_tweets, args=(user_queue, app_type, recent_tweets), daemon=True)
        worker.start()

    for user_id in recent_tweets:
        print("Adding user", user_id)
        user_queue.put(user_id)

    # Finish queue
    user_queue.join()

    print("Save user")

    # Save file in recent tweets directory
    directories = Directories()
    path = directories.USERS_PATH / f"{true_or_fake}_users"

    filename = f"{true_or_fake}_users_recent_tweets/{true_or_fake}_users_recent_tweets_{start_from_index}_to_{start_from_index+len(batch)}.pickle"

    with open(path / filename, "wb") as f:
        pickle.dump(recent_tweets, f)
    
    # Increment batch counter
    start_from_index = start_from_index + len(batch)

    # DOne
    end = time.time()
    print(f"############ Took {(end-start)/60} minutes #################")

    try:
        if len(error_users) > 0:
            with open(path / f"error_users_{start_from_index-len(batch)}_to_{start_from_index}", "w") as f:
                for item in error_users:
                    # write each item on a new line
                    f.write("%s\n" % item)
    except:
        print("Coulndt write file")


