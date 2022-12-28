"""
File to specify necessary model configurations
"""

DRIVER_BINARY_USER_FEATURES = [
    'party',
]

DRIVER_CONTINUOUS_USER_FEATURES = [
    'ideology_score',
    'worldview_alignment',
    'elite_exposure_score',
    'weighted_average_falsity_mutual_friends',
    'Analytic',                               
    # 'Tone',                                   
    'discrep',                                
    'tentat',                                 
    'allnone',                                
    'focusfuture',                            
    'emo_pos',                           
    'emo_neg',                                
    'emo_anx',                                
    'emo_anger',                              
    'emo_sad',                                
    'familiarity_effect_normalized_claim_amount',
    'average_sentiment',
    'positive_sentiment',
    'negative_sentiment',             
    # 'TOXICITY',                               
    # 'SEVERE_TOXICITY',                        
    # 'IDENTITY_ATTACK',                        
    # 'INSULT',                                 
    # 'PROFANITY',                              
    # 'THREAT',                                 
    'flesch_score'
]

FEATURES_TO_DRIVER_NAME = {
    # 'ideology_score',
    'worldview_alignment' : 'Worldview',
    'elite_exposure_score' : 'Elite exposure',
    'weighted_average_falsity_mutual_friends' : 'In-group',
    'Analytic' : 'Intuitive thinking',                               
    # 'Tone',                                   
    'discrep' : 'Discrepancy',                                
    'tentat' : 'Tentativeness',                                 
    'allnone' : 'Certainty',                                
    'focusfuture' : 'Future Focus',                            
    'emo_pos' : 'Positive state',                           
    'emo_neg' : 'Negative state',                                
    'emo_anx' : 'Anxiety',                                
    'emo_anger' : 'Anger',                              
    'emo_sad' : 'Sadness',                                
    'familiarity_effect_normalized_claim_amount' : 'Familiarity effect',
    'average_sentiment' : 'Average sentiment',
    'positive_sentiment' : 'Positive sentiment',
    'negative_sentiment' : 'Negative sentiment',            
    # 'TOXICITY',                               
    # 'SEVERE_TOXICITY',                        
    # 'IDENTITY_ATTACK',                        
    # 'INSULT',                                 
    # 'PROFANITY',                              
    # 'THREAT',                                 
    'flesch_score' : 'Fluency'
}


GENERAL_CONTINUOUS_USER_FEATURES = [
    'followers_count',
    'friends_count',
    'tweet_count',
    'tweets_per_day'
]


