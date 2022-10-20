import sys
sys.path.append("/Users/laurenzaisenpreis/Uni/Thesis/tweet-collector")

from fake_collector.utils.TwythonConnector import TwythonConnector
import os
import json 
import pickle
from fake_collector.configs.directory_config import Directories
from fake_collector.utils.TwitterUser import TwitterUser
from typing import Dict, List
import pandas as pd
import time

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

        start = time.time()

        # iterate over fake news tweet files in that directory
        #TODO might remove unnecessary loop and create user profiles immediately when loading/reading
        print("Reading tweets from files")
        # iterate over files in that directory
        tweets = []
        for filename in os.listdir(path):
            if filename.startswith('0'):
                print("Read file ", filename)
                items = filename.split("_")
                for line in open(path / filename, 'r'):
                    tweets.append((items[2],items[3],json.loads(line)))

        t1 = time.time()
        print(f'Took {t1 - start} seconds')

        # get user information
        print("Creating user objects from tweets")
        users = {}
        for tweet in tweets:
            try:
                if 'includes' in tweet[2].keys():
                    for user in tweet[2]["includes"]["users"]:
                        user_id = user["id"]
                        if user_id not in users:
                            users[user_id] = TwitterUser(user_id=user_id, user_name=user["name"], description=user['description'], followers_count=user["public_metrics"]["followers_count"], friends_count=user["public_metrics"]["following_count"], tweet_count=user["public_metrics"]["tweet_count"], verified=user["verified"], created_at=user["created_at"])
            except:
                print("Problem with tweet user", user)
        
        t2 = time.time()
        print(f'Took {t2 - t1} seconds')

        # add fake tweet ids to the corresponding user profile
        print("Adding ids to user profiles")
        for entry in tweets:

            topic = entry[0]
            label = entry[1]
            if label == 'barely-true':
                label = 'mostly-false' # https://www.politifact.com/article/2011/jul/27/-barely-true-mostly-false/

            try:
                if "data" in entry[2].keys():
                    for tweet in entry[2]["data"]:
                        # get corresponding user                    
                        author_id = tweet["author_id"]
                        tweet_id = tweet["id"]
                        # get type if present
                        if 'referenced_tweets' in tweet.keys():
                            tweet_type = tweet['referenced_tweets'][0]['type']
                        else:
                            if 'in_reply_to_user_id' in tweet.keys():
                                tweet_type = 'replied_to'
                            else:
                                tweet_type = 'tweet'

                        # add tweet info to user

                        user_obj = users.get(author_id)

                        match tweet_type:
                            case "tweet":
                                if topic not in user_obj.tweets[label].keys():
                                    user_obj.tweets[label][topic] = [tweet_id]
                                else:
                                    user_obj.tweets[label][topic].append(tweet_id)
                            case "retweeted":
                                if topic not in user_obj.retweets[label].keys():
                                    user_obj.retweets[label][topic] = [tweet_id]
                                else:
                                    user_obj.retweets[label][topic].append(tweet_id)
                            case "replied_to":
                                if topic not in user_obj.replies[label].keys():
                                    user_obj.replies[label][topic] = [tweet_id]
                                else:
                                    user_obj.replies[label][topic].append(tweet_id)
            except:
                print("issue with tweet ", tweet)
        
           
        t3 = time.time()
        print(f'Took {t3 - t2} seconds')

        print("Calculating falsity scores for users")
        for user in users.values():
            user.calculate_falsity_score()

           
        t4 = time.time()
        print(f'Took {t4 - t3} seconds')


        print("Saving TwitterUsers list as pickle file")
        users_list = list(users.values())
        path = directory.USERS_PATH / "all_users"
        filename = "users.pickle"

        with open(path / filename, "wb") as f:
            pickle.dump(users_list, f)


    def load_user_profiles_as_list(self) -> List[TwitterUser]:
        # Open pickle file
        directories = Directories()
        path = directories.USERS_PATH / "all_users"
        filename = "users.pickle"
        with open(path / filename, "rb") as f:
            users_loaded = pickle.load(f)
        return users_loaded

    def load_users_profiles_as_df(self) -> pd.DataFrame:
        # Open pickle file
        directories = Directories()
        path = directories.USERS_PATH / "all_users"
        filename = "users.pickle"
        with open(path / filename, "rb") as f:
            users_loaded = pickle.load(f)

        # Turn into dict
        users_dict = {user.user_id : user.get_user_as_dict() for user in users_loaded}

        users_df = pd.DataFrame.from_dict(users_dict.values())
    
        return users_df

    def load_users_profiles_as_dict(self) -> Dict[str, TwitterUser]:
        # Open pickle file
        directories = Directories()
        path = directories.USERS_PATH / "all_users"
        filename = "users.pickle"
        with open(path / filename, "rb") as f:
            users_loaded = pickle.load(f)

        # Turn into dict
        users_dict = {user.user_id : user for user in users_loaded}
    
        return users_dict



if __name__ == "__main__":
    user_collector = UserProfileCollector()
    user_collector.save_user_profiles()