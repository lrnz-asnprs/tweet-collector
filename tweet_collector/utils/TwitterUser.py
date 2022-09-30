


from datetime import datetime
from typing import List


class TwitterUser:
    def __init__(
        self, 
        user_id: int, 
        user_name: str, 
        followers_count: int, 
        friends_count: int, 
        tweet_count: int,
        verified: bool, 
        location: str,
        created_at: datetime,
        fake_news_tweets: List[int] = None,
        following_ids: List[int] = None
        ):
        """
        Twitter user object holding all relevant attributes.
        """
        self.user_id = user_id
        self.user_name = user_name
        self.followers_count = followers_count
        self.friends_count = friends_count
        self.tweet_count = tweet_count
        self.verified = verified
        self.location = location
        self.created_at = created_at
        self.fake_news_tweets = [] # empty at first
        self.following_ids = []
    
    def get_user_id(self):
        return self.user_id

    def is_verified(self):
        return self.verified

    def get_fake_news_tweets(self):
        return self.fake_news_tweets

    def add_following_ids(self, following_ids: List[int]):
        self.following_ids = list(set(self.following_ids + following_ids))
    