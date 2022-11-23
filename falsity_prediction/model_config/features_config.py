"""
File to specify necessary model configurations
"""

DRIVER_BINARY_USER_FEATURES = [
    'party',
]

DRIVER_CONTINUOUS_USER_FEATURES = [
    # 'ideology_score',
    'worldview_alignment',
    'elite_exposure_score',
    'weighted_avg_falsity_mutual_friends',
    'Analytic',                               
    'Tone',                                   
    'discrep',                                
    'tentat',                                 
    'allnone',                                
    'focusfuture',                            
    'emo_pos',                           
    'emo_neg',                                
    'emo_anx',                                
    'emo_anger',                              
    'emo_sad',                                
    'familiarity_effect_claim',               
    'TOXICITY',                               
    'SEVERE_TOXICITY',                        
    'IDENTITY_ATTACK',                        
    'INSULT',                                 
    'PROFANITY',                              
    'THREAT',                                 
    'flesch_score'
]


GENERAL_CONTINUOUS_USER_FEATURES = [
    'followers_count',
    'friends_count',
    'tweet_count',
    'tweets_per_day'
]


