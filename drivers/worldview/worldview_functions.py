import pandas as pd
import json

def get_party(x, dict_rep_dem):
    try:
        return dict_rep_dem['dem_rep'][int(x)]
    except:
        print("error")



def get_claims_ideology_by_user(fake_users_dict, tweet_party_dict):
    
    users_claim_labels = {}
    
    fake_users = fake_users_dict

    for id in fake_users.keys():
        user = fake_users[id]['user_object']
        tweets = user.get_all_true_tweets_retweets()
        tweets.extend(user.get_all_false_tweets_retweets())
        
        users_claim_labels[id] = {'Democrat':0, 'Republican':0, 'Ambigious':0}
        
        for tweet in tweets:
            val = tweet_party_dict['party'][tweet] 
            users_claim_labels[id][val] += 1    
    
    return users_claim_labels

def use_flw_news_iscore_combined_coverage(fake_users_ideology):
    #basically method to get the largest coverage of data possibly but taking the flw_ideology score where there is no data for the news_ideology_score of a user
    
    #Get the set of i_scores where there is is no news ideology_score
    set_iscore = set()
    for val in fake_users_ideology[~fake_users_ideology.ideology_score.isna()].index:
        set_iscore.add(val)
    
    # make column with higher coverage called i_score (repr. flw score when ideology_score has no values)
    fake_users_ideology['i_score'] = fake_users_ideology.apply(lambda x: x['ideology_score'] if x.name in set_iscore else x['ideology_score_flw'], axis=1)
    
