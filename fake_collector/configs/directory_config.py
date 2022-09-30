from pathlib import Path
import fake_collector
import os

class Directories:
    """
    Class with all parths used in the repo
    """
    REPO_PATH = Path(fake_collector.__file__).parent.parent
    DATA_PATH = REPO_PATH / "data"
    FAKE_NEWS_SOURCES = DATA_PATH / "fakenews_sources"
    FAKE_NEWS_TWEETS = DATA_PATH / "fakenews_tw_output"
    USERS_PATH = DATA_PATH / "users"


if __name__ == "__main__":
    dir = Directories()
    print(dir.USERS_PATH)