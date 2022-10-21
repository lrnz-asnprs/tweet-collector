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
import queue
import threading
import time
import pickle
import pandas as pd
import time

user_counter = 0

def add_user_recent_tweets(user_queue, app_type, recent_tweets):
    """
    Takes user queue as input, adds the corresponding following ID's to each user object, and returns the final list
    """

    print("In worker ", app_type)

    while True:

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


# Directories add path name!
directories = Directories()
path = directories.USERS_PATH / "true_users"

# Load the user profiles
filename = "true_users.pickle"
with open(path / filename, "rb") as f:
    users_loaded = pickle.load(f)

# Just transform for saving as df
users_dict = {id : users_loaded.get(id).get_user_as_dict() for id in users_loaded.keys()}

# Load users as df
users_df = pd.DataFrame.from_dict(users_dict.values())
users_df.head()

# Add the labeled tweet count to the user df
users_df['labeled_tweet_count'] = users_df.apply(lambda x: len(users_loaded.get(x['user_id']).get_all_true_tweets_retweets()) + len(users_loaded.get(x['user_id']).get_all_false_tweets_retweets()), axis=1)
# Rank users
users_df['rank'] = users_df['labeled_tweet_count'].rank(method='dense')
users_df.sort_values(by='rank', ascending=False, inplace=True)

# Split into batches
start_from_index = 0
users_df = users_df.iloc[start_from_index:]

max_users = 100 #2000
batch_size = 100 #500

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

    # for app_type in ['laai_elevated', 'laai_academic', 'gugy_academic', 'gugy_elevated', 'luca_academic', 'luca_elevated']:
    for app_type in ['laai_academic']:
        worker = threading.Thread(target=add_user_recent_tweets, args=(user_queue, app_type, recent_tweets), daemon=True)
        worker.start()

    for user_id in recent_tweets:
        print("Adding user", user_id)
        user_queue.put(user_id)

    # Finish queue
    user_queue.join()

    print("Save user")
    # Save file in recent tweets directory

    filename = f"true_users_recent_tweets/true_users_recent_tweets_{start_from_index}_to_{start_from_index+len(batch)}.pickle"

    with open(path / filename, "wb") as f:
        pickle.dump(recent_tweets, f)
    
    # Increment batch counter
    start_from_index = start_from_index + len(batch)

    # DOne
    end = time.time()
    print(f"############ Took {(end-start)/60} minutes #################")
