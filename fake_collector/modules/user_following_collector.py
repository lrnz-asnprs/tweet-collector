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
import queue


class UserFollowingCollector:
    def __init__(self) -> None:
        pass

    def add_user_friends_ids(self, user: TwitterUser, twitter_app: TwythonConnector):
        """
        """
        print("Trying user ", user.user_name)
        cursor = -1
        while cursor != 0:
            try:
                response = twitter_app.twitter_connection.get_friends_ids(user_id=user.get_user_id(), cursor=cursor, count=5000)
                following_ids = response['ids']
                user.add_following_ids(following_ids)
                cursor = response['next_cursor']

            except TwythonRateLimitError as error:
                rate_limit_stats = twitter_app.twitter_connection.get_application_rate_limit_status()
                remaining_time = rate_limit_stats["resources"]["friends"]["/friends/ids"]["reset"]
                remainder = remaining_time - time.time() # epoch time
                minutes = remainder // 60 % 60
                print("Sleeping for minutes: ", minutes)
                time.sleep(remainder)
                twitter_app.make_connection() # make a new connection
                continue
