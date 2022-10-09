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
import queue
import threading
import time


def add_user_friends_ids(user_queue, app_type):
    """
    Takes user queue as input, adds the corresponding following ID's to each user object, and returns the final list
    """

    print("in worker ", app_type)

    while True:

        if app_type == "normal":

            user_following_collector_v2 = UserFollowingCollectorV2(app_type=app_type)
            user = user_queue.get()
            user_following_collector_v2.get_friends(user=user)
            user_queue.task_done()

        else:

            twitter_app = TwythonConnector(app_type=app_type)
            twitter_app.make_connection()

            user = user_queue.get()
            user_following_collector = UserFollowingCollector()
            user_following_collector.add_user_friends_ids(user=user, twitter_app=twitter_app)
            user_queue.task_done()


# Load the user profiles
user_profile_collector = UserProfileCollector()
user_profiles = user_profile_collector.load_user_profiles_as_list()

user_queue = queue.Queue()

for app_type in ['normal', 'academic']:
    worker = threading.Thread(target=add_user_friends_ids, args=(user_queue, app_type), daemon=True)
    worker.start()

for i in range(32):
    print("adding user", user_profiles[i].user_name)
    user_queue.put(user_profiles[i])

# for user in user_profiles:
#     user_queue.put(user)

user_queue.join()

print(f"{user_profiles[0]} friends: ", len(user_profiles[5].following_ids))
print(f"{user_profiles[1]} friends: ", len(user_profiles[6].following_ids))
print(f"{user_profiles[2]} friends: ", len(user_profiles[7].following_ids))
print(f"{user_profiles[3]} friends: ", len(user_profiles[8].following_ids))