import pickle
import os
import sys
sys.path.append(os.getcwd())
import pandas as pd
from fake_collector.configs.directory_config import Directories

directory = Directories()


def load_all_fake_users():

    fake_users_path = directory.USERS_PATH / "fake_users"

    with open(fake_users_path / "fake_users.pickle", "rb") as f:
        fake_users_loaded = pickle.load(f)

    # Put fake users into dict
    users_dict = {}

    for fake_group in fake_users_loaded.keys():
        # Loop through those fake users
        for user_id in fake_users_loaded.get(fake_group).keys():
            # Add them to dict
            users_dict[user_id] = fake_users_loaded.get(fake_group).get(user_id).get_user_as_dict()
            users_dict.get(user_id)['fake_group'] = fake_group
    
    # Load as df
    users_dict_df = pd.DataFrame.from_dict(users_dict.values())

    # Sort values by aggregate falsity score
    users_dict_df.sort_values(by='aggregate_falsity_score', ascending=False, inplace=True)

    return users_dict_df


def load_fake_users_by_goup(fake_group: str):
    """
    :param group: very_low, low, medium, high, very_high
    """
    fake_users_path = directory.USERS_PATH / "fake_users"

    with open(fake_users_path / "fake_users.pickle", "rb") as f:
        fake_users_loaded = pickle.load(f)

    # Load specific fake group as df
    users = fake_users_loaded.get(fake_group)

    users_dict = {user_id : users.get(user_id).get_user_as_dict() for user_id in users.keys()}

    users_df = pd.DataFrame.from_dict(users_dict.values())

    users_df['fake_group'] = fake_group

    # Sort according to aggregate score for this group
    users_df.sort_values(by='aggregate_falsity_score', ascending=False, inplace=True)

    return users_df


if __name__ == "__main__":
    res = load_fake_users_by_goup('high')
    print(res)
    print(len(res))
    print('loaded')
