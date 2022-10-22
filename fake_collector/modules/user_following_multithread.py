import sys
import os
sys.path.append(os.getcwd())
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
from fake_collector.utils.load_fake_true_users import load_all_true_users, load_all_fake_users, load_fake_users_by_goup
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

        user = user_queue.get()
        user_following_collector = UserFollowingCollectorV2(app_type=app_type)
        user_following_collector.add_user_friend_ids(user=user)
        user_queue.task_done()

        # Change global user counter var
        global user_counter
        user_counter += 1
        print("User count: ", user_counter)


# Load true or fake users
# users_df = load_all_true_users()
users_df = load_all_fake_users()


############################# ADJUST HERE #########################
start_from_index = 0
users_df = users_df.iloc[start_from_index:]

# Split into batches 
max_users = 2000 #2000
batch_size = 500 #500

# Method to split into batche
def _batch_proccess(df, max_users, batch_size):
    for ndx in range(0, max_users, batch_size):
        yield users_df[ndx:min(ndx+batch_size,max_users)]

# Split df into batches
batches = _batch_proccess(users_df, max_users, batch_size)

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
    filename = f"true_users_following_ids_{start_from_index}_to_{start_from_index+len(batch)}.pickle"

    with open(path / filename, "wb") as f:
        pickle.dump(true_users, f)

    # Increment
    start_from_index = start_from_index + len(batch)

    # Done
    end = time.time()

    print()
    print(f"############ Took {(end-start)/60} minutes #################")
