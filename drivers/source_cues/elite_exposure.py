# Imports and stuff
import sys
import os
sys.path.append('/Users/laurenzaisenpreis/Uni/Thesis/tweet-collector/')
import pandas as pd
from fake_collector.configs.directory_config import Directories
import pickle
import numpy as np
from typing import Dict

def get_elite_exposure_scores(fake_or_true: str):
    """
    Returns dictionary of user_id : {elite_exposure_score, elites_followed(list)}
    """

    directory = Directories()
    path = directory.USERS_PATH / f"{fake_or_true}_users/{fake_or_true}_users_following" 

    # Get following users
    users_all = {}
    for file in os.listdir(path):
        with open(path / file, "rb") as f:
            users_loaded = pickle.load(f)
            users_all.update(users_loaded)

    # Get elite scores
    path2 = directory.DATA_PATH
    elites = pd.read_csv(path2 / "falsity_scores/falsity.scores.csv")
    elites = elites.astype({'elite_id_str': 'str'})


    # Add elite exposure scores to users
    for user_id in users_all:
    # Following ids of this user
        following_ids = users_all.get(user_id).following_ids
    # Get matches
        following_elites = list(set(following_ids).intersection(set(elites['elite_id_str'])))

        if len(following_elites) > 0:
        # Calculate weighted average exposure score
            falsity_scores = [elites.loc[elites['elite_id_str'] == elite_id, 'falsity_score'].values[0] for elite_id in following_elites]
            elite_weights = [elites.loc[elites['elite_id_str'] == elite_id, 'elite_weight'].values[0] for elite_id in following_elites]
        # Calculate weighted average for this user
            weighted_average_exposure_score = np.average(falsity_scores, weights=elite_weights)
        # Add falsity score to user object
            users_all.get(user_id).elite_exposure_score = weighted_average_exposure_score
        # Add elite ids to user object
            users_all.get(user_id).elite_ids = following_elites
        else:
        # If not following any elites, set score to 0
            users_all.get(user_id).elite_exposure_score = 0 
        # No elites followed, add empty list
            users_all.get(user_id).elite_ids = []


    return_dict = { user_id : {'elite_exposure_score': users_all.get(user_id).elite_exposure_score, 'elite_ids' : users_all.get(user_id).elite_ids } for user_id in users_all }

    # Return dict
    return return_dict
