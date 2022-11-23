
# Imports and stuff
import sys
import os
sys.path.append('/Users/laurenzaisenpreis/Uni/Thesis/tweet-collector/')
import pandas as pd
from fake_collector.configs.directory_config import Directories
import pickle
import numpy as np
from typing import Dict
from drivers.source_cues.elite_exposure import get_elite_exposure_scores
from drivers.source_cues.in_group import get_in_group_scores
from drivers.illusory_truth.familiarity_illusory_truth import get_familiarity_effect_scores
from drivers.emotions.emotional_content import get_emotional_content_fluency_scores

"""
Specify if done for fake or true users
"""
fake_or_true = 'fake'

dirs = Directories()
emotion_state_folder = dirs.DATA_PATH / 'emotion_dictionary/'

# Get emotional_state_df
emotional_state = pd.read_csv(emotion_state_folder / f'{fake_or_true}_users_processed.csv')

# Select the right emotional_state features
features_to_extract = ['Analytic', 'Tone', 'discrep', 'tentat','allnone','focusfuture', 'emo_pos', 'emo_neg', 'emo_anx', 'emo_anger', 'emo_sad'] 
emotional_state.set_index('user_id', inplace=True)
emotional_state_dict = emotional_state[features_to_extract].to_dict(orient='index')

# Change dtype to str of keys
emotional_state_dict = {str(k):v for k,v in emotional_state_dict.items()}
emotional_state_df = pd.DataFrame.from_dict(emotional_state_dict, orient='index')

print("Getting elite exposure scores")
# Get elite_exposure_scores
elite_exposure_scores = get_elite_exposure_scores(fake_or_true=fake_or_true)
elite_exposure_scores_df = pd.DataFrame.from_dict(elite_exposure_scores, orient='index')

print("Getting in group scores")
# Get in-group scores
in_group_scores = get_in_group_scores(fake_or_true=fake_or_true)
in_group_scores_df = pd.DataFrame.from_dict(in_group_scores, orient='index')

print("Getting familiarity effect")
# Get familiarity effect
familiarity_effect = get_familiarity_effect_scores(fake_or_true=fake_or_true)
familiarity_effect_df = pd.DataFrame.from_dict(familiarity_effect, orient='index')

print('Getting emotional content & fluency scores')
# Get emotional content & familiarity fluency average scores per user
emotion_content_fluency_scores = get_emotional_content_fluency_scores(fake_or_true=fake_or_true)
emotion_content_fluency_df = pd.DataFrame.from_dict(emotion_content_fluency_scores, orient='index')

# Put user features together
joined = elite_exposure_scores_df \
    .join(in_group_scores_df, how='inner') \
    .join(emotional_state_df, how='inner') \
    .join(familiarity_effect_df, how='inner') \
    .join(emotion_content_fluency_df, how='inner')

print("Saving")
# Save it 
joined.to_pickle(dirs.USERS_PATH / f'{fake_or_true}_users/{fake_or_true}_users_ALL_driver_features.pickle')

