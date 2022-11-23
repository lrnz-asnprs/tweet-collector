# Imports and stuff
import sys
import os
sys.path.append('/Users/laurenzaisenpreis/Uni/Thesis/tweet-collector/')
import pandas as pd
from fake_collector.configs.directory_config import Directories
import pickle
import numpy as np
from fake_collector.utils.load_fake_true_users import load_all_fake_users_dict, load_all_true_users_dict


def get_emotional_content_fluency_scores(fake_or_true: str):
    """
    Returns average of toxicity values for all claims that a user has posted plus fluency flesch reading easy average score
    """
    dir = Directories()

    # Load claims
    claim_dir = dir.DATA_PATH / 'fakenews_sources'
    claims = pd.read_csv(claim_dir / 'politifact_claims_all_features_0911.csv')

    # All tweets we have 
    tweet_dir = dir.DATA_PATH / 'tweets'
    with open(tweet_dir / 'all_tweets.pickle', 'rb') as f:
        tweets_loaded = pickle.load(f)

    # Now get tweets from user
    if fake_or_true == 'fake':
        users = load_all_fake_users_dict()
    else:
        users = load_all_true_users_dict()
        print("Taking this amount of true users ", len(users))

    # Dictionary to return
    return_dict = {}

    # Loop through every user
    for user_id in users:

        # Get tweets of that user
        users_tweets = users.get(user_id)['user_object'].get_all_false_tweets_retweets() + users.get(user_id)['user_object'].get_all_true_tweets_retweets()

        # Features to extract
        emotional_features = ['TOXICITY', 'SEVERE_TOXICITY', 'IDENTITY_ATTACK', 'INSULT', 'PROFANITY', 'THREAT', 'flesch_score']
        for tweet in users_tweets:

            # user emotional features temporary store
            user_emotion_stats = {'TOXICITY':[], 'SEVERE_TOXICITY':[], 'IDENTITY_ATTACK':[], 'INSULT':[], 'PROFANITY':[], 'THREAT':[], 'flesch_score':[]}

            # Grab emotional features from claim
            claim_index = tweets_loaded.get(tweet)['claim_index']
            claims_features = claims.loc[claims['claim_index'] == int(claim_index)]
            for emotion in emotional_features:
                user_emotion_stats[emotion].append(claims_features[emotion].values[0])

        # When done, calc average and return that per user
        for emotion in emotional_features:
            emotion_avg = np.average(user_emotion_stats.get(emotion))
            user_emotion_stats[emotion] = emotion_avg
        
        return_dict[user_id] = user_emotion_stats

    return return_dict