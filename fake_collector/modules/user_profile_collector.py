from fake_collector.utils.TwythonConnector import TwythonConnector
import os
import json 
import pickle
from fake_collector.configs.directory_config import Directories
from fake_collector.utils.TwitterUser import TwitterUser
from typing import List
import pandas as pd

class UserProfileCollector:
    def __init__(self) -> None:
        """
        Class to both save as well as load user profiles (TwitterUser objects)
        """
        pass

    def save_user_profiles(self):
        """
        First read tweets from fakenews_tw_output directory
        Iterate over all tweets to create user profiles (Twitter User objects)
        Iterate over all tweets to append fake news tweet ID to user profile who tweeted
        """
        directory = Directories()
        path = directory.FAKE_NEWS_TWEETS

        # iterate over fake news tweet files in that directory
        #TODO might remove unnecessary loop and create user profiles immediately when loading/reading
        print("Reading tweets from files")
        tweets = []
        for filename in os.listdir(path):
            if filename.startswith("0"):
                file = open(path / filename, 'r')
                for line in open(path / filename, 'r'):
                    tweets.append(json.loads(line))

        # get user information
        print("Creating user objects from tweets")
        users = {}
        for tweet in tweets:
            try:
                for user in tweet["includes"]["users"]:
                    user_id = int(user["id"])
                    if user_id not in users:
                        users[user_id] = TwitterUser(user_id=user_id, user_name=user["name"], followers_count=user["public_metrics"]["followers_count"], friends_count=user["public_metrics"]["following_count"], tweet_count=user["public_metrics"]["tweet_count"], verified=user["verified"], created_at=user["created_at"])
            except:
                print("Problem with creating user profile in tweet ", tweet)

        # add fake tweet ids to the corresponding user profile
        print("Adding fake tweet ids to user profiles")
        for tweet in tweets:
            try:
                for tweet in tweet["data"]:
                    # get corresponding user
                    author_id = int(tweet["author_id"])
                    tweet_id = int(tweet["id"])

                    user_obj = users.get(author_id)
                    user_obj.add_fake_news_tweet(tweet_id)
            except:
                print("Problem with adding tweet to user profile for  ", tweet)

        
        # store list of TwitterUsers as picke file
        print("Saving TwitterUsers list as pickle file")
        users_list = list(users.values())
        path = directory.USERS_PATH
        filename = "users.pickle"

        with open(path / filename, "wb") as f:
            pickle.dump(users_list, f)


    def load_user_profiles(self) -> List[TwitterUser]:
        # Open pickle file
        directories = Directories()
        path = directories.USERS_PATH
        filename = "users.pickle"
        with open(path / filename, "rb") as f:
            users_loaded = pickle.load(f)
        return users_loaded

    def load_users_profiles_as_df(self) -> pd.DataFrame:
        # Open pickle file
        directories = Directories()
        path = directories.USERS_PATH
        filename = "users.pickle"
        with open(path / filename, "rb") as f:
            users_loaded = pickle.load(f)

        # Turn into dict
        users_dict = {user.user_id:user.get_user_as_dict() for user in users_loaded}

        users_df = pd.DataFrame.from_dict(users_dict.values())
    
        return users_df

