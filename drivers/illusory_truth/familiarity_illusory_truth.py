# Imports and stuff
import sys
import os
sys.path.append('/Users/laurenzaisenpreis/Uni/Thesis/tweet-collector/')
import pandas as pd
from fake_collector.configs.directory_config import Directories
import pickle
import math


def get_familiarity_effect_scores(fake_or_true: str):

    # Get following information of users
    directory = Directories()
    path = directory.USERS_PATH / f"{fake_or_true}_users/{fake_or_true}_users_following" 

    # All tweets we have 
    with open(directory.DATA_PATH / 'tweets/all_tweets.pickle', 'rb') as f:
        tweets_loaded = pickle.load(f)

    # Get following users
    users_all = {}
    for file in os.listdir(path):
        with open(path / file, "rb") as f:
            users_loaded = pickle.load(f)
            users_all.update(users_loaded)

    # Load users as df
    users_dict = {user_id : users_all.get(user_id).get_user_as_dict() for user_id in users_all}

    # Add following ids to twitter user
    twitter_users_dataset = set(users_dict.keys())

    for user_id in users_dict:
        # Get following ids
        following_ids = users_dict.get(user_id)['following_ids']
        # Create list of following fake users
        users_dict.get(user_id)[f'following_{fake_or_true}_users'] = [following_id for following_id in following_ids if following_id in twitter_users_dataset]


    # Get first N users
    N = len(users_dict)

    user_count_no_illusory_truth = 0

    # Initial object
    illusory_truth = {} # Cases where user has been exposed to same claim before AND posted it
    no_illusory_truth = {} # Cases where user has NOT posted but has been exposed to it before

    for user_id in list(users_dict.keys())[:N]:

        following_claims = {} # Of the format {claim_idx : [{tweet_id : id str, created_at : date}]}
        following_claims_count = 0

        # Loop over followings
        for following_id in users_dict.get(user_id)[f'following_{fake_or_true}_users']:

            # Tweets
            for label in users_dict.get(following_id)['tweets']:
                # Topics
                for topic, topic_tweets in users_dict.get(following_id)['tweets'][label].items():
                    # Tweets
                    for tweet in topic_tweets:
                        # Get original tweet info
                        claim_idx = tweets_loaded.get(tweet)['claim_index']
                        tweet_created_at = tweets_loaded.get(tweet)['created_at']
                        # Add tweet to claims
                        if claim_idx in following_claims:
                            following_claims.get(claim_idx).append({'tweet_id' : tweet, 'created_at' : tweet_created_at})
                        else: 
                            following_claims[claim_idx] = [{'tweet_id' : tweet, 'created_at' : tweet_created_at}]

            # Retweets
            for label in users_dict.get(following_id)['retweets']:
                # Topics
                for topic, topic_retweets in users_dict.get(following_id)['retweets'][label].items():
                    # Tweets
                    for retweet in topic_retweets:
                        # Get original tweet info
                        claim_idx = tweets_loaded.get(retweet)['claim_index']
                        retweet_created_at = tweets_loaded.get(retweet)['created_at']
                        # Add tweet to claims
                        if claim_idx in following_claims:
                            following_claims.get(claim_idx).append({'tweet_id' : retweet, 'created_at' : retweet_created_at})
                        else: 
                            following_claims[claim_idx] = [{'tweet_id' : retweet, 'created_at' : retweet_created_at}]


        # Get claims of individual user
        user_claims = {}
        user_claims_count = 0

        # Followings
        for label in users_dict.get(user_id)['tweets']:
            # Topics
            for topic, topic_tweets in users_dict.get(user_id)['tweets'][label].items():
                # Tweets
                for tweet in topic_tweets:
                    # Get original tweet info
                    claim_idx = tweets_loaded.get(tweet)['claim_index']
                    tweet_created_at = tweets_loaded.get(tweet)['created_at']
                    # Add tweet to claims
                    if claim_idx in user_claims:
                        user_claims.get(claim_idx).append({'tweet_id' : tweet, 'created_at' : tweet_created_at})
                    else: 
                        user_claims[claim_idx] = [{'tweet_id' : tweet, 'created_at' : tweet_created_at}]

        # Retweet labels
        for label in users_dict.get(user_id)['retweets']:
            # Topics
            for topic, topic_retweets in users_dict.get(user_id)['retweets'][label].items():
                # Tweets
                for retweet in topic_retweets:
                    # Get original tweet info
                    claim_idx = tweets_loaded.get(retweet)['claim_index']
                    retweet_created_at = tweets_loaded.get(retweet)['created_at']
                    if claim_idx in user_claims:
                        user_claims.get(claim_idx).append({'tweet_id' : retweet, 'created_at' : retweet_created_at})            
                    else:
                        user_claims[claim_idx] = [{'tweet_id' : retweet, 'created_at' : retweet_created_at}]

        for claim in user_claims:

            if claim in following_claims:

                # Sort claims in ascending order
                # This sorts all tweets of a user referring to one claim in ascending order
                user_claims_sorted = sorted(user_claims.get(claim), key=lambda d: d['created_at'], reverse=False) 

                # Get claims of followings
                following_claim_list = following_claims.get(claim)
                # Sort by first occurence date
                following_claim_list_sorted = sorted(following_claim_list, key=lambda d: d['created_at'], reverse=False) 
                claims_prior_to_user = [ claim for claim in following_claim_list_sorted if claim['created_at'] < user_claims_sorted[0]['created_at']]
                
                if len(claims_prior_to_user) > 0:
                    
                    if user_id in illusory_truth.keys():

                        illusory_truth.get(user_id).append({
                        'claim_id' : claim, 'tweeted_at' : user_claims_sorted[0]['created_at'], 'prior_following_claims' : claims_prior_to_user  
                        })

                    else:

                        illusory_truth[user_id] = [{
                        'claim_id' : claim, 'tweeted_at' : user_claims_sorted[0]['created_at'], 'prior_following_claims' : claims_prior_to_user  
                        }]
        
        # All the claims that user has been exposed to but not shared
        for claim in following_claims:

            # All the claims that user has been exposed to but not shared
            if claim not in user_claims:

                if user_id in no_illusory_truth.keys():

                    # Get claims of followings
                    following_claim_list = following_claims.get(claim)

                    no_illusory_truth.get(user_id).append({
                    'claim_id' : claim, 'tweets_by_friends' : following_claim_list  
                    })

                else:

                    no_illusory_truth[user_id] = [{
                    'claim_id' : claim, 'tweets_by_friends' : following_claim_list
                    }]


    # Calc ill truth scores for each user

    for user_id in users_dict:

        try: 
            # List of claims by user with prior tweets
            claims_by_user = illusory_truth.get(user_id)
            claims_amount = len(claims_by_user)
            
            # For each claim, calculate the log of the amount of tweets prior, then aggregate
            log_sum_prior_claims = 0
            for claim in claims_by_user:
                log_sum_prior_claims += math.log(len(claim['prior_following_claims']))
                
            # Normalize by claim count that have prior tweets of this user
            norm_log_sum = log_sum_prior_claims / claims_amount
            users_dict.get(user_id)['familiarity_effect_normalized_claim_amount'] = norm_log_sum

             # Try to normalize by friends count
            norm_log_sum_friends = log_sum_prior_claims / len(users_dict.get(user_id)['following_ids'])
            users_dict.get(user_id)['familiarity_effect_normalized_all_friends_amount'] = norm_log_sum_friends

            # Normalize by amount of fake friends
            norm_log_sum_fake_friends = log_sum_prior_claims / len(users_dict.get(user_id)['following_fake_users'])
            users_dict.get(user_id)['familiarity_effect_normalized_fake_friends_amount'] = norm_log_sum_fake_friends


        except:
            # No familiarity effect for those users
            users_dict.get(user_id)['familiarity_effect_normalized_claim_amount'] = -1
            users_dict.get(user_id)['familiarity_effect_normalized_all_friends_amount'] = -1
            users_dict.get(user_id)['familiarity_effect_normalized_fake_friends_amount'] = -1


    return_dict = {k : {'familiarity_effect_normalized_claim_amount' : v['familiarity_effect_normalized_claim_amount'], 
                        'familiarity_effect_normalized_all_friends_amount' : v['familiarity_effect_normalized_all_friends_amount'], 
                        'familiarity_effect_normalized_fake_friends_amount' : v['familiarity_effect_normalized_fake_friends_amount']} for k,v in users_dict.items()}

    return return_dict
