import sys
sys.path.append("/Users/laurenzaisenpreis/Uni/Thesis/tweet-collector")
import time
import datetime
from fake_collector.utils.TwythonConnector import TwythonConnector
from fake_collector.configs.directory_config import Directories
from twython import TwythonRateLimitError
from fake_collector.utils.TwitterUser import TwitterUser
from typing import List
from multiprocessing import Process
from fake_collector.modules.user_profile_collector import UserProfileCollector
from fake_collector.modules.user_following_collector_v2 import UserFollowingCollectorV2
from fake_collector.modules.user_following_collector import UserFollowingCollector
import queue
import threading
import time
import pickle
import pandas as pd
import time

user_counter = 0

def add_user_friends_ids(user_queue, app_type):
    """
    Takes user queue as input, adds the corresponding following ID's to each user object, and returns the final list
    """

    print("In worker ", app_type)

    while True:

        if app_type == "laai_elevated":

            user = user_queue.get()
            user_following_collector = UserFollowingCollectorV2(app_type=app_type)
            user_following_collector.add_user_friend_ids(user=user)
            user_queue.task_done()

            # Change global user counter var
            global user_counter
            user_counter += 1
            print("User count: ", user_counter)

        elif app_type == 'laai_academic':

            user = user_queue.get()
            user_following_collector = UserFollowingCollectorV2(app_type=app_type)
            user_following_collector.add_user_friend_ids(user=user)
            user_queue.task_done()

            # Change global user counter var
            user_counter += 1
            print("User count: ", user_counter)

        elif app_type == 'gugy_academic':

            user = user_queue.get()
            user_following_collector = UserFollowingCollectorV2(app_type=app_type)
            user_following_collector.add_user_friend_ids(user=user)
            user_queue.task_done()

            # Change global user counter var
            user_counter += 1
            print("User count: ", user_counter)

        elif app_type == 'gugy_elevated':

            user = user_queue.get()
            user_following_collector = UserFollowingCollectorV2(app_type=app_type)
            user_following_collector.add_user_friend_ids(user=user)
            user_queue.task_done()

            # Change global user counter var
            user_counter += 1
            print("User count: ", user_counter)

        elif app_type == 'luca_academic':

            user = user_queue.get()
            user_following_collector = UserFollowingCollectorV2(app_type=app_type)
            user_following_collector.add_user_friend_ids(user=user)
            user_queue.task_done()

            # Change global user counter var
            user_counter += 1
            print("User count: ", user_counter)

        elif app_type == 'luca_elevated':

            user = user_queue.get()
            user_following_collector = UserFollowingCollectorV2(app_type=app_type)
            user_following_collector.add_user_friend_ids(user=user)
            user_queue.task_done()

            # Change global user counter var
            user_counter += 1
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


############################# ADJUST HERE #########################
# Split into batches 
max_users = 10 
batch_size = 2

# Method to split into batche
def _batch_proccess(df, max_users, batch_size):
    for ndx in range(0, max_users, batch_size):
        yield users_df[ndx:min(ndx+batch_size,max_users)]

# Split df into batches
batches = _batch_proccess(users_df, max_users, batch_size)

batch_index_counter = 0

# Iterate over batches
for batch in batches:    

    start = time.time()

    # Select users from batch
    to_process = [users_loaded.get(user_id) for user_id in batch['user_id']]

    user_queue = queue.Queue()

    for app_type in ['laai_elevated', 'laai_academic', 'gugy_academic', 'gugy_elevated', 'luca_academic', 'luca_elevated']:
        worker = threading.Thread(target=add_user_friends_ids, args=(user_queue, app_type), daemon=True)
        worker.start()

    for user in to_process:
        print("Adding user", user.user_name)
        user_queue.put(user)

    # Finish queue
    user_queue.join()

    # Done, save
    true_users = {}
    for user in to_process:
        true_users[user.user_id] = user

    print("Save user")
    # Save file in true users directory
    filename = f"true_users_following_ids_{batch_index_counter}_to_{batch_index_counter+len(batch)}.pickle"

    with open(path / filename, "wb") as f:
        pickle.dump(true_users, f)

    # Increment
    batch_index_counter = batch_index_counter + len(batch)

    # Done
    end = time.time()

    print()
    print(f"############ Took {(end-start)/60} minutes #################")
