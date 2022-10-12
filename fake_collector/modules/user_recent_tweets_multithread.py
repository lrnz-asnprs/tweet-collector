from concurrent.futures import thread
import sys
sys.path.append("/Users/laurenzaisenpreis/Uni/Thesis/tweet-collector")
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
import queue
import threading
import time

user_counter = 0

def add_user_recent_tweets(user_queue, app_type):
    """
    Takes user queue as input, adds the corresponding following ID's to each user object, and returns the final list
    """

    print("In worker ", app_type)

    while True:

        if app_type == "elevated":

            user = user_queue.get()
            user_recent_tweets_collector = UserLatestTweetsCollectorV2(app_type=app_type)
            user_recent_tweets_collector.get_user_timeline(user=user)
            user_queue.task_done()

            # Change global user counter var
            global user_counter
            user_counter += 1
            print("User count: ", user_counter)

        else:

            user = user_queue.get()
            user_recent_tweets_collector = UserLatestTweetsCollectorV2(app_type=app_type)
            user_recent_tweets_collector.get_user_timeline(user=user)
            user_queue.task_done()

            # Change global user counter var
            user_counter += 1
            print("User count: ", user_counter)


# Load the user profiles
user_profile_collector = UserProfileCollector()
user_profiles = user_profile_collector.load_user_profiles_as_list()

user_queue = queue.Queue()

for app_type in ['elevated', 'academic']:
    worker = threading.Thread(target=add_user_recent_tweets, args=(user_queue, app_type), daemon=True)
    worker.start()

for i in range(10):
    print("Adding user", user_profiles[i].user_name)
    user_queue.put(user_profiles[i])

# for user in user_profiles:
#     user_queue.put(user)

user_queue.join()

print(f"{user_profiles[0]} recent tweets: ", len(user_profiles[1].recent_tweets))
print(f"{user_profiles[1]} recent tweets: ", len(user_profiles[2].recent_tweets))
print(f"{user_profiles[2]} recent tweets: ", len(user_profiles[3].recent_tweets))
print(f"{user_profiles[3]} recent tweets: ", len(user_profiles[4].recent_tweets))