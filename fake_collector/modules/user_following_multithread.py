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

user_counter = 0

def add_user_friends_ids(user_queue, app_type):
    """
    Takes user queue as input, adds the corresponding following ID's to each user object, and returns the final list
    """

    print("In worker ", app_type)

    while True:

        if app_type == "elevated":

            user = user_queue.get()
            user_following_collector = UserFollowingCollector(app_type=app_type)
            user_following_collector.add_user_friends_ids(user=user)
            user_queue.task_done()

            # Change global user counter var
            global user_counter
            user_counter += 1
            print("User count: ", user_counter)

        else:

            user = user_queue.get()
            user_following_collector = UserFollowingCollector(app_type=app_type)
            user_following_collector.add_user_friends_ids(user=user)
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

# Select first K profiles
k = 10
top_k = users_df.head(k)
to_process = [users_loaded.get(user_id) for user_id in top_k['user_id']]

user_queue = queue.Queue()

for app_type in ['elevated', 'academic']:
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
filename = "true_users_following_ids.pickle"

with open(path / filename, "wb") as f:
    pickle.dump(true_users, f)
