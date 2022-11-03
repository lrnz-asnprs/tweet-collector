from drivers.configs.directories import Directories
import pickle, os, re, json
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class NewsScorer250():
    
    def __init__(self, fake=True):
    
        self.dir = Directories()
        
        if fake:
            self.directory = self.dir.FAKE_USERS_RECENT_TWEETS_PATH
        else:
            self.directory = self.dir.TRUE_USERS_RECENT_TWEETS_PATH
        
        
        self.numeric_ideology = {'strong democratic':0.0,
                                 'lean democratic':0.25,
                                 'centrist':0.50,
                                 'lean republican':0.75,
                                 'strong republican':1.0}
        
        #Democrats/Republican news outlets and ideology scores.
        self.news = self.__read_news(self.dir.NEWS_OUTLETS_PATH, "dem_rep_news.json")
        self.__format_ideology_score()
        
        #User Exposure to News
        self.users_news_exposure = {}
        
  
    def __read_news(self, path, filename):
        """Helper method to retrieve the news outlet domains and their respective ideological position.

        Args:
            path (str): path to directory
            filename (str): the filename

        Returns:
            Dict: 250 common news outlets and the respective ideological position strong democratic and strong republican.
        """
        
        with open(path / filename) as fp:
            dict = json.load(fp)
        
        return dict
    
    def __format_ideology_score(self):
        for key, val in self.news.items():
            self.news[key] = self.numeric_ideology[val]           

    def __read_user_recent_tweets(self, path, filename):
        with open(path / filename, "rb") as f:
            users_loaded_batch = pickle.load(f)
        return users_loaded_batch
    
    def __read_users_recent_tweets(self):
        """Method to read the pickle files in a directory and convert them into one file.

        Args:
            directory (str): directory of the recent_tweets.pickle files.

        Returns:
            lst: Returns a list of converted pickle files. 
        """
        recent_tweets_batches = []
        files = [file for file in  os.listdir(self.directory)]
        for file in files:
            recent_tweet_batch = self.__read_user_recent_tweets(self.directory, file)
            recent_tweets_batches.append(recent_tweet_batch)
        return recent_tweets_batches
    
    
    def __find_news_per_user_batch(self, user_batch):
        """Helper method to find_news_per_user.

        Args:
            user_batch (lst): list of user objects
        """
        for key, user in user_batch.items():
            self.users_news_exposure[key] = []
            for tweet in user:
                if "entities" in tweet.keys():
                    if 'urls' in tweet['entities'].keys():
                        if "expanded_url" in tweet['entities']['urls'][0]:
                            for news in self.news.keys():
                                if news in tweet['entities']['urls'][0]['expanded_url']:
                                    self.users_news_exposure[key].append(news)    
    
    
    def find_news_per_user_batches(self):
        batches = self.__read_users_recent_tweets()
        
        for batch in batches:
            self.__find_news_per_user_batch(batch)
    
    
    def get_data_summary(self):
        df = pd.DataFrame(self.users_news_exposure.items())
        df[2] = df[1].apply(lambda x: len(x[:]))
        return df[2].describe(), print(f"{len(df[df[2]>0])}/{len(df)}".format())
        
    
    def calculate_user_ideology_score(self):
        self.user_ideology = {}

        for user_id, vals in self.users_news_exposure.items():
            #To avoid division by zero error
            if len(vals)==0:
                self.user_ideology[user_id] = None
                continue
            
            #Summing the total score
            score = 0
            for val in vals:
                score += float(self.news[val])
                
            
            user_ideology_avg_score = score/len(vals)
            
            self.user_ideology[user_id] = user_ideology_avg_score
        
    
    def get_user_ideology(self):
        try: 
            type(self.user_ideology)
        except:
            self.calculate_user_ideology_score()

        return self.user_ideology
    
    
    def full_run(self):
        """To run both the retrieval of users recent tweets and the calculation fo the ideology scores.

        Returns:
            dict: dictionary of user_ids and their ideology scores according to the news outlets that they share in their recent tweets.
        """
        self.find_news_per_user_batches()
        return self.get_user_ideology()
        