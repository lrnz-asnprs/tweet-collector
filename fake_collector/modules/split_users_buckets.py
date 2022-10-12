import sys
sys.path.append("/Users/laurenzaisenpreis/Uni/Thesis/tweet-collector")

import pandas as pd
import copy
import pickle
from fake_collector.utils.TwythonConnector import TwythonConnector
# from fake_collector.modules.user_profile_collector import UserProfileCollector
from fake_collector.utils.TwitterUser import TwitterUser
from fake_collector.configs.directory_config import Directories
from fake_collector.modules.user_profile_collector import UserProfileCollector


# Directories
directories = Directories()
path = directories.USERS_PATH


def save_only_true_users():

    print("Load everything")
    # Load user profiles
    user_profile_collector = UserProfileCollector()
    user_df = user_profile_collector.load_users_profiles_as_df()
    users_obj = user_profile_collector.load_users_profiles_as_dict()
    
    # Make a copy of the initial objects
    # users_objects = copy.deepcopy(users_obj)

    print("Prep DF")
    # Check which users have posts ONLY true tweets or retweets
    user_df['only_true'] = user_df.apply(lambda x: 1 if 
                            (len(users_obj.get(x['user_id']).get_all_false_tweets_retweets()) == 0) 
                            & (len(users_obj.get(x['user_id']).get_half_true_tweets()) == 0) 
                            & (len(users_obj.get(x['user_id']).get_half_true_retweets()) == 0) 
                            & (len(users_obj.get(x['user_id']).get_mostly_true_tweets()) == 0) 
                            & (len(users_obj.get(x['user_id']).get_mostly_true_retweets()) == 0) 
                            else 0, axis=1)

    # Get df of only true users
    only_true = user_df[user_df['only_true'] == 1].copy()

    # Get the true tweet count
    only_true['true_tweet_count'] = only_true.apply(lambda x: (len(users_obj.get(x['user_id']).get_true_tweets())) + len(users_obj.get(x['user_id']).get_true_retweets()), axis=1)

    true_users = {}
    for user_id in only_true['user_id']:
        if user_id in users_obj.keys():
            true_users[user_id] = users_obj.get(user_id)
    
    print("Save user")
    # Save file in true users directory
    filename = "true_users.pickle"

    with open(path / "true_users" / filename, "wb") as f:
        pickle.dump(user_df, f)


save_only_true_users()