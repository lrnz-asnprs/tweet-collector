import pickle
import os
import sys
sys.path.append(os.getcwd())
import pandas as pd
from fake_collector.configs.directory_config import Directories

directory = Directories()


def load_true_or_fake_df(users: str):
    """Get either fake users or true users as a dataframe 

    :param users: true or fake as string

    Returns: fake or true users dataframes
    """
    if users == 'true':
        return load_all_true_users_df()
    elif users == 'fake':
        return load_all_fake_users_df()

def load_true_or_fake_dict(users: str):
    """Loads the true or fake users as a dictionary
    True users: {"user_id" : twitter user object}
    Fake users: {'user_id" : {'user_object' : twitter user object, 'fake_group' : whether this user is in low,med,high fake group}}

    :param users: true or fake as string
    """
    if users == 'true':
        return load_all_true_users()
    elif users == 'fake':
        return load_all_fake_users_dict()


def load_all_true_users():
    # Directories add path name!
    path = directory.USERS_PATH / "true_users"

    # Load the user profiles
    filename = "true_users.pickle"
    with open(path / filename, "rb") as f:
        users_loaded = pickle.load(f)

    return users_loaded


def load_all_fake_users_dict():

    fake_users_path = directory.USERS_PATH / "fake_users"

    with open(fake_users_path / "fake_users.pickle", "rb") as f:
        fake_users_loaded = pickle.load(f)

    # Put fake users into dict
    users_dict = {}

    for fake_group in fake_users_loaded.keys():
        # Loop through those fake users
        for user_id in fake_users_loaded.get(fake_group).keys():
            # Add them to dict
            users_dict[user_id] = {"user_object" : fake_users_loaded.get(fake_group).get(user_id)}
            users_dict.get(user_id)['fake_group'] = fake_group

    return users_dict


def load_all_fake_users_df():
    """Loads the fake users as a dataframe including the info about which fake group they belong to
    
    """
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


def load_fake_users_by_goup_df(fake_group: str):
    """Loads the users as dataframe belonging to the respective fake group

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


def load_all_true_users_df():
    """
    Loads all true users as a dataframe
    """
    # Directories add path name!
    path = directory.USERS_PATH / "true_users"

    # Load the user profiles
    filename = "true_users.pickle"
    with open(path / filename, "rb") as f:
        users_loaded = pickle.load(f)

    # Just transform for saving as df
    users_dict = {id : users_loaded.get(id).get_user_as_dict() for id in users_loaded.keys()}

    # Load users as df
    users_df = pd.DataFrame.from_dict(users_dict.values())
    users_df.head()

    # Add the labeled tweet count to the user df
    users_df['labeled_tweet_count'] = users_df.apply(lambda x: len(users_loaded.get(x['user_id']).get_all_true_tweets_retweets()) + len(users_loaded.get(x['user_id']).get_all_false_tweets_retweets()), axis=1)
    # Rank users
    users_df['rank'] = users_df['labeled_tweet_count'].rank(method='dense')
    users_df.sort_values(by='rank', ascending=False, inplace=True)

    # Only return TOP 5000 users
    users_df = users_df[:5000]
    
    return users_df
    
def load_all_true_users_dict():
    """
    Loads all true users as a dictionary
    """
    # Directories add path name!
    path = directory.USERS_PATH / "true_users"

    # Load the user profiles
    filename = "true_users.pickle"
    with open(path / filename, "rb") as f:
        users_loaded = pickle.load(f)

    # Just transform for saving as df
    users_dict = {id : users_loaded.get(id).get_user_as_dict() for id in users_loaded.keys()}

    # Load users as df
    users_df = pd.DataFrame.from_dict(users_dict.values())
    users_df.head()

    # Add the labeled tweet count to the user df
    users_df['labeled_tweet_count'] = users_df.apply(lambda x: len(users_loaded.get(x['user_id']).get_all_true_tweets_retweets()) + len(users_loaded.get(x['user_id']).get_all_false_tweets_retweets()), axis=1)
    # Rank users
    users_df['rank'] = users_df['labeled_tweet_count'].rank(method='dense')
    users_df.sort_values(by='rank', ascending=False, inplace=True)

    # Only look at TOP 5000 users
    users_df = users_df[:5000]

    # Grab the top 5000 user ids and return as dict
    return_dict = {}
    user_ids = list(users_df['user_id'])
    for user_id in user_ids:
        return_dict[user_id] = {'user_object':users_loaded.get(user_id)}

    return return_dict


if __name__ == "__main__":
    res = load_fake_users_by_goup('high')
    print(res)
    print(len(res))
    print('loaded')
