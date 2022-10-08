
from datetime import datetime
from typing import Dict, List


class TwitterUser:
    def __init__(
        self, 
        user_id: str, 
        user_name: str,
        description: str,
        followers_count: int, 
        friends_count: int, 
        tweet_count: int,
        verified: bool, 
        created_at: datetime,
        average_falsity_score: int = None,
        aggregate_falsity_score: int = None,
        tweets: Dict[str, Dict[str,List]] = None,
        retweets: Dict[str, Dict[str,List]] = None,
        replies: Dict[str, Dict[str,List]] = None,
        following_ids: List[str] = None,
        ):
        """
        Twitter user object holding all relevant attributes.
        """
        self.user_id = user_id
        self.user_name = user_name
        self.description = description
        self.followers_count = followers_count
        self.friends_count = friends_count
        self.tweet_count = tweet_count
        self.verified = verified
        self.created_at = created_at
        self.tweets = {
            "pants-fire": {}, # categories in the next level
            "false": {},
            "mostly-false": {},
            "half-true": {},
            "mostly-true": {},
            "true": {}
        } 
        self.retweets = {
            "pants-fire": {},
            "false": {},
            "mostly-false": {},
            "half-true": {},
            "mostly-true": {},
            "true": {}
        } 
        self.replies = {
            "pants-fire": {},
            "false": {},
            "mostly-false": {},
            "half-true": {},
            "mostly-true": {},
            "true": {}
        } 
        self.aggregate_falsity_score = -1 # initialized at -1 
        self.average_falsity_score = -1 # initialized at -1 
        self.following_ids = []
    
    def get_user_id(self):
        return self.user_id

    def is_verified(self):
        return self.verified

    # All tweet getters
    def get_all_false_tweets_retweets(self):
        all_false_tweets = self.get_false_tweets() + self.get_mostly_false_tweets() + self.get_pants_fire_tweets()
        all_false_retweets = self.get_false_retweets() + self.get_mostly_false_retweets() + self.get_pants_fire_retweets()
        return all_false_tweets + all_false_retweets

    def get_all_true_tweets_retweets(self):
        all_true_tweets = self.get_true_tweets() + self.get_mostly_true_tweets() + self.get_half_true_tweets()
        all_true_retweets = self.get_true_retweets() + self.get_mostly_true_retweets() + self.get_half_true_retweets()
        return all_true_tweets + all_true_retweets

    # falsity score
    def calculate_falsity_score(self):

        temp_falsity_score = 0
        tweet_counter = 0

        # Tweets
        for label in self.tweets.keys():
            match label:
                case "pants-fire":
                    pants_tweets = []
                    for topic in self.tweets['pants-fire']:
                        pants_tweets = pants_tweets + self.tweets['pants-fire'][topic]
                    temp_falsity_score += len(pants_tweets) * 1
                    tweet_counter += len(pants_tweets)
                case "false":
                    false_tweets = self.get_false_tweets()
                    temp_falsity_score += len(false_tweets) * 0.8
                    tweet_counter += len(false_tweets)
                case "mostly-false":
                    mostly_false_tweets = []
                    for topic in self.tweets['mostly-false']:
                        mostly_false_tweets = mostly_false_tweets + self.tweets['mostly-false'][topic]
                    temp_falsity_score += len(mostly_false_tweets) * 0.6
                    tweet_counter += len(mostly_false_tweets)
                case "half-true":
                    half_true_tweets = []
                    for topic in self.tweets['half-true']:
                        half_true_tweets = half_true_tweets + self.tweets['half-true'][topic]
                    temp_falsity_score += len(half_true_tweets) * 0.4
                    tweet_counter += len(half_true_tweets)
                case "mostly-true":
                    mostly_true_tweets = []
                    for topic in self.tweets['mostly-true']:
                        mostly_true_tweets = mostly_true_tweets + self.tweets['mostly-true'][topic]
                    temp_falsity_score += len(mostly_true_tweets) * 0.2
                    tweet_counter += len(mostly_true_tweets)
                case "true":
                    true_tweets = self.get_true_tweets()
                    tweet_counter += len(true_tweets)
        
        # Retweets
        for label in self.retweets.keys():
            match label:
                case "pants-fire":
                    pants_retweets = []
                    for topic in self.retweets['pants-fire']:
                        pants_retweets = pants_retweets + self.retweets['pants-fire'][topic]
                    temp_falsity_score += len(pants_tweets) * 1
                    tweet_counter += len(pants_retweets)
                case "false":
                    false_retweets = self.get_false_retweets()
                    temp_falsity_score += len(false_retweets) * 0.8
                    tweet_counter += len(false_retweets)
                case "mostly-false":
                    mostly_false_retweets = []
                    for topic in self.retweets['mostly-false']:
                        mostly_false_retweets = mostly_false_retweets + self.retweets['mostly-false'][topic]
                    temp_falsity_score += len(mostly_false_retweets) * 0.6
                    tweet_counter += len(mostly_false_retweets)
                case "half-true":
                    half_true_retweets = []
                    for topic in self.retweets['half-true']:
                        half_true_retweets = half_true_retweets + self.retweets['half-true'][topic]
                    temp_falsity_score += len(half_true_retweets) * 0.4
                    tweet_counter += len(half_true_retweets)
                case "mostly-true":
                    mostly_true_retweets = []
                    for topic in self.retweets['mostly-true']:
                        mostly_true_retweets = mostly_true_retweets + self.retweets['mostly-true'][topic]
                    temp_falsity_score += len(mostly_true_retweets) * 0.2
                    tweet_counter += len(mostly_true_retweets)
                case "true":
                    true_retweets = self.get_true_retweets()
                    tweet_counter += len(true_retweets)


        if tweet_counter == 0: # user only had replies
            self.aggregate_falsity_score = -1
            self.average_falsity_score = -1
        else:
            self.aggregate_falsity_score = temp_falsity_score
            self.average_falsity_score = temp_falsity_score / tweet_counter


    def add_following_ids(self, following_ids: List[str]):
        self.following_ids = list(set(self.following_ids + following_ids))

    def get_user_as_dict(self):
        return self.__dict__

    # Tweet getters
    def get_false_tweets(self):
        fake_tweets = []
        for topic in self.tweets['false']:
            fake_tweets = fake_tweets + self.tweets['false'][topic]
        return fake_tweets

    def get_pants_fire_tweets(self):
        pants_fire_tweets = []
        for topic in self.tweets['pants-fire']:
            pants_fire_tweets = pants_fire_tweets + self.tweets['pants-fire'][topic]
        return pants_fire_tweets

    def get_mostly_false_tweets(self):
        mostly_false_tweets = []
        for topic in self.tweets['mostly-false']:
            mostly_false_tweets = mostly_false_tweets + self.tweets['mostly-false'][topic]
        return mostly_false_tweets

    def get_true_tweets(self):
        true_tweets = []
        for topic in self.tweets['true']:
            true_tweets = true_tweets + self.tweets['true'][topic]
        return true_tweets

    def get_mostly_true_tweets(self):
        mostly_true_tweets = []
        for topic in self.tweets['mostly-true']:
            mostly_true_tweets = mostly_true_tweets + self.tweets['mostly-true'][topic]
        return mostly_true_tweets

    def get_half_true_tweets(self):
        half_true_tweets = []
        for topic in self.tweets['half-true']:
            half_true_tweets = half_true_tweets + self.tweets['half-true'][topic]
        return half_true_tweets

    # Retweet getters
    def get_false_retweets(self):
        fake_retweets = []
        for topic in self.retweets['false']:
            fake_retweets = fake_retweets + self.retweets['false'][topic]
        return fake_retweets

    def get_pants_fire_retweets(self):
        pants_fire_retweets = []
        for topic in self.retweets['pants-fire']:
            pants_fire_retweets = pants_fire_retweets + self.retweets['pants-fire'][topic]
        return pants_fire_retweets

    def get_mostly_false_retweets(self):
        mostly_false_retweets = []
        for topic in self.retweets['mostly-false']:
            mostly_false_retweets = mostly_false_retweets + self.retweets['mostly-false'][topic]
        return mostly_false_retweets

    def get_true_retweets(self):
        true_retweets = []
        for topic in self.retweets['true']:
            true_retweets = true_retweets + self.retweets['true'][topic]
        return true_retweets

    def get_mostly_true_retweets(self):
        mostly_true_retweets = []
        for topic in self.retweets['mostly-true']:
            mostly_true_retweets = mostly_true_retweets + self.retweets['mostly-true'][topic]
        return mostly_true_retweets

    def get_half_true_retweets(self):
        half_true_retweets = []
        for topic in self.retweets['half-true']:
            half_true_retweets = half_true_retweets + self.retweets['half-true'][topic]
        return half_true_retweets
    