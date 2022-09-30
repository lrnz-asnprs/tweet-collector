import time
import datetime
from tweet_collector.utils.TwythonConnector import TwythonConnector
from twython import TwythonRateLimitError
from tweet_collector.utils.TwitterUser import TwitterUser
from typing import List

class UserFollowingCollector:
    def __init__(self) -> None:
        pass

    def add_user_friends_ids(self, user_list: List[TwitterUser], twitter_app: TwythonConnector) -> List[TwitterUser]:
        """
        Takes users (List[TwitterUser]) as input, adds the corresponding following ID's to each user object, and returns the final list
        """
        user_output_list = user_list.copy()

        for user in user_output_list:
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
        
        return user_output_list

    