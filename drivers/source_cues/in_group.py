# Imports and stuff
import sys
import os
sys.path.append('/Users/laurenzaisenpreis/Uni/Thesis/tweet-collector/')
import pandas as pd
from fake_collector.configs.directory_config import Directories
import pickle
from datetime import datetime
from datetime import date
import pandas as pd
import numpy as np


def get_in_group_scores(fake_or_true: str):
    """
    Returns dict of type {user_id : weighted_avg_falsity_mutual_friends, tweets_per_day, mutual_friends}
    """
    # Get following information of users
    directory = Directories()
    path = directory.USERS_PATH / f"{fake_or_true}_users/{fake_or_true}_users_following" 

    # Get following users
    users_all = {}
    for file in os.listdir(path):
        with open(path / file, "rb") as f:
            users_loaded = pickle.load(f)
            users_all.update(users_loaded)


    # Load users as df
    users_dict = {user_id : users_all.get(user_id).get_user_as_dict() for user_id in users_all}

    users_df = pd.DataFrame.from_dict(users_dict.values())

    # First add other fake users as friends 
    twitter_users_dataset = set(users_dict.keys())

    for user_id in users_dict:
        # Get friend ids
        following_ids = users_dict.get(user_id)['following_ids']
        # Create list of friend fake users
        users_dict.get(user_id)[f'following_{fake_or_true}_users'] = [following_id for following_id in following_ids if following_id in twitter_users_dataset]

    # Next only get mutual friends (bidirectional following)# Add mutual friends
    for user_id in users_dict:
        # Get other fake users from dataset
        following_fake_users = users_dict.get(user_id)[f'following_{fake_or_true}_users']
        # Loop through following fake users and check wether they follow back this user
        mutual_friends = []
        for friend in following_fake_users:
            if user_id in users_dict.get(friend)['following_ids']:
                mutual_friends.append(friend)
        users_dict.get(user_id)['mutual_friends'] = mutual_friends


    # Next calculate weighted falsity of in-group

    # Get days since creation
    today = date.today()

    # Add it to dataframe
    users_df['days_since_created'] = users_df['created_at'].apply(lambda x: (today - pd.to_datetime(x, format='%Y-%m-%d').date()).days)
    users_df['tweets_per_month'] = users_df['tweet_count'] / (users_df['days_since_created'] / 30)

    # Add it do dictioinary
    for user_id in users_dict:
        users_dict.get(user_id)['days_since_created'] = (today - pd.to_datetime(users_dict.get(user_id)['created_at'], format='%Y-%m-%d').date()).days
        users_dict.get(user_id)['tweets_per_day'] = users_dict.get(user_id)['tweet_count'] / users_dict.get(user_id)['days_since_created']


    """
    This score is a self fulfilling prophecy -> score is naturally high, because we can only consider fake users in dataset

    Weighted by the average number of tweets per two-month period in the past two years of the corresponding account
    """

    for user_id in users_dict:

        try:
        
            mutual_friends = users_dict.get(user_id)['mutual_friends']

            agg_falsity_scores = [users_dict.get(mutual_friend)['aggregate_falsity_score'] for mutual_friend in mutual_friends]
            avg_falsity_scores = [users_dict.get(mutual_friend)['average_falsity_score'] for mutual_friend in mutual_friends]

            weights = [users_dict.get(mutual_friend)['tweets_per_day']*60 for mutual_friend in mutual_friends] # Tweets in a two months period

            agg_weighted_avg = np.average(agg_falsity_scores)
            avg_weighted_avg = np.average(avg_falsity_scores)

            users_dict[user_id]['weighted_aggregate_falsity_mutual_friends'] = agg_weighted_avg
            users_dict[user_id]['weighted_average_falsity_mutual_friends'] = avg_weighted_avg

        except:

            users_dict[user_id]['weighted_aggregate_falsity_mutual_friends'] = 0
            users_dict[user_id]['weighted_average_falsity_mutual_friends'] = 0


    # For sanity checking, add scores to df
    users_df['weighted_aggregate_falsity_mutual_friends'] = users_df['user_id'].apply(lambda x: users_dict.get(x)['weighted_aggregate_falsity_mutual_friends'])
    users_df['weighted_average_falsity_mutual_friends'] = users_df['user_id'].apply(lambda x: users_dict.get(x)['weighted_average_falsity_mutual_friends'])

    users_df['aggregate_falsity_score'].corr(users_df['weighted_average_falsity_mutual_friends'])

    # Return dict with the necessary columns
    return_dict = {}

    for user_id in users_dict:
        if user_id not in return_dict:
            return_dict[user_id] = { 'weighted_aggregate_falsity_mutual_friends':users_dict.get(user_id)['weighted_aggregate_falsity_mutual_friends'],
                                    'weighted_average_falsity_mutual_friends':users_dict.get(user_id)['weighted_average_falsity_mutual_friends'],
                                    'tweets_per_day':users_dict.get(user_id)['tweets_per_day'],
                                    'mutual_friends':users_dict.get(user_id)['mutual_friends']
                                    }

    return return_dict