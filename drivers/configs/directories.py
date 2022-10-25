from pathlib import Path
import os

class Directories:
    """
    Class with all parths used in the repo
    """
    REPO_PATH = Path(os.getcwd())
    
    #If issue with os.path should occur.
    if not str(REPO_PATH).endswith("tweet-collector"):
        REPO_PATH = REPO_PATH.parent
        if not str(REPO_PATH).endswith("tweet-collector"):
            print(REPO_PATH / "ISSUE! --> Check the drivers/config/directories.py file for issues")
    
    DATA_PATH = REPO_PATH / "data"
    FAKE_NEWS_SOURCES = DATA_PATH / "fakenews_sources"
    FAKE_NEWS_TWEETS = DATA_PATH / "fakenews_tw_output"
    NEWS_OUTLETS_PATH = DATA_PATH / "news_outlets"
    
    
    #USERS
    USERS_PATH = DATA_PATH / "users"
    #FAKE USERS
    FAKE_USERS_PATH = USERS_PATH / "fake_users"
    FAKE_USERS_RECENT_TWEETS_PATH = FAKE_USERS_PATH / "fake_users_recent_tweets"
    FAKE_USERS_FOLLOWING_PATH = FAKE_USERS_PATH / "fake_users_following"
    #TRUE USERS
    TRUE_USERS_PATH = USERS_PATH / "true_users"
    TRUE_USERS_RECENT_TWEETS_PATH = TRUE_USERS_PATH / "true_users_recent_tweets"
    TRUE_USERS_FOLLOWING_PATH = TRUE_USERS_PATH / "true_users_following"
    
    
    TOKENS_PATH = REPO_PATH / "tokens.json"

if __name__ == "__main__":
    dir = Directories()