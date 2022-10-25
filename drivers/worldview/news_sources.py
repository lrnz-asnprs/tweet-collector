from drivers.configs.directories import Directories
import pickle, os
import pandas as pd
dir = Directories()

class NewsOutletScorer():
    
    def __init__(self):
        """ 
        - Reads the political trust scores for 60 commmon US news outlets.
        """
        self.dir = Directories()
        self.news_outlets = self.read_news_outlets(dir.NEWS_OUTLETS_PATH, "news_outlets_elites.txt")
        self.news_outelets_dem_rep_scores = self.read_news_outlets_dem_rep_scores(dir.NEWS_OUTLETS_PATH, "dem_rep_trustscores.csv")
        self.users_news_exposure = {}
        
    
    def read_news_outlets(self, path, filename):
        news = {}
        with open(path / filename, "r") as reader:
            lines = reader.readlines()
            for line in lines:
                news[line.strip()] = 0
        return news
    
    def read_news_outlets_dem_rep_scores(self, path, filename):
        return pd.read_csv(path / filename)
    
    def read_user_recent_tweets(self, path, filename):
        with open(path / filename, "rb") as f:
            users_loaded_batch = pickle.load(f)
        return users_loaded_batch
    
    def get_users_recent_tweets(self, directory):
        recent_tweets_batches = []
        files = [file for file in  os.listdir(directory)]
        for file in files:
            recent_tweet_batch = self.read_user_recent_tweets(directory, file)
            recent_tweets_batches.append(recent_tweet_batch)
        return recent_tweets_batches
    
    
    def find_news_outlets_per_user_batch(self, user_batch):
        
        for key, user in user_batch.items():
            self.users_news_exposure[key] = None
            
            for tweet in user.recent_tweets:
                print(tweet)
                if "entities" in tweet.keys():
                    if 'urls' in tweet['entities'].keys():
                        if "expanded_url" in tweet['entities']['urls'][0]:
                            for news in self.news_outlets.keys():
                                if news in tweet['entities']['urls'][0]['expanded_url']:
                                    self.users_news_exposure[key].append(news)    
    
    def calculate_user_political_score(self):
        pass
    
    
    def get_users_news_outlet_scores(self):
        pass
    
